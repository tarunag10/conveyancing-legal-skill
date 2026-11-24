"""Conservative document facts and comparisons, with exact source citations.

Extraction is candidate discovery, NEVER authentication of a deed or legal finding.
"""
from __future__ import annotations

from dataclasses import dataclass
from difflib import unified_diff
from hashlib import sha256
from pathlib import Path
from typing import Iterable
import re

from .matter_store import MatterError, timestamp

FIELD_PATTERNS = {
 'title_number': [r'(?im)\b(?:title\s*(?:number|no\.?))\s*[:#\-]?\s*([A-Z]{1,4}\s?\d{3,8})\b'],
 'company_number': [r'(?im)\b(?:company\s*(?:registration\s*)?(?:number|no\.?|reg(?:istration)?\s*no\.?))\s*[:#\-]?\s*([A-Z]{0,2}\d{6,8})\b'],
 'purchase_price': [r'(?im)\b(?:purchase\s*price|consideration)\s*[:=]?\s*(?:£|GBP\s*)([\d,]+(?:\.\d{2})?)'],
 'loan_amount': [r'(?im)\b(?:gross\s*loan|loan\s*amount|facility\s*amount|mortgage\s*advance)\s*[:=]?\s*(?:£|GBP\s*)([\d,]+(?:\.\d{2})?)'],
 'completion_date': [r'(?im)\b(?:contractual\s*)?completion\s*date\s*[:=]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{4}-\d{2}-\d{2})'],
 'mortgage_reference': [r'(?im)\b(?:mortgage|facility)\s*(?:account\s*)?reference\s*[:#]?\s*([A-Z0-9/\-]{5,30})'],
}
CONDITION_PATTERN = re.compile(r"(?im)\b(?:the (?:solicitor|conveyancer) must|solicitors? (?:must|shall|to) (?:provide|confirm|obtain|send|submit|ensure)|\bwe require\b|\bprior to (?:drawdown|release|completion)\b|\bcondition precedent\b|\byou must (?:provide|obtain|confirm|ensure|submit)\b|\bplease provide\b)" )

NAME_PATTERNS = {
 'buyer_name': [r'(?im)^\s*(?:buyer|purchaser|transferee|borrower)\s*:\s*([^\n\r]{3,140})'],
 'seller_name': [r'(?im)^\s*(?:seller|vendor|transferor)\s*:\s*([^\n\r]{3,140})'],
 'lender_name': [r'(?im)^\s*lender\s*:\s*([^\n\r]{3,140})'],
 'property_address': [r'(?im)^\s*(?:property(?:\s*address)?|security\s*address)\s*:\s*([^\n\r]{8,180})'],
}

@dataclass(frozen=True)
class Page:
    number: int
    text: str

def read_pages(path: str|Path) -> list[Page]:
    f=Path(path)
    if not f.is_file() or f.stat().st_size>25*1024*1024:
        raise MatterError('Document missing or exceeds 25MB manual inspection limit')
    ext=f.suffix.lower()
    if ext in ('.txt','.md','.csv'):
        return [Page(1,f.read_text(encoding='utf-8-sig'))]
    if ext=='.pdf':
        try: from pypdf import PdfReader
        except ImportError as e: raise MatterError('Install optional pypdf to inspect PDF; do not assume scans were read') from e
        pdf=PdfReader(str(f),strict=False)
        if pdf.is_encrypted:raise MatterError('Encrypted PDF: request authorised readable copy')
        if len(pdf.pages)>250: raise MatterError('PDF exceeds 250-page processing limit; divide and review')
        return [Page(i+1,(p.extract_text() or '')) for i,p in enumerate(pdf.pages)]
    if ext=='.docx':
        try:from docx import Document
        except ImportError as e:raise MatterError('Install optional python-docx to inspect Word; do not assume document was read') from e
        document=Document(str(f))
        lines=[p.text for p in document.paragraphs if p.text.strip()]
        for table in document.tables:
            for row in table.rows:
                lines.append(' | '.join(cell.text.strip() for cell in row.cells))
        return [Page(1,'\n'.join(lines))]  # Word page numbers are not preserved by parsing
    raise MatterError('Supported document types for conservative extraction: PDF, DOCX, TXT, MD, CSV')

def detect_candidates(pages: Iterable[Page], document_id: str) -> list[dict]:
    out=[]
    for page in pages:
        for field,patterns in {**FIELD_PATTERNS,**NAME_PATTERNS}.items():
            for pat in patterns:
                for match in re.finditer(pat,page.text):
                    val=' '.join(match.group(1).strip().split())
                    if len(val)>200 or len(val)<2:continue
                    line=page.text.count('\n',0,match.start())+1
                    observation={
                        'field':field,'value':val,'document_id':document_id,
                        'locator':f'page {page.number}, text line {line}' if page.number else f'line {line}',
                        'verification':'unverified_extraction_candidate',
                        'recorded_at':timestamp(),
                    }
                    if observation not in out:out.append(observation)
    return out[:200]

def lender_condition_candidates(pages: Iterable[Page], document_id:str) -> list[dict]:
    """Return candidate clauses from supplied text; no legal completeness or requirement status."""
    results=[];seen=set()
    for page in pages:
        for line_no,line in enumerate(page.text.splitlines(),1):
            raw=' '.join(line.strip().split())
            if not raw or not CONDITION_PATTERN.search(raw):continue
            short=raw[:440];key=short.casefold()
            if key in seen:continue
            seen.add(key)
            results.append({'candidate_id':f'{document_id}-COND-{len(results)+1}',
                'source_document_id':document_id,'source_locator':f'page {page.number}, text line {line_no}',
                'text':short,'status':'untriaged_unverified','source_text_truncated':len(raw)>440,
                'review_required':'Compare complete original provision, offer conditions and lender instructions; do not assume text completeness.'})
            if len(results)>=100:return results
    return results

def scan_document(path:str|Path, document_id:str, document_type:str='other') -> tuple[dict,list[dict]]:
    f=Path(path)
    pages=read_pages(f)
    candidates=detect_candidates(pages, document_id)
    blank=[p.number for p in pages if not p.text.strip()]
    sha=sha256(f.read_bytes()).hexdigest()
    record={'document_id':document_id,'document_type':document_type,'file_name':f.name,
            'local_path':str(f.resolve()),'sha256':sha,'pages_or_sections':len(pages),
            'received_at':timestamp(),'review_state':'unreviewed',
            'extraction_warning':('No readable text on '+str(len(blank))+' page(s); review scanned originals' if blank else 'Text extracted only; execution, signatures, plans, colours and authenticity unverified')}
    return record,candidates

def ingest_into(matter:dict,path:str|Path,document_id:str,document_type:str='other')->dict:
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{1,60}',document_id):
        raise MatterError('Invalid document ID')
    if any(d.get('document_id')==document_id for d in matter.get('documents',[])):
        raise MatterError('Document ID already exists; use a new version ID')
    rec,candidates=scan_document(path,document_id,document_type)
    conditions=lender_condition_candidates(read_pages(path),document_id) if document_type in ('lender_offer','lender_instructions','facility_agreement','mortgage_offer') else []
    if any(d.get('sha256')==rec['sha256'] for d in matter.get('documents',[])):
        raise MatterError('File already in register under another ID; do not duplicate silently')
    matter.setdefault('documents',[]).append(rec)
    for obs in candidates:matter.setdefault('fact_observations',{}).setdefault(obs['field'],[]).append(obs)
    matter.setdefault('lender_condition_candidates',[]).extend(conditions)
    matter.setdefault('events',[]).append({'at':timestamp(),'event':'document_ingested','document_id':document_id,'status':'candidate_only'})
    return {'document':rec,'extracted_candidates':len(candidates),'candidate_fields':sorted({x['field'] for x in candidates}),'lender_condition_candidates':len(conditions)}

def normalize(field:str,value) -> str:
    s=' '.join(str(value).strip().split()).casefold()
    if field in ('title_number','company_number'):return re.sub(r'[^a-z0-9]','',s)
    if field.endswith('_date'):return s.replace('/','-')
    if field in ('loan_amount','purchase_price'):return s.replace(',','').replace('£','').removesuffix('.00')
    return s

def contradictions(matter:dict)->list[dict]:
    result=[]
    for field,items in matter.get('fact_observations',{}).items():
        if not isinstance(items,list):continue
        vals={}
        for o in items:
            if not isinstance(o,dict) or not o.get('value'):continue
            n=normalize(field,o['value'])
            vals.setdefault(n,[]).append({'value':o['value'],'document_id':o.get('document_id'),'locator':o.get('locator'),'verification':o.get('verification','unverified')})
        if len(vals)>1:
            result.append({'type':'fact_conflict','field':field,'severity':'high' if field in ('title_number','buyer_name','seller_name','company_number','loan_amount','purchase_price') else 'medium',
                           'variants':list(vals.values()),'action':'Check each original and resolve with actual parties/lender; do not silently select one value.'})
    return result

def compare_text_files(files: list[str],max_diff_lines:int=180)->dict:
    if len(files)!=2:raise MatterError('Document comparison needs exactly two paths')
    a,b=[read_pages(f) for f in files]
    txt=['\n'.join(p.text for p in pages) for pages in (a,b)]
    lines=list(unified_diff(txt[0].splitlines(),txt[1].splitlines(),fromfile=Path(files[0]).name,tofile=Path(files[1]).name,lineterm=''))
    vals=[detect_candidates(p, 'OLD' if i==0 else 'NEW') for i,p in enumerate((a,b))]
    def grouped(lst):
        out={}
        for c in lst:out.setdefault(c['field'],set()).add(normalize(c['field'],c['value']))
        return out
    old,new=map(grouped,vals)
    changes=[]
    for field in sorted(set(old)|set(new)):
        if old.get(field)!=new.get(field):
            changes.append({'field':field,'old_candidates':sorted(old.get(field,[])),'new_candidates':sorted(new.get(field,[])),
                            'status':'possible_change_requires_original_review'})
    return {'file_names':[Path(p).name for p in files], 'changed_candidate_fields':changes,
            'text_diff':lines[:max_diff_lines],'diff_truncated':len(lines)>max_diff_lines,
            'requires_visual_comparison':True,'legal_effect':'NOT DETERMINED: compare full originals, signature panels, formatting, schedules and any scanned pages.'}
