"""Private, local, evidence-led matter records. No remote I/O or approval actions.

Matter records are references and observations, not a case-management system.
A tamper-evident JSONL audit detects accidental edits, not privileged tampering.
"""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import os
import re
import tempfile

SCHEMA_VERSION = '1.0.0'
SENSITIVE_KEYS = {'password','token','secret','account_number','sort_code','iban','bank_details'}
ALLOWED_JURISDICTIONS = {'England','Wales'}

class MatterError(ValueError):
    pass

def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')

def canonical(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')

def digest(obj) -> str:
    return sha256(canonical(obj)).hexdigest()

def safe_id(value: str) -> str:
    if not isinstance(value,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{2,79}', value):
        raise MatterError('Use a pseudonymous matter ID of 3-80 characters (letters, numbers, . _ -).')
    return value

def new_matter(matter_id: str, jurisdiction: str, transaction_type: str) -> dict:
    safe_id(matter_id)
    if jurisdiction not in ALLOWED_JURISDICTIONS:
        raise MatterError('Jurisdiction must be England or Wales')
    if not isinstance(transaction_type,str) or not transaction_type.strip():
        raise MatterError('Transaction type required')
    return {
        'schema_version': SCHEMA_VERSION,
        'matter_id': matter_id,
        'jurisdiction': jurisdiction,
        'transaction_type': transaction_type.strip(),
        'created_at': timestamp(),
        'roles': [],
        'documents': [],
        'fact_observations': {},
        'requirements': [],
        'lender_condition_candidates': [],
        'securities': [],
        'events': [],
        'dates': {},
        'financials': {},
        'registration': {},
        'execution': [],
        'specialist': {},
        'lender': {},
        'review': {'decision': 'pending', 'reviewer': None, 'reviewed_at': None},
        'external_actions': [],
        'warnings': ['Use only firm-approved storage; no encryption or access management is supplied by this package.'],
    }

def validate_matter(m: dict) -> list[str]:
    errors = []
    if not isinstance(m, dict): return ['Matter must be a JSON object']
    try: safe_id(m.get('matter_id'))
    except MatterError as exc: errors.append(str(exc))
    if m.get('jurisdiction') not in ALLOWED_JURISDICTIONS: errors.append('Unsupported jurisdiction')
    for key in ('documents','requirements','lender_condition_candidates','securities','events','execution'):
        if not isinstance(m.get(key,[]), list): errors.append(f'{key} must be an array')
    if not isinstance(m.get('fact_observations', {}),dict): errors.append('fact_observations must be an object')
    docs=m.get('documents', [])
    if isinstance(docs,list):
        docids=[x.get('document_id') for x in docs if isinstance(x,dict)]
        if len(docids)!=len(set(docids)): errors.append('Duplicate document IDs')
    req=m.get('requirements', [])
    if isinstance(req,list):
        ids=[x.get('id') for x in req if isinstance(x,dict)]
        if len(ids)!=len(set(ids)): errors.append('Duplicate requirement IDs')
    secs=m.get('securities',[])
    if isinstance(secs,list):
        ids=[x.get('id') for x in secs if isinstance(x,dict)]
        if len(ids)!=len(set(ids)): errors.append('Duplicate security IDs')
    for k in SENSITIVE_KEYS:
        if k in m: errors.append(f'Unexpected sensitive root field: {k}')
    return errors

def read_matter(path: str|Path) -> dict:
    file=Path(path)
    m=json.loads(file.read_text(encoding='utf-8'))
    issues=validate_matter(m)
    if issues: raise MatterError('; '.join(issues))
    return m

def audit_path(path: str|Path) -> Path:
    file=Path(path)
    return file.with_name(file.name + '.audit.jsonl')

def append_audit(path: str|Path, action: str, old_hash: str|None, new_hash: str, detail: dict|None=None) -> dict:
    af=audit_path(path)
    prior=[]
    if af.exists():
        prior=[json.loads(s) for s in af.read_text(encoding='utf-8').splitlines() if s.strip()]
        if not verify_audit(path, check_current=False)['valid']:
            raise MatterError('Audit history invalid; refusing write')
    prev=prior[-1]['event_hash'] if prior else 'GENESIS'
    event={'seq':len(prior)+1,'at':timestamp(),'action':action,'prev_hash':prev,'old_matter_hash':old_hash,
           'new_matter_hash':new_hash,'detail':detail or {}}
    event['event_hash']=digest(event)
    with af.open('a',encoding='utf-8') as f:
        f.write(json.dumps(event,ensure_ascii=False,sort_keys=True)+'\n')
        f.flush();os.fsync(f.fileno())
    try: os.chmod(af, 0o600)
    except OSError: pass
    return event

def verify_audit(path: str|Path, check_current: bool=True) -> dict:
    af=audit_path(path)
    if not af.exists(): return {'valid':False,'error':'Audit log missing','events':0}
    prev='GENESIS'; prior=None; count=0
    try:
        for s in af.read_text(encoding='utf-8').splitlines():
            if not s.strip():continue
            event=json.loads(s); count+=1
            expected=event.get('event_hash'); stripped=dict(event); stripped.pop('event_hash',None)
            if digest(stripped)!=expected or event.get('prev_hash')!=prev or event.get('seq')!=count:
                return {'valid':False,'error':f'Hash-chain mismatch at event {count}','events':count}
            if prior is not None and event.get('old_matter_hash')!=prior:
                return {'valid':False,'error':f'Matter revision mismatch at event {count}','events':count}
            prev=expected;prior=event.get('new_matter_hash')
        if check_current:
            m=json.loads(Path(path).read_text(encoding='utf-8'))
            if digest(m)!=prior: return {'valid':False,'error':'On-disk matter differs from last audited revision','events':count}
        return {'valid':count>0,'events':count,'last_matter_hash':prior,'warning':'Detects alteration, not authenticity or legal approval.'}
    except (ValueError, KeyError, OSError) as e:
        return {'valid':False,'error':str(e),'events':count}

def write_matter(path: str|Path,m:dict, action:str='revision',detail:dict|None=None) -> dict:
    issues=validate_matter(m)
    if issues:raise MatterError('; '.join(issues))
    file=Path(path)
    file.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    old_hash=None
    if file.exists():
        old=json.loads(file.read_text(encoding='utf-8'))
        old_hash=digest(old)
        if not verify_audit(file).get('valid'):
            raise MatterError('Matter audit failed: refusing overwrite')
        # A previously reviewed record must be amended through a solicitor-controlled process.
        if old.get('review',{}).get('decision') in ('approved','lawyer-approved'):
            raise MatterError('Cannot automatically overwrite a lawyer-approved matter')
    data=json.dumps(m,ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',prefix='.matter-',suffix='.json',dir=file.parent,delete=False) as f:
        temp=Path(f.name); f.write(data); f.flush(); os.fsync(f.fileno())
    try:
        os.chmod(temp,0o600)
        os.replace(temp,file)
        event=append_audit(file,action,old_hash,digest(m),detail)
        return {'path':str(file),'matter_id':m['matter_id'],'audit_event':event['seq'],'integrity':verify_audit(file)['valid']}
    finally:
        temp.unlink(missing_ok=True)
