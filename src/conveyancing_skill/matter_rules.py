"""Conveyancing workbench: evidence-driven conditional checks, NOT legal certification.
All findings are triage, not lender approval or legal opinion. No external actions.
"""
from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path
import json
import re

from .matter_store import MatterError, validate_matter
from .matter_intelligence import contradictions, normalize

SOURCE_DATE = '2026-11-20'
AUTHORITIES = {
    'hmrc_sdlt':{'url':'https://www.gov.uk/guidance/check-if-you-need-to-send-a-stamp-duty-land-tax-return','checked':'2026-11-20'},
    'wra_ltt':{'url':'https://www.legislation.gov.uk/anaw/2017/1/section/44','checked':'2026-11-20'},
    'wra_ltt_payment':{'url':'https://www.gov.wales/pay-land-transaction-tax','checked':'2026-11-20'},
    'hmlr_pg12':{'url':'https://www.gov.uk/government/publications/official-searches-and-outline-applications/practice-guide-12-official-searches-and-outline-applications','checked':'2026-11-20'},
    'companies_house_mr01':{'url':'https://www.gov.uk/guidance/register-a-charge-mortgage-for-a-limited-company','checked':'2026-11-20'},
    'hmlr_requisitions':{'url':'https://www.gov.uk/guidance/hm-land-registry-requisitions','checked':'2026-11-20'},
    'hmlr_pg50':{'url':'https://www.gov.uk/government/publications/requisition-and-cancellation-procedures/practice-guide-50-requisition-and-cancellation-procedures','checked':'2026-11-20'},
    'hmlr_drs':{'url':'https://www.gov.uk/government/publications/digital-registration-service','checked':'2026-11-20'},
    'hmlr_execution':{'url':'https://www.gov.uk/government/publications/execution-of-deeds','checked':'2026-11-20'},
    'sra_ai':{'url':'https://www.sra.org.uk/solicitors/guidance/misuse-ai/','checked':'2026-11-20'},
    'uk_finance':{'url':'https://lendershandbook.ukfinance.org.uk/','checked':'2026-11-20'}
}

RISK = {'info':0,'low':1,'medium':2,'high':3,'critical':4}

def issue(code:str, title:str, severity:str='medium', evidence: list|None=None, action:str='', owner:str|None=None, source:str|None=None)->dict:
    if severity not in RISK:raise MatterError('Unknown severity')
    return {'id':code,'title':title,'severity':severity,'evidence_refs':evidence or [],'suggested_action':action,'owner':owner,
            'status':'outstanding','authority':SOURCE_DATE if source else None,'authority_url':AUTHORITIES[source]['url'] if source in AUTHORITIES else None,
            'human_decision':'pending'}

def as_date(value:str|None, label:str='date')->date|None:
    if not value:return None
    try:return date.fromisoformat(value)
    except (TypeError,ValueError) as e:raise MatterError(f'{label} must be YYYY-MM-DD') from e

def days_before(d:date,n:int,kind:str,holidays:list[str]|None)->date|None:
    if kind in ('working_days','business_days'):
        if holidays is None:return None
        h={as_date(x,'bank holiday') for x in holidays};count=0
        while count<n:
            d-=timedelta(days=1)
            if d.weekday()<5 and d not in h:count+=1
        return d
    if kind=='calendar_days':return d-timedelta(days=n)
    return None

def days_after(d:date,n:int,kind:str,holidays:list[str]|None)->date|None:
    if kind=='calendar_days':return d+timedelta(days=n)
    if kind not in ('working_days','business_days') or holidays is None:return None
    h={as_date(x,'bank holiday') for x in holidays};count=0
    while count<n:
        d+=timedelta(days=1)
        if d.weekday()<5 and d not in h:count+=1
    return d

def deadlines(m:dict,lender:dict|None=None)->dict:
    dt=m.get('dates',{})
    holidays=dt.get('bank_holidays') if isinstance(dt.get('bank_holidays'),list) else None
    out=[]
    def add(key,title,d,trigger,auth=None,notes=''):
        out.append({'key':key,'title':title,'due_date':d.isoformat() if d else None,'trigger':trigger,
                    'basis':auth,'official_source':AUTHORITIES[auth]['url'] if auth else None,
                    'status':'provisional_requires_case_check' if d else 'unresolved','notes':notes})
    effective=as_date(dt.get('tax_effective_date'),'tax_effective_date')
    if effective:
        if m.get('jurisdiction')=='England':
            add('sdlt','SDLT return and payment',effective+timedelta(days=14),'tax_effective_date','hmrc_sdlt','Ordinary notifiable transaction only. Substantial performance and exemptions require solicitor review; banking cut-off may be earlier.')
        if m.get('jurisdiction')=='Wales':
            add('ltt','LTT return and payment',effective+timedelta(days=30),'tax_effective_date','wra_ltt','Ordinary notifiable transaction only; any tax due must be received by filing deadline. See https://www.gov.wales/pay-land-transaction-tax; review transaction/date/exclusions and banking cut-offs.')
    created=as_date(dt.get('company_charge_created'),'company_charge_created')
    if created and m.get('specialist',{}).get('uk_company_or_llp_borrower') is True:
        add('mr01','Companies House charge registration',created+timedelta(days=21),'company_charge_created','companies_house_mr01','21-day period begins the day after creation. Confirm charge regime and delivery/acceptance requirements; missed deadlines may need court order.')
    pr=as_date(dt.get('priority_search_receipt'),'priority_search_receipt')
    if pr:
        # Period only calculable with jurisdiction-specific holidays supplied and verified.
        p=days_after(pr,30,'working_days',holidays)
        add('priority','Priority search protection period',p,'priority_search_receipt','hmlr_pg12','Actual OS1/OS2 certificate/receipt and working-day bank holidays must be checked. To guarantee day-list entry by expiry, HMLR advises delivery by noon that day; confirm applicability and instructions.')
    contractual=as_date(dt.get('contractual_completion'),'contractual_completion')
    current=as_date(dt.get('agreed_extended_completion'),'agreed_extended_completion')
    if contractual:add('completion_original','Original contractual completion',contractual,'contractual_completion',None,'Read contract, special conditions, exchange evidence and any valid extension.')
    if current:add('completion_extended','Proposed/agreed extended completion',current,'agreed_extended_completion',None,'Check actual written extension and whether notice, interest and other rights were reserved.')
    notice=dt.get('auction_notice',{})
    if notice:
        signed=as_date(notice.get('served_on'),'auction_notice.served_on')
        count=notice.get('days')
        kind=notice.get('unit')
        if signed and isinstance(count,int) and count>0 and kind in ('calendar_days','working_days','business_days'):
            add('notice_to_complete','Notice to complete candidate period end',days_after(signed,count,kind,holidays),'auction_notice',None,'Not a legal determination; check contractual time origin/service, excluded days, termination, interest and actual notice wording.')
        else:add('notice_to_complete','Notice to complete deadline not established',None,'auction_notice',None,'Exact contract terms and proof of service required.')
    if lender and lender.get('notice') and m.get('dates',{}).get('target_completion'):
        notice=lender['notice'];target=as_date(dt['target_completion'],'target_completion')
        minimum=notice.get('minimum');unit=notice.get('unit')
        if isinstance(minimum,int) and minimum>=0:
            earliest=days_before(target,minimum,unit,holidays)
            add('lender_cot_notice','Indicative latest lender CoT/drawdown notice',earliest,'target_completion',None,'Public directory snapshot only; offer, lender business-day counting, portal acceptance and cut-off must be confirmed. Bank holiday list needed for working-day computation.')
    out.sort(key=lambda x:(x['due_date'] is None,x['due_date'] or '9999'))
    return {'deadlines':out,'date_engine':'illustrative; actual transaction, statutory trigger and contract must be solicitor-verified',
            'holidays_supplied':holidays is not None,'sources_checked_on':SOURCE_DATE}

def lender_lookup(name:str, directory:dict)->dict:
    matches=[];target=normalize('lender_name',name)
    if not target:return {'matches':[],'status':'unknown'}
    for x in directory.get('lenders',[]):
        names=[x.get('lender','')]+x.get('aliases',[])
        if any(normalize('lender_name',n)==target for n in names):matches.append(x)
    return {'matches':matches,'status':'located' if matches else 'unlisted_check_current_offer',
            'warning':'Match is a 2026 research snapshot, not confirmed current CoT routing, panel membership, offer conditions or lender consent.'}

def evaluate_requirements(m:dict)->tuple[list[dict],dict]:
    issues=[];statuses={};recs=m.get('requirements',[])
    accepted={'verified','waived_by_lender','not_applicable'}
    for req in recs:
        if not isinstance(req,dict):continue
        rid=req.get('id','?');st=req.get('status','outstanding')
        statuses[st]=statuses.get(st,0)+1
        evidence=req.get('evidence_refs',[])
        if st not in accepted:
            if req.get('blocking',True):
                issues.append(issue('LENDER-'+rid,'Lender requirement not completed: '+req.get('description',rid),'high',evidence,'Obtain evidence, report adverse matters and any necessary written lender decision.'))
        if st=='verified' and (not evidence or not req.get('reviewed_by') or not req.get('reviewed_at')):
            issues.append(issue('LENDER-EVIDENCE-'+rid,'Claimed verified lender condition lacks documented solicitor review/evidence','high',evidence,'Record documentary evidence and qualified reviewer details; re-check original offer.'))
        if st=='waived_by_lender' and (not req.get('lender_written_approval_ref') or not req.get('lender_decision_date')):
            issues.append(issue('LENDER-WAIVER-'+rid,'Lender waiver has no written decision reference','critical',evidence,'Obtain and retain genuine lender written waiver, identifying condition and scope.'))
        if st=='not_applicable' and not req.get('applicability_rationale'):
            issues.append(issue('LENDER-NA-'+rid,'Non-applicable condition has no reason','medium',evidence,'Record reviewed rationale and person approving non-applicability.'))
        if not req.get('source_document_id') or not req.get('source_locator'):
            issues.append(issue('LENDER-SOURCE-'+rid,'Lender condition missing exact source locator','medium',evidence,'Link to actual offer, lender instructions, clause or page.'))
    return issues,{'total':len(recs),'status_counts':statuses,'open':sum(1 for x in recs if x.get('status','outstanding') not in accepted)}

def security_preflight(m:dict)->list[dict]:
    out=[]
    for sec in m.get('securities',[]):
        if not isinstance(sec,dict):continue
        sid=sec.get('id','SEC-?');refs=sec.get('evidence_refs',[])
        if not sec.get('property_id') or not sec.get('title_number'):
            out.append(issue('SEC-IDENT-'+sid,'Security property/title not uniquely identified','high',refs,'Check full title, estate and legal owner.'))
        rank=sec.get('intended_rank')
        if rank in ('second','third','subsequent') and sec.get('existing_charge_review')!='verified':
            out.append(issue('SEC-RANK-'+sid,'Lower-ranking security without verified existing-charge analysis','critical',refs,'Review existing first charge, restrictions, consents and any priority/deed of postponement.'))
        if rank in ('second','third','subsequent') and sec.get('prior_mortgagee_consent') not in ('verified','not_required_with_reason'):
            out.append(issue('SEC-CONSENT-'+sid,'Prior chargee consent/priority position not verified','high',refs,'Check lender permission, registered restrictions and actual lender security instructions.'))
        if sec.get('third_party_owner') and sec.get('third_party_advice')!='reviewed':
            out.append(issue('SEC-THIRD-'+sid,'Third-party security advice/consent unreviewed','high',refs,'Establish authority, conflicts, identity, advice and execution requirements.'))
        if not sec.get('charge_instrument_ref'):
            out.append(issue('SEC-CHARGE-'+sid,'No security deed/charge instrument identified','high',refs,'Confirm correct legal charge per security asset; TR1 is not a charge over retained property.'))
        if sec.get('company_charge_filing')=='outstanding':
            out.append(issue('SEC-MR01-'+sid,'Company charge filing outstanding','high',refs,'Check correct charge date, certified instrument and registration deadline.'))
    return out

def money(value,label:str)->Decimal:
    if isinstance(value,bool) or value is None:raise MatterError(f'{label} invalid amount')
    try:n=Decimal(str(value).replace(',','').replace('£',''))
    except (InvalidOperation, ValueError) as e:raise MatterError(f'{label} invalid amount') from e
    if not n.is_finite() or n.as_tuple().exponent<-2:raise MatterError(f'{label}: amount requires at most two decimal places')
    return n.quantize(Decimal('0.01'))

def accounting(m:dict)->dict:
    f=m.get('financials',{})
    required=['purchase_price','deposit_paid','seller_balance_stated','lender_net_advance','client_funds_confirmed','costs_and_disbursements','tax_and_filing']
    missing=[k for k in required if f.get(k) is None]
    if missing:return {'state':'insufficient_data','missing':missing,'approved_for_funds_release':False}
    vals={k:money(f[k],k) for k in required}
    adj=sum((money(x.get('amount'),'adjustment') for x in f.get('seller_adjustments',[])),Decimal('0'))
    expected=vals['purchase_price']-vals['deposit_paid']+adj
    total_need=vals['seller_balance_stated']+vals['costs_and_disbursements']+vals['tax_and_filing']
    total_source=vals['lender_net_advance']+vals['client_funds_confirmed']
    seller_diff=expected-vals['seller_balance_stated'];fund_gap=total_need-total_source
    return {'state':'reconciled_arithmetically_only' if seller_diff==fund_gap==0 else 'discrepancy_or_funding_gap',
            'seller_expected':str(expected),'seller_stated':str(vals['seller_balance_stated']),
            'seller_discrepancy':str(seller_diff),'total_needed':str(total_need),
            'funds_recorded':str(total_source),'funding_shortfall_positive':str(fund_gap),
            'approved_for_funds_release':False,'warning':'Arithmetic excludes unrecorded interest, redemption changes, fees, retentions and bank verification; no actual money was inspected.'}

def registration_preflight(m:dict)->list[dict]:
    r=m.get('registration',{});o=[]
    if not r:return [issue('REG-UNASSESSED','No registration pack recorded','high',[],'Identify AP1/FR1/other route and required evidence.')]
    refs=r.get('evidence_refs',[])
    if r.get('application_type') not in ('AP1','FR1','other_reviewed'):
        o.append(issue('REG-FORM','Application route not confirmed','high',refs,'Confirm official prescribed form and specific transaction requirements.'))
    if not r.get('title_numbers') and r.get('application_type')!='FR1':
        o.append(issue('REG-TITLE','No title numbers provided for registered application','high',refs,'Compare with official copies and executed deeds.'))
    if not r.get('deeds_reviewed'):
        o.append(issue('REG-DEEDS','Executed deeds not confirmed as reviewed','high',refs,'Check actual original/electronic execution against current HMLR practice guides.'))
    if r.get('restrictions') and any(x.get('status')!='satisfied_with_evidence' for x in r.get('restrictions',[])):
        o.append(issue('REG-RESTRICTION','Title restriction not evidenced as satisfied','critical',refs,'Obtain proper consent, certificate or other compliance evidence.'))
    if r.get('tax_return_required') and not r.get('tax_certificate_ref'):
        o.append(issue('REG-TAX','Missing tax certificate/evidence','high',refs,'Check SDLT5/LTT certificate or applicable no-return grounds.'))
    if r.get('fee_checked_against_live_scale') is not True:
        o.append(issue('REG-FEE','HMLR fee unverified','medium',refs,'Check current HMLR fee order and application method.'))
    if r.get('priority_result_reviewed') is not True:
        o.append(issue('REG-PRIORITY','Priority search not evidenced/reviewed','high',refs,'Verify current OS1/OS2 result, beneficiary and protection period.'))
    if r.get('filing_acknowledgement') and not r.get('registration_completed_evidence'):
        o.append(issue('REG-PENDING','Application lodged but registration not confirmed','medium',refs,'Monitor requisitions, register changes and lender charge priority.'))
    return o

def execution_preflight(m:dict)->list[dict]:
    result=[]
    for x in m.get('execution',[]):
        if not isinstance(x,dict):continue
        ref=x.get('document_id','unknown');e=[ref]
        if not x.get('signatory_capacity'):
            result.append(issue('EXEC-CAP-'+ref,'Signatory authority/capacity not documented','high',e,'Check proprietor, attorney, office and authority under appropriate law.','solicitor','hmlr_execution'))
        if x.get('execution_route') in ('individual_with_witness','director_with_witness'):
            if not x.get('witness_name') or not x.get('witness_address') or not x.get('presence_attested'):
                result.append(issue('EXEC-WIT-'+ref,'Witness details/presence evidence incomplete','high',e,'Check original executed document and the correct deed formalities.','solicitor','hmlr_execution'))
        if x.get('electronic_signature') and not x.get('electronic_signing_route_reviewed'):
            result.append(issue('EXEC-ESIG-'+ref,'Electronic-signature method requires independent legal review','high',e,'Apply the relevant current HMLR practice guide and lender/transaction restrictions.','solicitor','hmlr_execution'))
        if x.get('status')!='original_reviewed':
            result.append(issue('EXEC-ORIGINAL-'+ref,'Execution original/electronic source not reviewed','high',e,'Visual verification of signed instrument is required.'))
    return result

SPECIALIST_CHECKS = {
 'leasehold': [('lease_reviewed','Lease and variations not reviewed'),('management_pack_reviewed','Management information not reviewed'),('notices_and_restrictions_checked','Notices and restrictions unchecked')],
 'building_safety': [('applicability_reviewed','Building Safety Act applicability not established'),('certificates_reviewed','Landlord/leaseholder certificate evidence unreviewed')],
 'tenancy': [('occupation_checked','Occupation and tenancy position unverified'),('lender_reportability_checked','Tenancy position not reconciled with lender requirements')],
 'unregistered': [('epitome_reviewed','Unregistered title deeds/epitome not reviewed'),('land_charges_search_reviewed','Land Charges searches not reviewed'),('first_registration_evidence_checked','First registration evidence unreviewed')],
 'commercial': [('vat_togc_checked','VAT, option to tax or TOGC status not analysed'),('lta_1954_checked','LTA 1954 status unreviewed')],
 'probate_trust': [('authority_reviewed','Representative/trustee authority unverified'),('execution_authority_reviewed','Execution power not reviewed')],
 'new_build': [('planning_and_building_docs_reviewed','Planning/building approvals not reviewed'),('warranty_reviewed','Warranty/security acceptance unreviewed')],
}

def specialist_preflight(m:dict)->list[dict]:
    s=m.get('specialist',{});result=[]
    for category,checks in SPECIALIST_CHECKS.items():
        data=s.get(category)
        if not isinstance(data,dict) or not data.get('applicable'):continue
        for field,title in checks:
            if data.get(field) is not True:
                result.append(issue('SP-'+category.upper()+'-'+field,title,'medium',data.get('evidence_refs',[]),'Obtain primary documents and solicitor review; do not infer satisfaction.'))
    return result

def review(m:dict,lender_dir:dict|None=None)->dict:
    errors=validate_matter(m)
    if errors:raise MatterError('; '.join(errors))
    issues=[]
    for c in contradictions(m):
        refs=[f"{entry.get('document_id')} {entry.get('locator')}" for variant in c['variants'] for entry in variant]
        issues.append(issue('FACT-'+c['field'].upper(),'Contradictory '+c['field']+' in matter evidence',c['severity'],refs,c['action']))
    lender_result={'status':'not_evaluated'}
    if m.get('lender',{}).get('name'):
        lender_result=lender_lookup(m['lender']['name'],lender_dir or {'lenders':[]})
        if not lender_result['matches']:
            issues.append(issue('LENDER-NOT-FOUND','Lender product/routing unverified','medium',[],'Check live mortgage offer, panel, current Part 2 and lender instructions.'))
        elif len(lender_result['matches'])>1:
            issues.append(issue('LENDER-AMBIGUOUS','Multiple lender directory matches','high',[],'Resolve exact legal entity and product before selecting CoT/RoT.'))
        if not m.get('lender',{}).get('live_instructions_checked'):
            issues.append(issue('LENDER-LIVE','Live offer/handbook/special conditions not confirmed','high',[],'Check live lender instructions and version before drawdown/certification.'))
    reqissues,reqsummary=evaluate_requirements(m);issues.extend(reqissues)
    linked={x.get('candidate_ref') for x in m.get('requirements',[]) if isinstance(x,dict)}
    untriaged=[x for x in m.get('lender_condition_candidates',[]) if x.get('candidate_id') not in linked]
    if untriaged:
        issues.append(issue('LENDER-CANDIDATES','Potential mortgage-offer conditions require triage against the full originals','high',
            [x.get('source_document_id','?')+' '+x.get('source_locator','?') for x in untriaged[:15]],
            'Review every candidate against original offer and Part 2/3; record actual conditions under requirements with candidate_ref, proper source locator and status outstanding.'))
    reqsummary['untriaged_text_candidates']=len(untriaged)
    issues.extend(security_preflight(m))
    issues.extend(registration_preflight(m))
    if m.get('registration'):
        from .matter_lifecycle import form_preflight, requisitions
        issues.extend(form_preflight(m)['issues'])
        for rec in requisitions(m)['items']:
            if rec['status'] not in ('closed_confirmed','cancelled'):
                issues.append(issue('REG-REQ-'+rec['id'],'HMLR requisition not confirmed closed','high',rec['evidence_refs'],'Verify original requisition, actual deadline, acknowledgement and required supporting documents.'))
    issues.extend(execution_preflight(m))
    issues.extend(specialist_preflight(m))
    financial=accounting(m)
    if financial['state']=='discrepancy_or_funding_gap':
        issues.append(issue('FUNDS-RECON','Completion figures not reconciled','critical',[],'Resolve seller statement and funding shortfall with authorised staff; independent bank detail checks required.'))
    elif financial['state']=='insufficient_data':
        issues.append(issue('FUNDS-MISSING','Completion money evidence incomplete','high',[],'Obtain verified completion statement and financial inputs; no funds release.'))
    docs=m.get('documents',[])
    revisions={}
    for d in docs:
        if d.get('document_type') and d.get('sha256'):
            revisions.setdefault(d['document_type'],set()).add(d['sha256'])
    for dtype,hashes in revisions.items():
        if len(hashes)>1 and any(d.get('document_type')==dtype and d.get('review_state')!='superseded' for d in docs):
            issues.append(issue('DOC-VERSION-'+dtype.upper(),'Multiple versions of document type '+dtype+' remain on file','medium',[d.get('document_id','?') for d in docs if d.get('document_type')==dtype], 'Identify controlling revision; compare all operative changes and avoid executing a superseded document.'))
    if not docs:issues.append(issue('DOC-NONE','No matter documents on record','high',[],'Register and review source documents.'))
    elif any(x.get('review_state')!='reviewed_by_lawyer' for x in docs):
        issues.append(issue('DOC-UNREVIEWED','Some documents remain unreviewed or machine-extracted only','medium',[x.get('document_id','?') for x in docs if x.get('review_state')!='reviewed_by_lawyer'],'Solicitor to check relevant originals and source evidence.'))
    h=m.get('review',{})
    if h.get('decision') not in ('approved','lawyer-approved') or not h.get('reviewer') or not h.get('reviewed_at'):
        issues.append(issue('LEGAL-SIGNOFF','Qualified lawyer review is outstanding','critical',[],'Obtain actual matter-specific sign-off through firm-approved process.'))
    match=lender_result['matches'][0] if len(lender_result.get('matches',[]))==1 else None
    dd=deadlines(m,match)
    tasks=[{'issue_id':x['id'],'action':x['suggested_action'],'status':'outstanding','owner':x['owner'],'deadline':None} for x in issues]
    return {'matter_id':m['matter_id'],'generated_at':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(timespec='seconds'),
            'review_type':'supervised_preflight_not_legal_opinion','issue_count':len(issues),
            'risk_level':max((x['severity'] for x in issues),key=lambda x:RISK[x],default='info'),
            'issues':issues,'requirements':reqsummary,'lender':lender_result,'securities_count':len(m.get('securities',[])),
            'financial_reconciliation':financial,'deadlines':dd,'actions':tasks,
            'ready_to_certify':False,'ready_to_exchange':False,'ready_to_release_funds':False,'ready_to_file':False,
            'authority_sources':AUTHORITIES,
            'limitations':['AI cannot certify title, confirm true lender consent, verify client account funds or file forms.',
                           'Source snapshots and proposed dates require live matter-specific review.',
                           'All extracted observations are candidates, not independently verified facts.']}
