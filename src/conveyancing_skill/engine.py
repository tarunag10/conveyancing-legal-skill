"""No-network deterministic conveyancing quality gates and calculations.

The CLI does not perform legal sign-off, bank verification or source refresh.
"""
from __future__ import annotations
import json
import re
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

class LegalReviewRequired(ValueError):
    """Refuse to assume a fact, tax category, legal source or deadline."""


def load(rel: str):
    path=(ROOT / rel).resolve()
    if ROOT not in path.parents:
        raise LegalReviewRequired('Path must stay within repository')
    return json.loads(path.read_text(encoding='utf8'))


def money(value) -> Decimal:
    if isinstance(value, bool):
        raise LegalReviewRequired('Boolean is not a monetary amount')
    try:
        n = Decimal(str(value))
    except (InvalidOperation, ValueError) as e:
        raise LegalReviewRequired(f'Invalid monetary amount: {value!r}') from e
    if not n.is_finite():
        raise LegalReviewRequired('Non-finite amount is invalid')
    return n.quantize(Decimal('0.01'),rounding=ROUND_HALF_UP)


def fmt(v):
    return f'£{v:,.2f}'


def _tax_snapshot_cutoff(data):
    """Return the last date usable under both the verification and review limits."""
    try:
        verified=date.fromisoformat(data['last_verified_date'])
        review_by=date.fromisoformat(data['review_by'])
    except (KeyError, TypeError, ValueError) as e:
        raise LegalReviewRequired('Tax snapshot has invalid verification dates; verify the source data') from e
    return min(verified,review_by)


def forms(query:str):
    q=query.lower().strip()
    return [x for x in load('knowledge/forms/catalogue.json') if q in x['code'].lower() or q in x['official_title'].lower()]


def workflow(profile: str):
    stages=load('knowledge/workflows/stages.json')
    matches=[x for x in load('knowledge/workflows/profiles.json') if x['id']==profile]
    if not matches:
        raise LegalReviewRequired(f'Unknown profile {profile}; use workflow --list')
    return {'profile': matches[0], 'stages': stages, 'approval_state':'none; all evidence gates remain outstanding'}


def tax_estimate(jurisdiction: str, price, as_of: str, additional=False, *, acknowledge_simple=False, complexity_flags=()):
    """Constrained snapshot calculation, refused outside review window or scope."""
    if not acknowledge_simple:
        raise LegalReviewRequired('Must explicitly acknowledge this is a simple residential illustrative case')
    if complexity_flags:
        raise LegalReviewRequired('Complex tax issue requires specialist review: '+', '.join(complexity_flags))
    data=load('knowledge/legislation/tax-rates.json')
    try:
        d=date.fromisoformat(as_of)
    except (TypeError, ValueError) as e:
        raise LegalReviewRequired('Invalid calculation date; use YYYY-MM-DD') from e
    cutoff=_tax_snapshot_cutoff(data)
    if d>cutoff:
        raise LegalReviewRequired(f'Tax snapshot verified only through {cutoff}; verify current official rates for this date')
    rate = next((r for r in data['regimes'] if r['jurisdiction']==jurisdiction.lower() and r['additional']==additional),None)
    if rate is None: raise LegalReviewRequired('Unknown jurisdiction/regime')
    if d<date.fromisoformat(rate['effective_from']): raise LegalReviewRequired('No historical rates included for requested date')
    value=money(price)
    if value < 0: raise LegalReviewRequired('Purchase price must not be negative')
    tax=Decimal('0'); lower=Decimal('0'); breakdown=[]
    for band in rate['bands']:
        upper=Decimal(band['limit']) if band['limit'] else value
        taxable=max(Decimal(0),min(value,upper)-lower)
        portion=(taxable*Decimal(band['rate'])).quantize(Decimal('0.01'),rounding=ROUND_HALF_UP)
        breakdown.append({'from':str(lower),'to':str(upper) if band['limit'] else 'above', 'taxed':str(taxable),'rate':band['rate'],'duty':str(portion)})
        tax+=portion
        if value<=upper: break
        lower=upper
    return {'jurisdiction':jurisdiction,'regime':rate['id'],'price':str(value),'tax':str(tax),'breakdown':breakdown,'source_url':rate['source'],'snapshot_verified':data['last_verified_date'],'effective_from':rate['effective_from'],'review_by':data['review_by'],'legal_status':'ILLUSTRATIVE ONLY; validate reliefs, surcharges, chargeable consideration and rates at actual effective date'}


def statutory_deadline(event: str, on: str, holidays=None):
    start=date.fromisoformat(on)
    e=event.lower()
    if e in ('sdlt','hmrc-sdlt'): days=14;typ='calendar'
    elif e in ('ltt','wra-ltt'): days=30;typ='calendar'
    elif e in ('mr01','company-charge'): days=21;typ='calendar'
    elif e in ('priority','os1','os2'):days=30;typ='working'
    else: raise LegalReviewRequired('Unknown deadline rule; contractual deadlines must be independently supplied and construed')
    if typ=='calendar':
        due=start+timedelta(days=days)
        comment='Unadjusted legal period; effective/creation date and service must be confirmed. Payment banking cutoff may precede this date.'
    else:
        if holidays is None:
            raise LegalReviewRequired('Priority calculation needs explicit public-holiday calendar and actual application RECEIPT date; no inferred holidays')
        hs={date.fromisoformat(x) for x in holidays};due=start;n=0
        while n<days:
            due+=timedelta(days=1)
            if due.weekday()<5 and due not in hs: n+=1
        comment='Provisional expiry by HMLR PG12: midnight end of 30th working day after receipt. Confirm actual day-list and official HMLR calculation.'
    return {'type':e,'event_date':str(start),'due_date':str(due),'period_days':days,'day_type':typ,'warning':comment}


def completion(statement:dict):
    """Buyer-side reconciliation. All amounts are input figures, NOT verified bank balances."""
    if statement.get('side')!='buyer':
        raise LegalReviewRequired('This deterministic statement currently supports buyer-side only')
    needed=['purchase_price','deposit_paid','cleared_client_funds','cleared_lender_funds']
    missing=[k for k in needed if k not in statement]
    if missing: raise LegalReviewRequired('Missing monetary inputs: '+', '.join(missing))
    price=money(statement['purchase_price']);deposit=money(statement['deposit_paid'])
    if price<0 or deposit<0 or deposit>price:raise LegalReviewRequired('Invalid purchase or deposit amounts')
    seller_debits = sum((money(x['amount']) for x in statement.get('seller_debits',[])),Decimal(0))
    seller_credits = sum((money(x['amount']) for x in statement.get('seller_credits',[])),Decimal(0))
    other = sum((money(x['amount']) for x in statement.get('other_payments',[])),Decimal(0))
    if any(money(x['amount'])<0 for k in ('seller_debits','seller_credits','other_payments') for x in statement.get(k,[])):
        raise LegalReviewRequired('Item amounts must be nonnegative: use appropriate debit/credit category')
    due_seller=price-deposit+seller_debits-seller_credits
    if due_seller<0: raise LegalReviewRequired('Negative seller completion sum: verify apportionments')
    spending=due_seller+other
    cleared=money(statement['cleared_client_funds'])+money(statement['cleared_lender_funds'])
    if min(money(statement['cleared_client_funds']),money(statement['cleared_lender_funds']))<0:
        raise LegalReviewRequired('Funds cannot be negative')
    gap=(cleared-spending).quantize(Decimal('0.01'))
    blockers=[]
    if gap<0: blockers.append('Funds shortfall based on input amounts')
    if not statement.get('bank_evidence_confirmed_by_human',False):blockers.append('Actual bank cleared funds not independently confirmed by authorised user')
    if not statement.get('lender_conditions_satisfied_by_human',False):blockers.append('Lender conditions not confirmed by authorised user')
    return {'purchase_price':str(price),'deposit_credit':str(deposit),'seller_debits':str(seller_debits),'seller_credits':str(seller_credits),'balance_due_to_seller':str(due_seller),'other_payments':str(other),'total_required_at_completion':str(spending),'input_cleared_funds':str(cleared),'surplus_or_shortfall':str(gap),'completion_blockers':blockers,'ready_to_send_funds':False,'disclaimer':'No bank feed, lender authority or actual payment verified. Human-only completion release.'}

# Detect issues from structured, explicit case assertions: never claim to have parsed an unsupplied deed.
def review_matter(m:dict):
    issues=[]
    def add(code,levels,fact,missing,action,source=None,blocker=False,document_id=None,locator=None,requirement_ref=None):
        issue={'code':code,'risk_levels':levels,'recorded_fact':fact,'missing_evidence':missing,'next_action':action,'evidence_ref':source or 'No satisfactory primary evidence supplied','completion_blocker':blocker}
        if document_id or locator:
            issue['evidence_location']={'document_id':document_id,'locator':locator}
        if requirement_ref:
            issue['requirement_source_ref']=requirement_ref
        issues.append(issue)
    docs=m.get('documents',[])
    titles={d.get('title_number') for d in docs if d.get('title_number')}
    addresses={re.sub(r'\s+',' ',d.get('property_address','').strip()).lower() for d in docs if d.get('property_address')}
    if len(titles)>1 and not m.get('multiple_titles_explained'):
        add('TITLE_NUMBER_CONFLICT',['R1','R3'],'Document metadata names different title numbers','Identify exact interests held and being transferred','Compare official registers and related titles',blocker=True)
    if len(addresses)>1:
        add('ADDRESS_CONFLICT',['R1'],'Document metadata contains different property descriptions','Check land extent and whether one address is historic','Require rectification or satisfactory documentary explanation',blocker=False)
    for c in m.get('charges',[]):
        state=c.get('status','unknown').lower()
        evidence=c.get('evidence_type','').lower()
        if state in ('vacated','discharged','redeemed','released') and (evidence not in ('registered_discharge','executed_release','accepted_e-ds1','accepted_eds1','official_register_updated','acceptable_endorsed_receipt') or not c.get('evidence_ref')):
            add('UNPROVEN_CHARGE_DISCHARGE',['R2','R3','R4'],f'Claimed {state} for charge {c.get("id","unknown")}','Satisfactory executed/recorded discharge and full scope of release','Obtain discharge evidence and verify registration / lender acceptance',c.get('evidence_ref'),blocker=True,document_id=c.get('evidence_document_id'),locator=c.get('evidence_locator'))
        elif state in ('outstanding','unknown'):
            add('OUTSTANDING_CHARGE',['R2','R3','R4'],f'Charge {c.get("id","unknown")} not proven discharged','Redemption and release mechanism','Seek documentary release and assess lender priority',c.get('evidence_ref'),blocker=True,document_id=c.get('evidence_document_id'),locator=c.get('evidence_locator'))
    for r in m.get('restrictions',[]):
        if r.get('required') and (r.get('status') not in ('verified','authorised_waiver') or not r.get('evidence_ref') or not r.get('checked_by_human')):
            add('UNSATISFIED_RESTRICTION',['R2','R4'],r.get('wording','Restriction recorded'),'Correct certificate/consent or registrar-acceptable removal','Request evidence satisfying the exact restriction',r.get('evidence_ref'),blocker=True,document_id=r.get('evidence_document_id'),locator=r.get('evidence_locator'))
    access=m.get('access',{})
    if access.get('public_highway_claimed') and not (access.get('official_highways_confirmation') and access.get('evidence_ref') and access.get('checked_by_human')):
        add('HIGHWAY_STATUS_UNVERIFIED',['R1','R3'],'Property stated to abut or have access to a public highway','Highway authority confirmation and legal access route','Verify adoption/public highway extent and deed rights',access.get('evidence_ref'),blocker=bool(access.get('critical_to_lender',False)),document_id=access.get('evidence_document_id'),locator=access.get('evidence_locator'))
    for x in m.get('lender_requirements',[]):
        if (x.get('status') not in ('verified','waived_by_lender','not_applicable') or not x.get('source_ref') or not x.get('evidence_ref') or not x.get('checked_by_human')):
            add('LENDER_CONDITION_OPEN',['R3','R4'] if x.get('blocking') else ['R1','R3'],f'Lender requirement {x.get("id","unknown")}: {x.get("text","not transcribed")}','Evidence or written lender waiver','Obtain and verify precisely required document/approval',x.get('evidence_ref'),blocker=bool(x.get('blocking')),document_id=x.get('evidence_document_id'),locator=x.get('evidence_locator'),requirement_ref=x.get('source_ref'))
    if m.get('building_safety',{}).get('potentially_applicable') and not m.get('building_safety',{}).get('documented_assessment'):
        add('BUILDING_SAFETY_UNASSESSED',['R2','R3'],'Building Safety Act protections may apply (not yet evidenced)','Building and lease status, landlord/leaseholder certificates as applicable','Evaluate England-specific rules and lender evidence',blocker=True)
    for req in m.get('missing_documents',[]):
        add('MISSING_DOCUMENT',['R1'],f'Missing: {req}','Required document','Obtain and assess before sign-off')
    doc_register=[{'document_id':d.get('document_id'),'document_type':d.get('document_type')} for d in docs]
    return {'matter_id':m.get('matter_id','UNSPECIFIED'),'jurisdiction':m.get('jurisdiction','UNKNOWN'),'transaction_type':m.get('transaction_type'),'observed_document_count':len(docs),'document_register':doc_register,'issues':issues,'completion_blockers':[i['code'] for i in issues if i['completion_blocker']],'completion_readiness':'NOT ASSESSED / NO AUTOMATED SIGN-OFF','notices':['Findings use only structured facts provided to the CLI; no underlying signatures or legal instruments authenticated.','Evidence locations are user-entered references, not verified citations; check every reference against the original.','Underlying lender and statutory source instructions need current use-point verification.']}
