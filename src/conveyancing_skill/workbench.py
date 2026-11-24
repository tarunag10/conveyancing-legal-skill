"""Matter-aware conveyancing workbench CLI.

Usage: python -m conveyancing_skill.workbench --help
All remote side effects are deliberately disabled: draft/preview/export only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from .matter_store import MatterError, new_matter, read_matter, validate_matter, write_matter, verify_audit, timestamp
from .matter_intelligence import ingest_into, compare_text_files
from .matter_rules import review, deadlines, lender_lookup, AUTHORITIES, accounting
from .matter_outputs import draft, export_handoff, html_dashboard, markdown_report, DRAFTS
from .matter_lifecycle import security_map, requisitions, post_completion, form_preflight


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def lender_data():
    module=Path(__file__).resolve()
    for root in (module.parents[2],module.parent/'data'):
        candidate=root/'knowledge/lenders/lender-directory.json'
        if candidate.is_file():return read_json(candidate)
    return {'lenders':[], 'research_as_of':None, 'warning':'Lender index not installed; verify source packaging.'}

def save_output(value,output:str|None,kind='json'):
    data=(json.dumps(value,indent=2,ensure_ascii=False,sort_keys=True)+'\n') if kind=='json' else value
    if output:
        f=Path(output);f.parent.mkdir(parents=True,exist_ok=True)
        f.write_text(data,encoding='utf-8')
        try:f.chmod(0o600)
        except OSError:pass
        return {'written':str(f),'kind':kind,'status':'LOCAL OUTPUT ONLY'}
    if kind=='html':return {'html':data,'status':'NOT HOSTED'}
    if kind=='markdown':return {'markdown':data}
    return value

def merge_manual(m:dict,updates:dict)->dict:
    allowed={'roles','requirements','securities','dates','financials','registration','execution','specialist','lender','post_completion'}
    notallowed=set(updates)-allowed
    if notallowed:raise MatterError('Disallowed fields in manual patch: '+', '.join(sorted(notallowed)))
    for k,v in updates.items():
        if k=='roles' and not isinstance(v,list):raise MatterError('roles must be a list')
        if k in ('requirements','securities','execution') and not isinstance(v,list):raise MatterError(k+' must be an array')
        if k in ('dates','financials','registration','specialist','lender','post_completion') and not isinstance(v,dict):raise MatterError(k+' must be an object')
        m[k]=v
    m.setdefault('events',[]).append({'at':timestamp(),'event':'manual_data_patch','fields':sorted(updates),'status':'unverified_input_requires_solicitor_review'})
    return m

def obs_add(m:dict,field:str,value:str,document_id:str,locator:str)->dict:
    if not any(x.get('document_id')==document_id for x in m['documents']):
        raise MatterError('Observation must cite an existing document ID')
    if not field or len(field)>80 or not all(x.isalnum() or x=='_' for x in field):raise MatterError('Invalid field')
    if not value or len(value)>400:raise MatterError('Observation value must be supplied (max 400 characters)')
    if not locator:raise MatterError('Observation requires page, clause or section locator')
    m.setdefault('fact_observations',{}).setdefault(field,[]).append({'field':field,'value':value,
      'document_id':document_id,'locator':locator,'verification':'manually_recorded_not_independently_verified','recorded_at':timestamp()})
    return m

def build_parser():
    p=argparse.ArgumentParser(prog='conveyancing-workbench',description='Local solicitor-supervised conveyancing matter engine; NEVER signs, files, sends or releases funds.')
    sub=p.add_subparsers(dest='command',required=True)
    q=sub.add_parser('init',help='Create a pseudonymous private matter JSON and chained audit')
    q.add_argument('file');q.add_argument('--matter-id',required=True);q.add_argument('--jurisdiction',required=True,choices=['England','Wales']);q.add_argument('--transaction-type',required=True)
    q=sub.add_parser('add-document',help='Read PDF/DOCX/TXT/MD and append candidate evidence')
    q.add_argument('matter');q.add_argument('document');q.add_argument('--id',required=True);q.add_argument('--type',default='other')
    q=sub.add_parser('add-observation',help='Append source-located, unverified matter fact')
    q.add_argument('matter');q.add_argument('--field',required=True);q.add_argument('--value',required=True);q.add_argument('--document-id',required=True);q.add_argument('--locator',required=True)
    q=sub.add_parser('update-data',help='Apply a controlled manual factual patch, never lawyer approval')
    q.add_argument('matter');q.add_argument('--patch',required=True)
    for key in ('review','deadlines','accounting','security-map','form-preflight'):
        q=sub.add_parser(key);q.add_argument('matter');q.add_argument('--output')
    q=sub.add_parser('post-completion');q.add_argument('matter');q.add_argument('--as-of');q.add_argument('--output')
    q=sub.add_parser('requisitions');q.add_argument('matter');q.add_argument('--as-of');q.add_argument('--output')
    q=sub.add_parser('compare');q.add_argument('old_document');q.add_argument('new_document');q.add_argument('--output')
    q=sub.add_parser('lender');q.add_argument('name');q.add_argument('--output')
    q=sub.add_parser('draft');q.add_argument('matter');q.add_argument('--kind',required=True,choices=sorted(DRAFTS));q.add_argument('--output')
    q=sub.add_parser('report-md');q.add_argument('matter');q.add_argument('--output')
    q=sub.add_parser('dashboard');q.add_argument('matter');q.add_argument('--output',required=True)
    q=sub.add_parser('handoff');q.add_argument('matter');q.add_argument('--output',required=True);q.add_argument('--format',choices=['csv','json'],default='csv')
    q=sub.add_parser('audit');q.add_argument('matter')
    q=sub.add_parser('validate');q.add_argument('matter',nargs='?')
    return p

def main(argv=None):
    args=build_parser().parse_args(argv)
    try:
        action=args.command
        if action=='init':
            result=write_matter(args.file,new_matter(args.matter_id,args.jurisdiction,args.transaction_type),'matter_created')
        elif action=='add-document':
            m=read_matter(args.matter);result=ingest_into(m,args.document,args.id,args.type)
            result={'ingestion':result,'save':write_matter(args.matter,m,'source_added',{'document_id':args.id})}
        elif action=='add-observation':
            m=read_matter(args.matter)
            obs_add(m,args.field,args.value,args.document_id,args.locator)
            result=write_matter(args.matter,m,'observation_added',{'field':args.field,'document_id':args.document_id})
        elif action=='update-data':
            m=read_matter(args.matter);patch=read_json(args.patch)
            result=write_matter(args.matter,merge_manual(m,patch),'manual_data_patch',{'fields':sorted(patch)})
        elif action=='compare':result=save_output(compare_text_files([args.old_document,args.new_document]),args.output)
        elif action=='lender':result=save_output(lender_lookup(args.name,lender_data()),args.output)
        elif action=='audit':result=verify_audit(args.matter)
        elif action=='validate':
            d=lender_data();lenders=d.get('lenders',[])
            result={'status':'PASS','lender_directory_entries':len(lenders),'verified_lender_snapshot':d.get('research_as_of'),
                    'legal_authorities':AUTHORITIES,'disclaimers':['No live lawyer approval, legal rule effect or lender route verified by this structural check.']}
            if args.matter:
                m=read_matter(args.matter);result['matter_errors']=validate_matter(m)
                result['audit']=verify_audit(args.matter)
                if result['matter_errors'] or not result['audit'].get('valid'):result['status']='FAIL'
        else:
            m=read_matter(args.matter);lr=lender_data()
            if action=='review': result=save_output(review(m,lr),args.output)
            elif action=='deadlines':
                matches=lender_lookup(m.get('lender',{}).get('name',''),lr).get('matches',[])
                result=save_output(deadlines(m,matches[0] if len(matches)==1 else None),args.output)
            elif action=='accounting':result=save_output(accounting(m),args.output)
            elif action=='security-map':result=save_output(security_map(m),args.output)
            elif action=='form-preflight':result=save_output(form_preflight(m),args.output)
            elif action=='requisitions':result=save_output(requisitions(m,args.as_of),args.output)
            elif action=='post-completion':
                matches=lender_lookup(m.get('lender',{}).get('name',''),lr).get('matches',[])
                result=save_output(post_completion(m,args.as_of,matches[0] if len(matches)==1 else None),args.output)
            elif action=='draft':result=save_output(draft(m,review(m,lr),args.kind),args.output)
            elif action=='report-md':result=save_output(markdown_report(review(m,lr)),args.output,'markdown')
            elif action=='dashboard':result=save_output(html_dashboard(review(m,lr)),args.output,'html')
            elif action=='handoff':result=export_handoff(review(m,lr),args.output,args.format)
            else:raise MatterError('Unsupported command')
        print(json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True))
        return 1 if isinstance(result,dict) and result.get('status')=='FAIL' else 0
    except (MatterError,OSError,ValueError,TypeError,ImportError) as e:
        print(json.dumps({'status':'REFUSED_UNVERIFIED_OR_INVALID','error':str(e)},indent=2),file=sys.stderr)
        return 2

if __name__=='__main__':sys.exit(main())
