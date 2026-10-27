"""Command line entrypoint with no implicit network or irreversible legal actions."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from datetime import date
from . import __version__
from .engine import ROOT, LegalReviewRequired, completion, forms, load, review_matter, statutory_deadline, tax_estimate, workflow
from .extract import extract_document
from .source_watch import watch


def validate() -> dict:
    errors=[]; warnings=[]
    expected=['SKILL.md','core/OPERATING_STANDARD.md','core/EVIDENCE_AND_RISK.md','core/SOURCE_POLICY.md','knowledge/forms/catalogue.json','knowledge/legislation/source-index.json','knowledge/legislation/rules.json','knowledge/legislation/tax-rates.json','knowledge/workflows/stages.json','knowledge/workflows/profiles.json','plugin.json','AGENTS.md','CLAUDE.md','GEMINI.md','.cursor/rules/conveyancing.mdc','.agents/skills/conveyancing-legal/SKILL.md','.claude/skills/conveyancing-legal/SKILL.md','.gemini/skills/conveyancing-legal/SKILL.md','skills/conveyancing-legal/SKILL.md','README.md','docs/VALIDATION_AND_LIMITATIONS.md']
    for s in expected:
        path=ROOT/s
        if not path.is_file() or not path.stat().st_size:errors.append(f'Missing or empty: {s}')
    f=load('knowledge/forms/catalogue.json'); sources=load('knowledge/legislation/source-index.json');rules=load('knowledge/legislation/rules.json');stages=load('knowledge/workflows/stages.json');profiles=load('knowledge/workflows/profiles.json')
    src_ids=[s['id'] for s in sources]
    if len(src_ids)!=len(set(src_ids)):errors.append('Duplicate source IDs')
    for s in sources:
        if not s.get('url','').startswith('https://'):errors.append(f'Non-HTTPS source: {s["id"]}')
        for prop in ('authority_type','jurisdiction','last_verified_date','verification_status','scope_note'):
            if not s.get(prop): errors.append(f'Incomplete source {s["id"]}: {prop}')
        try:date.fromisoformat(s['last_verified_date'])
        except ValueError:errors.append(f'Invalid source date: {s["id"]}')
    codes=[x['code'] for x in f]
    if len(codes)!=len(set(codes)):errors.append('Duplicate form codes')
    for x in f:
        for prop in ('code','official_title','issuer','purpose','official_catalogue_url','status'):
            if not x.get(prop):errors.append(f'Incomplete form {x.get("code")}: {prop}')
        if x['status'] not in ('edition_or_provenance_requires_verification','pending_verification') and not x.get('publisher_date_last_checked'):
            errors.append(f'Publisher listing date missing for claimed-checked form: {x["code"]}')
        if x['file_revision_verified'] and not x['official_download_link']:
            errors.append(f'Claimed verified version without binary link: {x["code"]}')
    for r in rules:
        for prop in ('id','authority_type','jurisdiction','effective_date','last_verified_date','verification_status'):
            if prop not in r:errors.append(f'Rule missing field: {r.get("id")}: {prop}')
        for ref in [r.get('source_id')] if r.get('source_id') else []:
            if ref not in src_ids:errors.append(f'Rule {r["id"]} references unknown source {ref}')
    pids=[p['id'] for p in profiles]
    if len(pids)!=len(set(pids)):errors.append('Duplicate profiles')
    stids=[x['id'] for x in stages]
    if len(stids)!=len(set(stids)):errors.append('Duplicate stage IDs')
    for profile in profiles:
        for stage in profile.get('additional_stages',[]):
            if stage not in stids:warnings.append(f'Profile {profile["id"]} has external stage: {stage}')
    for s in stages:
        for dep in s['dependencies']:
            if dep not in stids:errors.append(f'Unknown stage dependency: {s["id"]}: {dep}')
        if s['default_status']!='outstanding':errors.append(f'Unproven stage is marked complete: {s["id"]}')
    raw=(ROOT/'SKILL.md').read_text(encoding='utf-8')
    if not raw.startswith('---\n') or '\nname: conveyancing-legal\n' not in raw:errors.append('Canonical SKILL.md frontmatter invalid')
    for rel, up in [('.agents/skills/conveyancing-legal/SKILL.md','../../../SKILL.md'),('.claude/skills/conveyancing-legal/SKILL.md','../../../SKILL.md'),('.gemini/skills/conveyancing-legal/SKILL.md','../../../SKILL.md'),('skills/conveyancing-legal/SKILL.md','../../SKILL.md')]:
        path=ROOT/rel
        if path.is_file():
            if up not in path.read_text(encoding='utf8'):
                errors.append(f'Adapter does not reference canonical skill: {rel}')
            if not (path.parent/up).resolve().samefile(ROOT/'SKILL.md'):
                errors.append(f'Adapter root reference does not resolve: {rel}')
    plugin=load('plugin.json')
    if not plugin.get('$schema','').startswith('https://agent-plugins.org/'):
        errors.append('Portable plugin manifest schema missing')
    if not (ROOT/'skills/setup/SKILL.md').is_file():errors.append('OpenAI onboarding skill missing')
    if any(x.get('file_revision_verified') for x in f):warnings.append('Some forms marked verified; confirm binary hashes and licensing manually')
    if not errors:
        warnings.append('Automated validation does not verify individual legal propositions, signed originals, lender Part 2 or actual form file revisions')
    return {'status':'PASS' if not errors else 'FAIL','errors':errors,'warnings':warnings,'counts':{'sources':len(sources),'rules':len(rules),'forms':len(f),'stages':len(stages),'profiles':len(profiles)},'version':__version__}


def main(argv=None):
    parser=argparse.ArgumentParser(prog='conveyancing',description='Evidence-gated England & Wales conveyancing tools; not legal sign-off')
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('validate')
    p=sub.add_parser('forms');p.add_argument('query')
    p=sub.add_parser('workflow');p.add_argument('profile',nargs='?');p.add_argument('--list',action='store_true')
    p=sub.add_parser('review');p.add_argument('file')
    p=sub.add_parser('completion');p.add_argument('file')
    p=sub.add_parser('tax-estimate');p.add_argument('--jurisdiction',choices=['england','wales'],required=True);p.add_argument('--price',required=True);p.add_argument('--as-of',required=True);p.add_argument('--additional',action='store_true');p.add_argument('--acknowledge-simple',action='store_true');p.add_argument('--complexity',action='append',default=[])
    p=sub.add_parser('deadline');p.add_argument('type');p.add_argument('event_date');p.add_argument('--holidays')
    p=sub.add_parser('extract');p.add_argument('file');p.add_argument('--output')
    p=sub.add_parser('lender-checklist');p.add_argument('file')
    p=sub.add_parser('compare-documents');p.add_argument('files',nargs='+')
    p=sub.add_parser('source-watch');p.add_argument('--allow-network',action='store_true');p.add_argument('--limit',type=int,default=12);p.add_argument('--baseline');p.add_argument('--baseline-out');p.add_argument('--fail-on-change',action='store_true');p.add_argument('--output')
    p=sub.add_parser('to-docx');p.add_argument('input');p.add_argument('output')
    p=sub.add_parser('fill-docx');p.add_argument('input');p.add_argument('output');p.add_argument('--data',required=True);p.add_argument('--log',required=True)
    args=parser.parse_args(argv)
    try:
        if args.command=='validate':result=validate()
        elif args.command=='forms':result=forms(args.query)
        elif args.command=='workflow':result=load('knowledge/workflows/profiles.json') if args.list else workflow(args.profile or '')
        elif args.command in ('review','completion'):
            j=json.loads(Path(args.file).read_text(encoding='utf-8'))
            result=review_matter(j) if args.command=='review' else completion(j)
        elif args.command=='tax-estimate':result=tax_estimate(args.jurisdiction,args.price,args.as_of,args.additional,acknowledge_simple=args.acknowledge_simple,complexity_flags=args.complexity)
        elif args.command=='deadline':
            holidays=json.loads(Path(args.holidays).read_text(encoding='utf-8')) if args.holidays else None
            result=statutory_deadline(args.type,args.event_date,holidays)
        elif args.command=='extract':result=extract_document(args.file)
        elif args.command=='lender-checklist':
            from .intelligence import lender_candidates
            result=lender_candidates(args.file)
        elif args.command=='compare-documents':
            from .intelligence import compare_document_candidates
            result=compare_document_candidates(args.files)
        elif args.command=='source-watch':
            base=json.loads(Path(args.baseline).read_text(encoding='utf8')) if args.baseline else None
            result=watch(allow_network=args.allow_network,baseline=base,limit=args.limit)
        elif args.command=='to-docx':
            from .documents import to_docx
            result=to_docx(args.input,args.output)
        elif args.command=='fill-docx':
            from .documents import fill_placeholders
            data=json.loads(Path(args.data).read_text(encoding='utf8'))
            result=fill_placeholders(args.input,args.output,data.get('values',{}),allowed=data.get('allowed_fields',[]),source_refs=data.get('source_refs',{}))
            Path(args.log).write_text(json.dumps(result,indent=2),encoding='utf8')
        else:raise LegalReviewRequired('Unsupported command')
        output=json.dumps(result,ensure_ascii=False,indent=2)
        filename=getattr(args,'output',None)
        if args.command in ('extract','source-watch') and filename:
            Path(filename).parent.mkdir(parents=True,exist_ok=True)
            Path(filename).write_text(output+'\n',encoding='utf8')
            print(f'Wrote {filename}')
        else:print(output)
        if args.command=='source-watch':
            if args.baseline_out:
                fresh=dict(base or {})
                for row in result['sources']:
                    if row.get('sha256') and row.get('status') in ('fetched','change_detected_review_required'):
                        fresh[row['source_id']]=row['sha256']
                output_path=Path(args.baseline_out);output_path.parent.mkdir(parents=True,exist_ok=True)
                output_path.write_text(json.dumps(fresh,indent=2,sort_keys=True)+'\n',encoding='utf8')
            if args.fail_on_change and result['legal_review_queue']:
                print('PUBLIC SOURCE CONTENT CHANGED: specialist review required; see source-watch output',file=sys.stderr)
                return 3
        return 1 if isinstance(result,dict) and result.get('status')=='FAIL' else 0
    except (LegalReviewRequired,FileNotFoundError,ValueError,PermissionError) as exc:
        print(json.dumps({'error':str(exc),'status':'REFUSED_UNVERIFIED_OR_INVALID'},indent=2),file=sys.stderr)
        return 2

if __name__=='__main__':sys.exit(main())
