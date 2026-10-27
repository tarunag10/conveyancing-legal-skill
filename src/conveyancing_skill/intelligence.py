"""Conservative document candidate extraction.

No heuristic output is a verified legal fact or exhaustive conditions list.
"""
from __future__ import annotations
import re
from pathlib import Path
from .extract import extract_document
from .engine import LegalReviewRequired

CLAUSE_PATTERNS=(
    re.compile(r'\b(?:you\s+must|you\s+are\s+required|the\s+borrower\s+(?:must|shall)|we\s+require|please\s+(?:provide|confirm|obtain|send)|as\s+a\s+condition\s+of|prior\s+to\s+(?:drawdown|completion)|before\s+completion|subject\s+to)\b',re.I),
    re.compile(r'\b(?:certificate\s+of\s+title|independent\s+legal\s+advice|proof\s+of\s+funds|building\s+insurance|redemption\s+statement)\b',re.I),
)

def lender_candidates(filename: str):
    doc=extract_document(filename)
    results=[]
    for element in doc['elements']:
        content=element['text']
        if any(p.search(content) for p in CLAUSE_PATTERNS):
            results.append({'id':f'LC-{len(results)+1:03}',
                'verbatim_extracted_text':content[:2000],
                'source_document_id':doc['document_id'],
                'source_filename':doc['file_name'],
                'source_locator':element['location'],
                'evidence_status':'EXTRACTED UNCHECKED',
                'legal_completeness':'NOT_ASSESSED',
                'condition_type':'UNCLASSIFIED',
                'completion_blocker':'UNDETERMINED',
                'required_action':'Compare original and exact lender Part 1/2/bespoke conditions, verify whether mandatory, identify deadline and get evidence or lender waiver'})
    return {'source_filename':doc['file_name'],'source_id':doc['document_id'],
        'candidate_requirements':results,'possible_extraction_gaps':doc['warnings'],
        'caution':'KEYWORD EXTRACTION ONLY; may omit decisive conditions in tables, images or unobvious wording. Not an exhaustive lender checklist; manual clause-by-clause review mandatory.'}


def compare_document_candidates(files: list[str]):
    if not files:raise LegalReviewRequired('At least one document is required')
    if len(files)>20:raise LegalReviewRequired('Document batch limit 20; split into smaller matter batches')
    documents=[extract_document(p) for p in files]
    groups={}
    for x in documents:
        for number in x['potential_title_numbers_NOT_VERIFIED']:
            groups.setdefault(number,[]).append(x['file_name'])
    multiple=len(groups)>1
    return {'documents':[{'filename':d['file_name'],'document_id':d['document_id'],'title_candidates':d['potential_title_numbers_NOT_VERIFIED'],'warnings':d['warnings']} for d in documents],
        'all_title_number_candidates':groups,
        'different_title_candidates_detected':multiple,
        'issues_to_check':(['Multiple potential title identifiers detected. These MAY identify legitimate related freehold/leasehold titles: verify every official register and actual transfer interest.'] if multiple else []) + ['Compare exact parties, deed/contract dates, charges, addresses, leases and figures against the actual documents and source page. No automated sign-off.'],
        'caution':'Pattern matches are NOT authenticated title numbers and absence of a match does not mean a deed is silent.'}
