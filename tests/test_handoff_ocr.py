import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from conveyancing_skill.engine import LegalReviewRequired
from conveyancing_skill.handoff import export_actions

class HandoffTests(unittest.TestCase):
    def test_export_escapes_formula_and_refuses_overwrite(self):
        data={'stages':[{'id':'title','title':'Title','work_record':{'open_actions':[{'action':'=HYPERLINK("x")','status':'outstanding','owner':None,'due_date':None}]}}]}
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'actions.csv'
            self.assertEqual(1,export_actions(data,dest)['rows'])
            with dest.open(encoding='utf-8-sig',newline='') as f:
                row=next(csv.DictReader(f))
            self.assertTrue(row['action'].startswith("'="))
            with self.assertRaises(LegalReviewRequired):export_actions(data,dest)

    def test_invalid_workflow_is_refused_before_file_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'actions.csv'
            with self.assertRaises(LegalReviewRequired):export_actions({'stages':[{}]},dest)
            self.assertFalse(dest.exists())

class OCRTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('tesseract'), 'optional local Tesseract unavailable')
    def test_image_ocr_returns_unverified_page_location(self):
        try:
            from PIL import Image, ImageDraw
        except ImportError:
            self.skipTest('optional Pillow unavailable')
        from conveyancing_skill.ocr import ocr_document
        with tempfile.TemporaryDirectory() as tmp:
            image=Image.new('RGB',(400,60),'white')
            ImageDraw.Draw(image).text((10,10),'TITLE XX123456',fill='black')
            image=image.resize((1600,240))
            path=Path(tmp)/'scan.png'; image.save(path)
            result=ocr_document(str(path))
            self.assertEqual('page 1',result['elements'][0]['location'])
            self.assertEqual('unverified_ocr',result['elements'][0]['status'])
            self.assertTrue(result['elements'][0]['text'])

    @unittest.skipUnless(shutil.which('tesseract') and shutil.which('pdftoppm'), 'optional OCR tools unavailable')
    def test_pdf_ocr_reports_the_original_page(self):
        try:
            from PIL import Image, ImageDraw
            import pypdf
        except ImportError:
            self.skipTest('optional OCR dependencies unavailable')
        from conveyancing_skill.ocr import ocr_document
        with tempfile.TemporaryDirectory() as tmp:
            image=Image.new('RGB',(1200,300),'white')
            ImageDraw.Draw(image).text((30,30),'TITLE XX123456',fill='black')
            path=Path(tmp)/'scan.pdf'; image.save(path,'PDF',resolution=72)
            result=ocr_document(str(path))
            self.assertEqual('page 1',result['elements'][0]['location'])
            self.assertEqual('unverified_ocr',result['elements'][0]['status'])
