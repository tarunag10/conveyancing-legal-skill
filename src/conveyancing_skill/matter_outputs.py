"""Accessible previews, drafts and reversible integration handoff; no sending or filings."""
from __future__ import annotations

from csv import DictWriter
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from string import Template
import json
import os

from .matter_store import MatterError

DRAFTS = {
 'lender-report': {
  'subject':'Matter $reference: lender decision requested on outstanding title/security matters',
  'body':"""Dear Lender Solicitor,

Re: $reference
Property/security: $property
Borrower: $borrower

We act in connection with the above matter. The following matters require confirmation or a written decision under the current offer and your instructions:

$issues

We would be grateful if you would review the above and provide written directions, identifying any conditions or documentation required before drawdown.

For the avoidance of doubt, no lender consent or waiver is assumed pending your written response.

Kind regards,
[Authorised fee earner / firm signature]"""},
 'seller-enquiries': {
  'subject':'$reference: further title and completion enquiries',
  'body':"""Dear Colleagues,

Re: $property
Our reference: $reference

We have reviewed the documents currently available. Please could you provide the following information and supporting documentation:

$issues

We would be grateful if you could identify the source deed, register entry or plan for your replies where relevant.

Kind regards,
[Authorised fee earner / firm signature]"""},
 'client-update': {
  'subject':'$reference: transaction update and outstanding matters',
  'body':"""Dear Client,

Re: $property

We are progressing your matter. The principal points still requiring attention are:

$issues

Please note that any proposed completion date remains subject to outstanding documentation, lender requirements and the solicitor's final review. We will confirm the position once those checks have been completed.

Kind regards,
[Authorised fee earner / firm signature]"""},
 'auction-extension':{
  'subject':'$reference: request for extension of completion',
  'body':"""Dear Colleagues,

Re: $property
Our reference: $reference

We write to request your client's agreement to extend the contractual completion date to [INSERT PROPOSED DATE].

Please confirm your client's instructions, the precise terms of any agreed extension, whether interest or other rights are reserved, and whether any notice to complete has been or will be served.

No amendment to the contract or waiver is assumed unless expressly agreed in writing.

Kind regards,
[Authorised fee earner / firm signature]"""},
 'completion-chaser':{
  'subject':'$reference: urgent confirmation of completion requirements',
  'body':"""Dear Colleagues,

Re: $property
Our reference: $reference

Please may we have an urgent update on the outstanding matters listed below, together with any revised completion statement and confirmation of the relevant completion arrangements:

$issues

We would be grateful for a response as soon as practicable. This email does not constitute an undertaking or acceptance of any revised terms.

Kind regards,
[Authorised fee earner / firm signature]"""},
 'lender-cot-query':{
  'subject':'$reference: Certificate of Title / Report on Title submission instructions',
  'body':"""Dear Lender Completions Team,

Re: $reference
Property/security: $property

Please would you confirm the approved current Certificate of Title or Report on Title form applicable to this facility, the authorised submission method (including case-specific electronic portal where applicable), the minimum notice for drawdown and any outstanding conditions.

We should be grateful if you would also identify the appropriate contact or portal access route where the matter is not visible.

Kind regards,
[Authorised fee earner / firm signature]"""},
 'registration-requisition':{
  'subject':'$reference: HM Land Registry requisition response (draft)',
  'body':"""Dear HM Land Registry,

Re: $reference
Property: $property
Application reference: [INSERT APPLICATION REFERENCE]
Requisition dated: [INSERT ACTUAL DATE]

We refer to the requisition and set out below our proposed response, subject to verification against the notice and documents:

$issues

Enclosures and supporting evidence: [INSERT PRECISE DOCUMENT REFERENCES]

Please note that this is a draft for solicitor review. No application or response has been submitted.

Yours faithfully,
[Authorised fee earner / firm signature]"""},
 'security-consent':{
  'subject':'$reference: prior chargeholder consent / charge ranking',
  'body':"""Dear Colleagues,

Re: $property

We act in the above transaction. Please confirm whether the proposed additional charge is permitted under the existing security and what formal consent, restriction compliance or priority deed is required.

The following points remain under review:

$issues

Please supply any applicable lender-approved consent or deed requirements in writing.

Kind regards,
[Authorised fee earner / firm signature]"""},
 'postcompletion-chaser':{
  'subject':'$reference: post-completion registration outstanding items',
  'body':"""Dear Colleagues,

Re: $property

We are reviewing the outstanding post-completion position and would be grateful if you would respond to the matters below with the supporting evidence:

$issues

We will update the registration record after checking the actual application, receipt, requisitions and official copies.

Kind regards,
[Authorised fee earner / firm signature]"""},
 'redemption-statement':{
  'subject':'$reference: redemption statement request',
  'body':"""Dear Redemption Team,

Re: $property
Our reference: $reference

Please could you provide an up-to-date redemption statement calculated to the anticipated completion date of [INSERT ACTUAL DATE], including any daily interest, fees, discharge process and relevant payment instructions.

Please confirm the amount's validity period and any requirements for a revised statement if completion is deferred.

Kind regards,
[Authorised fee earner / firm signature]"""},
 'funds-request':{
  'subject':'$reference: completion balance and funds arrangements',
  'body':"""Dear Client,

Re: $property

We will provide a final completion statement when the purchase figures, lender advance and disbursements have been independently checked. Please do not transfer funds using bank details supplied in an unexpected email; confirm payment instructions through the firm's established independent verification procedure.

The following items remain outstanding:

$issues

Any amount or deadline must be confirmed by the authorised fee earner from the verified client ledger and final statement.

Kind regards,
[Authorised fee earner / firm signature]"""},
 'execution-clarification':{
  'subject':'$reference: executed deed / correct execution particulars',
  'body':"""Dear Colleagues,

Re: $property

Please provide the execution-ready deed with the correct legal entity and appropriate signatory/execution provisions. The following points require confirmation:

$issues

We will review the executed original against the current requirements before confirming satisfaction.

Kind regards,
[Authorised fee earner / firm signature]"""},
}


def _observed(m:dict,field:str)->str:
    vals=m.get('fact_observations',{}).get(field,[])
    if len(vals)==1:
        x=vals[0]
        return str(x.get('value','[UNCONFIRMED]'))+' [UNVERIFIED: '+str(x.get('document_id','?'))+']'
    if len(vals)>1:return '[CONFLICTING / MULTIPLE DOCUMENT VALUES: SOLICITOR TO CONFIRM]'
    return '[NOT SUPPLIED]'

def draft(matter:dict,report:dict,kind:str)->dict:
    if kind not in DRAFTS:raise MatterError('Unknown draft kind; available: '+', '.join(sorted(DRAFTS)))
    data={
        'reference':matter['matter_id'],
        'property':_observed(matter,'property_address'),
        'borrower':_observed(matter,'buyer_name'),
        'issues':'\n'.join(f"{i}. {x['title']}\n   Proposed next step: {x['suggested_action']}\n   Evidence: {', '.join(x.get('evidence_refs') or []) or '[VERIFY SOURCE]'}" for i,x in enumerate(report['issues'][:16],1)) or '[No verified outstanding list supplied; manual review required]'
    }
    t=DRAFTS[kind]
    return {'draft_type':kind,'subject':Template(t['subject']).safe_substitute(data),
            'body':Template(t['body']).safe_substitute(data),
            'status':'DRAFT ONLY – NOT APPROVED OR SENT',
            'open_issues_included':min(16,len(report['issues'])),'unlisted_issues':max(0,len(report['issues'])-16),
            'warnings':['Review legal scope, actual parties, names, references, dates and all evidence before use.',
                        'No email, certification, undertaking or filing is sent by this command.']}

def markdown_report(report:dict)->str:
    lines=[f"# Matter {report['matter_id']}: preflight review",'',
           '> DRAFT, UNSUPERVISED: not a title certificate, lender consent or completion authority.', '',
           f"Risk: **{report['risk_level']}** | Open findings: **{report['issue_count']}**",'',
           '## Findings','']
    for i,x in enumerate(report['issues'],1):
        lines.extend([f"### {i}. {x['title']} ({x['severity']})",'',
                      'Evidence: '+(', '.join(x.get('evidence_refs') or []) or 'Not supplied'),'',
                      'Action: '+x.get('suggested_action',''), ''])
    lines.extend(['## Deadlines',''])
    for d in report['deadlines']['deadlines']:
        lines.append(f"- {d['title']}: **{d['due_date'] or 'Unresolved'}**. {d['notes']}")
    lines.extend(['','## Financial reconciliation','',f"State: {report['financial_reconciliation']['state']}", '',
                  '## Approval','', 'No legal sign-off, lender instruction acceptance, funds release or registration is inferred.',''])
    return '\n'.join(lines)

def export_handoff(report:dict,outfile:str,format:str='csv')->dict:
    path=Path(outfile);path.parent.mkdir(parents=True,exist_ok=True)
    tasks=[{'matter_id':report['matter_id'],'issue_id':x['issue_id'],'action':x['action'],
            'owner':x.get('owner') or '', 'deadline':x.get('deadline') or '',
            'status':x['status'],'external_system_status':'NOT SENT'} for x in report['actions']]
    if format=='csv':
        with path.open('w',encoding='utf-8',newline='') as f:
            writer=DictWriter(f,fieldnames=['matter_id','issue_id','action','owner','deadline','status','external_system_status']);writer.writeheader();writer.writerows(tasks)
    elif format=='json':
        path.write_text(json.dumps({'format':'offline_pending_approval','system':'not_connected','tasks':tasks},indent=2)+'\n',encoding='utf-8')
    else:raise MatterError('Export format must be csv or json')
    try:os.chmod(path,0o600)
    except OSError:pass
    return {'output':str(path),'task_count':len(tasks),'integration':'file_based_manual_handoff_only','remote_updates':0,'status':'PREVIEW_NOT_UPLOADED'}

def html_dashboard(report:dict)->str:
    mid=escape(report['matter_id']);risks=escape(report['risk_level']);rows=[]
    for x in report['issues']:
        refs=escape('; '.join(x.get('evidence_refs') or []))
        rows.append('<tr><th scope="row">'+escape(x['id'])+'</th><td>'+escape(x['severity'])+'</td><td>'+escape(x['title'])+'</td><td>'+refs+'</td><td>'+escape(x['suggested_action'])+'</td></tr>')
    dates=[]
    for x in report['deadlines']['deadlines']:
        dates.append('<li>'+escape(x['title'])+': <strong>'+escape(x['due_date'] or 'UNRESOLVED')+'</strong>. '+escape(x['notes'])+'</li>')
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
      '<title>Matter '+mid+' review</title><style>body{font:1.13rem/1.55 system-ui,sans-serif;margin:auto;padding:1.2rem;max-width:80rem;color:#131313;background:#fff}'
      ':focus-visible{outline:3px solid #005fcc}table{border-collapse:collapse;width:100%}th,td{border:1px solid #444;padding:.5rem;text-align:left;vertical-align:top}'
      'th{background:#eee}caption{text-align:left;font-weight:bold}a{color:#0645ad} .warning{border-left:.35rem solid #9b3700;padding:1rem;background:#fff4e9}'
      '@media(prefers-color-scheme:dark){body{background:#161616;color:#fff}th{background:#2b2b2b}a{color:#9cd1ff}.warning{background:#43291e}}</style></head><body>'
      '<main><h1>Conveyancing preflight: '+mid+'</h1><p class="warning"><strong>NOT A LEGAL CERTIFICATION.</strong> No submissions, lender waivers or funds releases were performed.</p>'
      '<section aria-labelledby="status"><h2 id="status">Current review</h2><p>Risk: <strong>'+risks+'</strong>. Findings: <strong>'+str(report['issue_count'])+'</strong>.</p></section>'
      '<section aria-labelledby="findings"><h2 id="findings">Review findings</h2><table><caption>Evidence-linked outstanding checks</caption>'
      '<thead><tr><th scope="col">Issue</th><th scope="col">Risk</th><th scope="col">Finding</th><th scope="col">Evidence</th><th scope="col">Next action</th></tr></thead><tbody>'
      +''.join(rows)+'</tbody></table></section><section aria-labelledby="dates"><h2 id="dates">Indicative deadlines</h2><ul>'
      +''.join(dates)+'</ul></section><p>Generated '+escape(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'))+'. Review official live sources and all originals.</p></main></body></html>')
