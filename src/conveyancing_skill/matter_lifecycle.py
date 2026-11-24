"""Matter lifecycle views and quality checks. All deadlines are provisional and sources local."""
from __future__ import annotations
from datetime import date
from .matter_store import MatterError
from .matter_rules import issue,deadlines,as_date,security_preflight


def security_map(m:dict)->dict:
    properties=[];titles=set();warnings=[]
    for s in m.get('securities',[]):
        sid=s.get('id','UNKNOWN');title=s.get('title_number');property_id=s.get('property_id')
        if title and title in titles:
            warnings.append({'code':'DUPLICATE-SECURITY-TITLE','title_number':title,'security_id':sid,
                             'note':'Check whether this is an intentional shared title, additional instrument or duplicate entry.'})
        if title:titles.add(title)
        properties.append({'security_id':sid,'property_id':property_id,'title_number':title,
                           'legal_owner':s.get('legal_owner'),'intended_rank':s.get('intended_rank','unconfirmed'),
                           'prior_mortgagee_consent':s.get('prior_mortgagee_consent','outstanding'),
                           'charge_document':s.get('charge_instrument_ref'),
                           'third_party_owner':s.get('third_party_owner',False),
                           'existing_charge_review':s.get('existing_charge_review','unknown'),
                           'discharged':s.get('discharge_evidence_ref'),
                           'lender_instructions_status':s.get('lender_instructions_status','unverified')})
    return {'properties':properties,'identified_estates':len(properties),'warnings':warnings,
            'preflight_issues':security_preflight(m),
            'legal_status':'Security mapping is informational; deed rank, discharge, consent, restrictions and perfection require actual source review.'}


def requisitions(m:dict,as_of:str|None=None)->dict:
    ason=as_date(as_of,'as_of') if as_of else None
    r=m.get('registration',{}).get('requisitions',[])
    out=[]
    for i,x in enumerate(r,1):
        rid=x.get('id') or f'REQ-{i}';due=as_date(x.get('deadline'),'requisition deadline')
        served=as_date(x.get('issued_on'),'requisition issued_on')
        extended=as_date(x.get('extension_confirmed_to'),'requisition extension')
        effective=extended or due
        warning=[]
        if not x.get('actual_requisition_ref'):warning.append('Original HMLR requisition/reference not provided.')
        if not effective:warning.append('No evidenced response deadline; do not calculate a generic period.')
        if x.get('extension_requested') and not x.get('extension_approval_ref'):
            warning.append('Requested extension not evidenced as granted; use original deadline unless confirmed.')
            effective=due
        if x.get('status') in ('answered','response_sent') and not x.get('acknowledgement_ref'):
            warning.append('Sending a response does not prove accepted compliance.')
        overdue=bool(effective and ason and effective<ason and x.get('status') not in ('closed_confirmed','cancelled'))
        out.append({'id':rid,'issued_on':served.isoformat() if served else None,
                    'original_deadline':due.isoformat() if due else None,
                    'effective_deadline_if_confirmed':effective.isoformat() if effective else None,
                    'status':x.get('status','outstanding'),'overdue_as_of_supplied_date':overdue,
                    'warnings':warning,'evidence_refs':x.get('evidence_refs',[])})
    return {'items':out,'count':len(out),'as_of':as_of,
            'warning':'Use exact actual HMLR requisition/extension and source evidence. The workbench does not retrieve live case status or determine HMLR outcome.'}


def post_completion(m:dict,as_of:str|None=None,lender:dict|None=None)->dict:
    dd=deadlines(m,lender);r=m.get('registration',{});s=m.get('specialist',{})
    values=m.get('post_completion',{})
    tasks=[]
    def entry(key,title,required=True,ref=None,due_key=None):
        if not required:return
        due=next((x['due_date'] for x in dd['deadlines'] if x['key']==due_key),None)
        saved=values.get(key,{})
        status=saved.get('status','outstanding')
        if status in ('completed','accepted','registered') and not saved.get('external_evidence_ref'):
            status='claimed_done_without_external_evidence'
        tasks.append({'id':key,'title':title,'status':status,'deadline':due,
                      'evidence_ref':saved.get('external_evidence_ref'),
                      'owner':saved.get('owner'),
                      'last_checked':saved.get('last_checked'),
                      'note':'This is an evidence tracker, not a filing or satisfaction certificate.'})
    entry('tax','SDLT/LTT return, payment, certificate or documented exception', True,due_key='sdlt' if m.get('jurisdiction')=='England' else 'ltt')
    entry('hmlr','HMLR application with correct title, priority and instruments')
    entry('previous_charge','Discharge previous security/DS1/e-DS1 as applicable')
    entry('tax_certificate','Retain SDLT5/WRA evidence if reportable', bool(r.get('tax_return_required')))
    entry('company_charge','Companies House company charge filing and acceptance',bool(s.get('uk_company_or_llp_borrower')),due_key='mr01')
    entry('notices','Leasehold/management/company notices and compliance documents',bool(s.get('leasehold',{}).get('applicable')))
    entry('hmlr_requisitions','HMLR requisitions responded to and independently cleared',bool(r.get('requisitions')))
    entry('final_register','Final official copies compared to intended proprietor, charge, rank and restrictions')
    entry('report_to_lender','Final registered security and lender reporting')
    entry('undertakings','Discharge and record any post-completion undertakings')
    entry('ledger','Client ledger reconciliation and residual balances reviewed')
    if as_of:
        d=as_date(as_of,'as_of')
        for t in tasks:
            t['past_due']=bool(t['deadline'] and as_date(t['deadline'])<d and t['status'] not in ('completed','accepted','registered'))
    return {'matter_id':m['matter_id'],'as_of':as_of,'tasks':tasks,'outstanding':sum(t['status'] not in ('completed','accepted','registered') for t in tasks),
            'requisitions':requisitions(m,as_of),
            'registration_application_status':r.get('submission_status','not_submitted_or_unverified'),
            'registration_completion_status':r.get('registration_completed_evidence') or 'NOT CONFIRMED',
            'warning':'Filing receipt, requisition satisfaction and final registration are separate actual events. Review original documents and live external acceptance.'}


def form_preflight(m:dict)->dict:
    r=m.get('registration',{});route=r.get('application_type','unknown');issues=[]
    refs=r.get('evidence_refs',[])
    if route in ('AP1','FR1'):
        if not r.get('official_form_revision_checked'):
            issues.append(issue('FORM-REVISION','HMLR form revision/route not checked','high',refs,'Use official current prescribed form and current application guidance.'))
        if not r.get('signatory_identification_checked'):
            issues.append(issue('FORM-SIGN','Signatory capacity/identity unchecked','high',refs,'Compare deeds, power of attorney/representatives and execution against correct form panel.'))
    if route=='FR1':
        if not m.get('specialist',{}).get('unregistered',{}).get('epitome_reviewed'):
            issues.append(issue('FORM-FR1-EPITOME','First-registration evidence incomplete','high',refs,'Review root of title, original deeds, Land Charges and plan.'))
        if r.get('title_numbers'):
            issues.append(issue('FORM-FR1-TITLES','FR1 case lists an existing title number','medium',refs,'Confirm whether first registration or registration of an additional estate/title is appropriate.'))
    for field,label in [('proprietor_names_checked','Proprietors/transferees not cross-checked'),
                         ('charge_details_checked','Incoming charges not cross-checked'),
                         ('property_description_checked','Property and plan extent not cross-checked')]:
        if r.get(field) is not True:
            issues.append(issue('FORM-'+field.upper(),label,'high',refs,'Check register, title plan, actual transfer and legal charge in relevant panels.'))
    return {'form':route,'issues':issues,'form_check_status':'manual_preflight_only',
            'warnings':['AP1, FR1, TR1/TP1 and lender documents must use actual current official/authorised originals.',
                        'No form has been signed, generated as a prescribed facsimile, filed or accepted.']}
