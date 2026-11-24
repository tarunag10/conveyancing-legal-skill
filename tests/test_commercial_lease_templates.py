"""Regression checks for sanitised English commercial lease DOCX precedents.

Run: python -m unittest tests/test_commercial_lease_templates.py
Requires python-docx (documents extra). Layout rendering is an additional manual QA gate.
"""
import re
import unittest
from pathlib import Path
from zipfile import ZipFile

try:
    from docx import Document
except ImportError:
    Document = None

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "templates"

@unittest.skipUnless(Document is not None, "python-docx not installed")
class CommercialLeaseTemplates(unittest.TestCase):
    def test_master_files_present(self):
        for n in ("COMMERCIAL_LEASE_MASTER.docx", "RENT_DEPOSIT_DEED_MASTER.docx", "STATUTORY_DECLARATION_1954_MASTER.docx"):
            self.assertTrue((T/n).is_file(), n)

    def test_full_lease_clauses_and_schedule(self):
        doc=Document(T/"COMMERCIAL_LEASE_MASTER.docx")
        body='\n'.join(p.text for p in doc.paragraphs)
        for i in range(1,51):
            self.assertRegex(body,rf"(?m)^{i}[.]\s+[A-Z]",f"Main clause {i} missing")
        self.assertIn("SCHEDULE\n",body)
        for i in range(1,8):
            # The TOC and complete schedule both include the section number.
            self.assertGreaterEqual(len(re.findall(rf"(?m)^{i}[.]\s+",body)),2,f"Schedule section {i} absent")
        self.assertIn("PRESCRIBED CLAUSES",body)
        for i in range(1,15):self.assertIn(f"LR{i}.",body)
        self.assertIn("PLAN 1",body)

    def test_toc_is_linked_to_real_bookmarks(self):
        with ZipFile(T/"COMMERCIAL_LEASE_MASTER.docx") as z:
            xml=z.read('word/document.xml').decode('utf8')
        for i in range(1,51):
            self.assertIn('PAGEREF cl'+str(i),xml)
            self.assertIn('w:name="cl'+str(i)+'"',xml)
        self.assertIn('PAGEREF sched',xml)

    def test_no_historic_client_identity_or_instruction_placeholders(self):
        banned=['AMRIK','JASHBIR','JOHAL','SHAHINUR','RAHMAN','ROMFORD','EGL66830','E12 5AJ','18,000','22,000','5,500','4,500']
        for n in ('COMMERCIAL_LEASE_MASTER.docx','RENT_DEPOSIT_DEED_MASTER.docx','STATUTORY_DECLARATION_1954_MASTER.docx'):
            doc=Document(T/n)
            txt='\n'.join(p.text for p in doc.paragraphs)
            for token in banned:self.assertNotIn(token.lower(),txt.lower(),(n,token))
            self.assertNotRegex(txt,r'\[(?:TO CONFIRM|INSERT|PLACEHOLDER|DATE|NAME|ADDRESS)[^\]]*\]')
            self.assertIn('____________',txt)

if __name__=='__main__':unittest.main()
