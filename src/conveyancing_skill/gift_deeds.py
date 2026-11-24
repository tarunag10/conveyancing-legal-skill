"""Generate supervised, non-prescribed monetary Deeds of Gift for England and Wales.

This is a local drafting utility, not legal advice, signature verification,
lender acceptance, or proof of the stated facts. It deliberately does not
request, store, or output dates of birth or occupations. It never signs or
pre-dates a deed and never overwrites an existing file.

Use: conveyancing-gift-deeds --input /approved/private/data.json --output-dir /approved/private/output
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from .engine import ROOT, LegalReviewRequired

TEMPLATE = ROOT / 'templates' / 'DEED_OF_GIFT_TEMPLATE.docx'
DOTTED_SHORT = '.' * 39
DOTTED_LONG = '.' * 65
MAX_AMOUNT = Decimal('999999999.99')

_ONES = ('zero','one','two','three','four','five','six','seven','eight','nine',
         'ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen',
         'seventeen','eighteen','nineteen')
_TENS = ('','','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety')


def _clean(value: Any, field: str, required: bool = False) -> str:
    if value is None:
        value = ''
    if not isinstance(value, str):
        raise LegalReviewRequired(f'{field} must be text')
    value = ' '.join(value.split())
    if required and not value:
        raise LegalReviewRequired(f'Missing required {field}')
    if len(value) > 800:
        raise LegalReviewRequired(f'{field} is too long for a short deed field')
    if any(c in value for c in ('\u0000','\ufffd')):
        raise LegalReviewRequired(f'{field} includes invalid characters')
    return value


def _amount(value: Any, field: str) -> Decimal:
    if isinstance(value, bool):
        raise LegalReviewRequired(f'{field} cannot be a boolean')
    if not isinstance(value, (str,int,Decimal)):
        raise LegalReviewRequired(f'{field} must be an exact decimal/string amount')
    cleaned = str(value).replace(',','').replace('£','').strip()
    if not re.fullmatch(r'\d+(?:\.\d{1,2})?',cleaned):
        raise LegalReviewRequired(f'{field} must be a positive GBP amount with at most two decimal places')
    try: n = Decimal(cleaned)
    except (InvalidOperation,ValueError):
        raise LegalReviewRequired(f'Invalid {field}')
    if not (Decimal('0') < n <= MAX_AMOUNT):
        raise LegalReviewRequired(f'{field} must be positive and no more than £999,999,999.99')
    return n.quantize(Decimal('.01'))


def _number_words(n: int) -> str:
    if n < 20: return _ONES[n]
    if n < 100:
        return _TENS[n//10] + ('-' + _ONES[n%10] if n%10 else '')
    if n < 1000:
        return _ONES[n//100] + ' hundred' + (' and ' + _number_words(n%100) if n%100 else '')
    for base, label in ((1000000,'million'), (1000,'thousand')):
        if n >= base:
            upper, rem = divmod(n,base)
            prefix = _number_words(upper) + ' ' + label
            if not rem: return prefix
            return prefix + (' and ' if rem < 100 else ' ') + _number_words(rem)
    raise AssertionError('Unexpected amount')


def _money_words(n: Decimal) -> str:
    pounds = int(n)
    pence = int((n-Decimal(pounds))*100)
    out = _number_words(pounds) + (' pound' if pounds == 1 else ' pounds')
    if pence:
        out += ' and ' + _number_words(pence) + (' penny' if pence == 1 else ' pence')
    return out


def _gbp(n: Decimal) -> str:
    return '£' + (f'{n:,.0f}' if n == n.to_integral_value() else f'{n:,.2f}')


def _get(value: Any, key: str, field: str, required: bool=False) -> str:
    if value is None: value={}
    if not isinstance(value,dict):
        raise LegalReviewRequired(f'{field} must be a JSON object')
    return _clean(value.get(key,''),f'{field}.{key}',required)


def _donees(rows: list[dict]) -> tuple[str,str,str,str,list[str]]:
    """Return party line, collective reference, recipient phrase, subject, missing fields."""
    if not isinstance(rows,list) or not 1 <= len(rows) <= 8:
        raise LegalReviewRequired('donees must contain between one and eight recipient objects')
    people=[]; missing=[]
    for i, item in enumerate(rows,1):
        if not isinstance(item,dict): raise LegalReviewRequired(f'donees[{i}] must be an object')
        name=_get(item,'name',f'donees[{i}]',True)
        address=_get(item,'address',f'donees[{i}]')
        if not address:missing.append(f'donees[{i}].address')
        people.append((name,address or DOTTED_SHORT))
    n=len(people)
    if n==1:
        nm,addr=people[0];ident=f'{nm} of {addr} (the “Donee”).'
        return ident, 'the Donee', 'the Donee', 'The Donee intends', missing
    names=[x[0] for x in people]
    if n==2 and people[0][1]==people[1][1] and not missing:
        ident=f'{names[0]} and {names[1]}, both of {people[0][1]} (together, the “Donees”).'
    else:
        chunks=[f'{name} of {addr}' for name,addr in people]
        ident=', '.join(chunks[:-1]) + (' and ' if len(chunks)==2 else ', and ') + chunks[-1] + ' (together, the “Donees”).'
    return ident, 'the Donees', 'the Donees jointly', 'The Donees intend', missing


def _recital(transaction_type: str, subject: str, lender: Any) -> tuple[str,list[str]]:
    verb = 'to purchase' if transaction_type=='purchase' else 'to remortgage'
    text = f'{subject} {verb} the Property'
    if transaction_type == 'purchase':
        if lender:
            return text+'.', ['A lender has been supplied for a purchase; the template does not insert it into the purchase recital. Check the actual mortgage instructions.']
        return text+'.', []
    if lender is None: lender={}
    if not isinstance(lender,dict): raise LegalReviewRequired('lender must be a JSON object')
    name = _get(lender,'name','lender')
    address = _get(lender,'address','lender')
    desc = _get(lender,'loan_description','lender')
    offer_date = _get(lender,'offer_date','lender')
    offer_ref = _get(lender,'application_reference','lender')
    amount = lender.get('loan_amount')
    if not name:
        if any((address,desc,offer_date,offer_ref,amount)):
            raise LegalReviewRequired('lender.name is required when lender offer details are included')
        return text+'.', ['No lender-specific wording entered; check lender requirements and gift acceptance.']
    text += f' with {name}'
    if address: text += f' of {address}'
    text += ' (the “Lender”)'
    if any((desc,offer_date,offer_ref,amount)):
        prefix = f'{desc} mortgage offer' if desc else 'mortgage offer'
        article = 'an' if prefix[0].lower() in 'aeiou' else 'a'
        text += f', pursuant to {article} {prefix}'
        if offer_date: text += f' dated {offer_date}'
        if amount is not None and str(amount).strip():
            text += f' for {_gbp(_amount(amount,"lender.loan_amount"))}'
        if offer_ref: text += f' (application reference {offer_ref})'
    return text+'.', []


def _fill_template(template: Path, values: dict[str,str], destination: Path) -> list[str]:
    from docx import Document
    if destination.exists():
        raise LegalReviewRequired(f'Output already exists; refusing overwrite: {destination}')
    doc=Document(template)
    found=set()
    for para in doc.paragraphs:
        for run in para.runs:
            old=run.text
            for key, val in values.items():
                token='{{'+key+'}}'
                if token in run.text:
                    found.add(key)
            if '{{' in old:
                run.text=re.sub(r'\{\{([A-Z_]+)\}\}',
                    lambda m: values[m.group(1)] if m.group(1) in values else m.group(),old)
    missing_tokens=set(values)-found
    if missing_tokens:
        raise LegalReviewRequired('Required template placeholder(s) missing: '+', '.join(sorted(missing_tokens)))
    remaining=re.findall(r'\{\{[^{}]+\}\}', '\n'.join(p.text for p in doc.paragraphs))
    if remaining:
        raise LegalReviewRequired('Unreplaced placeholder(s): '+', '.join(sorted(set(remaining))))
    content='\n'.join(p.text for p in doc.paragraphs).lower()
    if any(bad in content for bad in ('date of birth','occupation of witness','occupation:')):
        raise LegalReviewRequired('The selected template still contains excluded identity/occupation fields')
    destination.parent.mkdir(parents=True,exist_ok=True)
    doc.save(destination)
    return sorted(found)


def generate_gift_deeds(payload: dict, output_dir: str | Path, template: str | Path = TEMPLATE) -> dict:
    """Create one fresh DOCX per donor and a review summary, without overwriting files."""
    if not isinstance(payload,dict): raise LegalReviewRequired('Input must be a JSON object')
    transaction_type=_clean(payload.get('transaction_type'),'transaction_type',True).lower()
    if transaction_type not in {'purchase','remortgage'}:
        raise LegalReviewRequired('transaction_type must be purchase or remortgage')
    property_address=_clean(payload.get('property_address'),'property_address',True)
    identification,donee_ref,recipient_phrase,subject,donee_missing=_donees(payload.get('donees'))
    # A gift to several recipients jointly changes their entitlement; require express instructions.
    if len(payload['donees']) > 1 and _clean(payload.get('recipient_allocation'),'recipient_allocation').lower() != 'joint':
        raise LegalReviewRequired('recipient_allocation: joint must be expressly supplied for multiple donees; do not infer their entitlement')
    recital, lender_warnings=_recital(transaction_type,subject,payload.get('lender'))
    donors=payload.get('donors')
    if not isinstance(donors,list) or not donors:
        raise LegalReviewRequired('donors must contain at least one donor')
    if len(donors)>40:raise LegalReviewRequired('No more than 40 donors per input')
    output_dir=Path(output_dir).expanduser().resolve()
    template=Path(template).expanduser().resolve()
    if not template.is_file():
        raise LegalReviewRequired('Gift deed Word template not found at '+str(template))
    if output_dir==template.parent:
        raise LegalReviewRequired('Output directory must not be the packaged template directory')
    if transaction_type=='purchase':
        purpose_recital='towards the purchase price of the Property'
        purpose_clause='towards the purchase of the Property'
    else:
        purpose_recital='in connection with the remortgage of the Property'
        purpose_clause=purpose_recital
    prefix=_clean(payload.get('output_prefix'),'output_prefix') or 'Deed_of_Gift'
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,60}',prefix):
        raise LegalReviewRequired('output_prefix may only contain letters, numbers, hyphens and underscores')
    planned=[]; seen=set()
    for i,donor in enumerate(donors,1):
        if not isinstance(donor,dict): raise LegalReviewRequired(f'donors[{i}] must be an object')
        donor_name=_get(donor,'name',f'donors[{i}]',True)
        donor_address=_get(donor,'address',f'donors[{i}]')
        amount=_amount(donor.get('amount'),f'donors[{i}].amount')
        bank=donor.get('bank') or {}
        if not isinstance(bank,dict):raise LegalReviewRequired(f'donors[{i}].bank must be an object')
        fields={
            'DONOR_NAME': donor_name.upper(),
            'DONOR_ADDRESS': donor_address or DOTTED_LONG,
            'DONEES_IDENTIFICATION': identification,
            'PROPERTY_ADDRESS': property_address,
            'TRANSACTION_RECITAL': recital,
            'GIFT_AMOUNT': _gbp(amount),
            'GIFT_AMOUNT_WORDS': _money_words(amount),
            'RECIPIENT_PHRASE': recipient_phrase,
            'DONEE_REFERENCE': donee_ref,
            'PURPOSE_RECITAL': purpose_recital,
            'PURPOSE_CLAUSE': purpose_clause,
            'SOURCE_OF_FUNDS': _get(donor,'source_of_funds',f'donors[{i}]') or DOTTED_LONG,
            'BANK_NAME': _get(bank,'name',f'donors[{i}].bank') or DOTTED_SHORT,
            'ACCOUNT_HOLDER': _get(bank,'account_holder',f'donors[{i}].bank') or DOTTED_SHORT,
            'ACCOUNT_NUMBER_IBAN': _get(bank,'account_number_iban',f'donors[{i}].bank') or DOTTED_LONG,
            'SORT_CODE_SWIFT_BIC': _get(bank,'sort_code_swift_bic',f'donors[{i}].bank') or DOTTED_LONG,
        }
        slug=re.sub(r'[^A-Za-z0-9]+','_',donor_name).strip('_')[:60] or f'Donor_{i}'
        filename=f'{prefix}_{slug}.docx'
        if filename.lower() in seen:
            filename=f'{prefix}_{slug}_{i}.docx'
        seen.add(filename.lower())
        missing=list(donee_missing)
        if not donor_address:missing.append(f'donors[{i}].address')
        if not donor.get('source_of_funds'):missing.append(f'donors[{i}].source_of_funds')
        for k in ('name','account_holder','account_number_iban','sort_code_swift_bic'):
            if not bank.get(k):missing.append(f'donors[{i}].bank.{k}')
        planned.append((filename,donor_name,amount,fields,missing))
    if len(set(name.lower() for name,*_ in planned)) != len(planned):
        raise LegalReviewRequired('Output filenames must be unique')
    for filename,*_ in planned:
        if (output_dir/filename).exists():
            raise LegalReviewRequired(f'Output already exists: {filename}; choose another folder')
    result={
        'status':'DRAFTS_CREATED_REVIEW_REQUIRED',
        'transaction_type':transaction_type,
        'property_address':property_address,
        'documents':[],
        'total_gift':_gbp(sum((amount for _,_,amount,_,_ in planned),Decimal('0'))),
        'title_number':'NOT INCLUDED: check official copy register separately',
        'review_required':[
            'Confirm each gift and joint or sole recipient allocation directly with the donor and borrowers',
            'Check the current lender offer and applicable gift/source-of-funds conditions and obtain written approval where required',
            'Verify source of funds/wealth and donor bank details separately under firm AML policy',
            'Check insolvency, third-party interests, conditions, repayability and any tax or independent advice issues',
            'Confirm deed wording and execution with a supervising qualified solicitor before signing',
            'The donor must sign as a deed in the physical presence of an attesting witness, with genuine delivery as a deed',
        ] + lender_warnings,
        'evidence_note':'Input values are user-supplied drafting data, not independently verified. No deed is signed, dated, witnessed, delivered or lender-approved by this tool.',
        'authority':{'law':'Law of Property (Miscellaneous Provisions) Act 1989, s.1',
                     'url':'https://www.legislation.gov.uk/ukpga/1989/34/section/1',
                     'guidance':'https://www.gov.uk/government/publications/execution-of-deeds/practice-guide-8-execution-of-deeds',
                     'source_checked':'2026-11-20',
                     'note':'Check the latest statutory text, lender requirements and practice guidance at point of use; not auto-verified by this local utility.'}
    }
    for filename,name,amount,fields,missing in planned:
        out=output_dir/filename
        filled=_fill_template(template,fields,out)
        result['documents'].append({'filename':filename,'donor':name,'gift_amount':_gbp(amount),
                                    'missing_fields':missing,'filled_template_tokens':filled,
                                    'status':'NOT EXECUTED; LAWYER AND LENDER REVIEW REQUIRED'})
    return result


def main(argv=None) -> int:
    parser=argparse.ArgumentParser(description='Produce individual draft Deeds of Gift from confidential JSON, for supervised English/Welsh property work only')
    parser.add_argument('--input',required=True,help='Path to local private JSON instructions')
    parser.add_argument('--output-dir',required=True,help='Output folder (new filenames only; no overwrites)')
    parser.add_argument('--review-out',help='Optional JSON review report path (must not already exist)')
    parser.add_argument('--template',default=str(TEMPLATE),help='Optional Word template path')
    args=parser.parse_args(argv)
    try:
        payload=json.loads(Path(args.input).read_text(encoding='utf-8'))
        if args.review_out and Path(args.review_out).exists():
            raise LegalReviewRequired('Review report already exists; refusing overwrite')
        r=generate_gift_deeds(payload,args.output_dir,args.template)
        summary=json.dumps(r,indent=2,ensure_ascii=False)+'\n'
        if args.review_out:
            Path(args.review_out).parent.mkdir(parents=True,exist_ok=True)
            Path(args.review_out).write_text(summary,encoding='utf-8')
            print(json.dumps({'status':r['status'],'documents':r['documents'], 'review_report':args.review_out},indent=2,ensure_ascii=False))
        else:
            print(summary)
        return 0
    except (ValueError,FileNotFoundError,PermissionError,json.JSONDecodeError) as exc:
        print(json.dumps({'status':'REFUSED_UNVERIFIED_OR_INVALID','error':str(exc)},indent=2),file=sys.stderr)
        return 2

if __name__=='__main__':sys.exit(main())
