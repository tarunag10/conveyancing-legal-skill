"""Accessible original Word output and controlled amendments to user templates.

Never claims to create or alter an official prescribed Land Registry form.
"""
from __future__ import annotations
import re
from pathlib import Path
from .engine import LegalReviewRequired


def _add_inline(paragraph, text: str):
    """Support basic **bold**, *italic* and labelled [official links](https://...)."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.opc.constants import RELATIONSHIP_TYPE as RT

    def add_hyperlink(label, url):
        r_id=paragraph.part.relate_to(url, RT.HYPERLINK, is_external=True)
        hyperlink=OxmlElement('w:hyperlink');hyperlink.set(qn('r:id'),r_id)
        run=OxmlElement('w:r');rpr=OxmlElement('w:rPr')
        rstyle=OxmlElement('w:rStyle');rstyle.set(qn('w:val'),'Hyperlink')
        rpr.append(rstyle);run.append(rpr)
        child=OxmlElement('w:t');child.text=label;run.append(child)
        hyperlink.append(run);paragraph._p.append(hyperlink)

    for chunk in re.split(r'(\[[^\]]+\]\(https://[^)]+\))',text):
        match=re.fullmatch(r'\[([^\]]+)\]\((https://[^)]+)\)',chunk)
        if match:
            add_hyperlink(match.group(1),match.group(2));continue
        for bit in re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*)',chunk):
            if not bit:continue
            if bit.startswith('**') and bit.endswith('**'):
                r=paragraph.add_run(bit[2:-2]);r.bold=True
            elif bit.startswith('*') and bit.endswith('*'):
                r=paragraph.add_run(bit[1:-1]);r.italic=True
            else:paragraph.add_run(bit)


def _cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def _is_table_separator(line):
    return bool(re.fullmatch(r'[|\s:\-]+',line)) and '-' in line


def to_docx(source: str, target: str) -> dict:
    """Create readable, accessible-ish editable Word from original non-prescribed text.

    Formal WCAG/PDF-UA audit and exact visual preservation are outside this converter.
    """
    from docx import Document
    from docx.shared import Pt
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    src=Path(source)
    if not src.is_file() or src.suffix.lower() not in ('.md','.txt'):
        raise LegalReviewRequired('Provide existing Markdown/TXT for original, non-prescribed report output')
    doc=Document()
    doc.styles['Normal'].font.name='Aptos'
    doc.styles['Normal'].font.size=Pt(12)
    doc.styles['Normal'].paragraph_format.space_after=Pt(8)
    lines=src.read_text(encoding='utf-8').splitlines()
    index=0
    while index<len(lines):
        line=lines[index]
        head=re.match(r'^(#{1,4})\s+(.*)$',line)
        if head:
            if len(head.group(1))==1 and not doc.core_properties.title:doc.core_properties.title=head.group(2)
            doc.add_heading(head.group(2),level=len(head.group(1)))
        elif line.startswith('|') and index+1<len(lines) and _is_table_separator(lines[index+1]):
            header=_cells(line);i=index+2;rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                rows.append(_cells(lines[i]));i+=1
            table=doc.add_table(rows=1,cols=len(header));table.style='Table Grid'
            for col,text in enumerate(header):
                cell=table.rows[0].cells[col];cell.text='';_add_inline(cell.paragraphs[0],text)
                for run in cell.paragraphs[0].runs:run.bold=True
            tbl_pr=table.rows[0]._tr.get_or_add_trPr()
            el=OxmlElement('w:tblHeader');el.set(qn('w:val'),'true');tbl_pr.append(el)
            for values in rows:
                cells=table.add_row().cells
                for col,value in enumerate(values[:len(header)]):
                    cells[col].text='';_add_inline(cells[col].paragraphs[0],value)
            for word_row in table.rows:
                tr_pr=word_row._tr.get_or_add_trPr()
                prevent_split=OxmlElement('w:cantSplit');tr_pr.append(prevent_split)
            index=i-1
        elif line.startswith('- '):
            p=doc.add_paragraph(style='List Bullet');_add_inline(p,line[2:])
        elif re.match(r'^\d+\. ',line):
            p=doc.add_paragraph(style='List Number');_add_inline(p,re.sub(r'^\d+\. ','',line))
        elif line.strip():
            p=doc.add_paragraph();_add_inline(p,line)
        index+=1
    out=Path(target);out.parent.mkdir(parents=True,exist_ok=True);doc.save(out)
    return {'path':str(out),'status':'editable Word with heading styles, semantic tables and editable inline runs; formal accessibility audit still required; original non-prescribed reports only'}


def fill_placeholders(src: str, target: str, replacements: dict, *, allowed: list[str], source_refs: dict) -> dict:
    """Replace only literal {{FIELD}} in one Word run, keeping unrelated runs.

    Rejects placeholders split between Word runs, supplied without evidence references,
    or overwrite of original. Do not use this code to edit prescribed legal wording.
    """
    from docx import Document
    if Path(src).resolve()==Path(target).resolve():
        raise LegalReviewRequired('Never overwrite supplied original: supply a distinct target path')
    if not isinstance(replacements,dict) or not isinstance(source_refs,dict):
        raise LegalReviewRequired('Replacements and source refs must be dictionaries')
    doc=Document(src)
    change_log=[]
    refs=set(allowed)
    if set(replacements)-refs:
        raise LegalReviewRequired('Replacement field not explicitly allowlisted: '+','.join(set(replacements)-refs))
    if any(not str(source_refs.get(field,'')).strip() for field in replacements):
        raise LegalReviewRequired('Every replacement requires a nonempty documentary evidence source ref')
    paragraphs=list(doc.paragraphs)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:paragraphs.extend(cell.paragraphs)
    counts={key:0 for key in replacements}
    for i,p in enumerate(paragraphs,1):
        for run_idx,run in enumerate(p.runs,1):
            for field,value in replacements.items():
                token='{{'+field+'}}'
                if token in run.text:
                    if not isinstance(value,str):raise LegalReviewRequired(f'{field}: value must be a string')
                    occurrences=run.text.count(token)
                    run.text=run.text.replace(token,value)
                    counts[field]+=occurrences
                    change_log.append({'field':field,'old_text':token,'new_text':value,'source_ref':source_refs[field], 'location':f'paragraph {i}, run {run_idx}', 'occurrences':occurrences})
    if any(counts[key]==0 for key in replacements):
        raise LegalReviewRequired('One or more placeholders not found wholly within a run: '+', '.join(k for k,v in counts.items() if v==0))
    out=Path(target);out.parent.mkdir(parents=True,exist_ok=True);doc.save(out)
    return {'output':str(out),'change_log':change_log,'note':'Unchanged text is preserved at run level; inspect source and output page-by-page before use; not a substitute for statutory form verification.'}
