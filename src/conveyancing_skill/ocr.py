"""Opt-in local OCR for document review, with bounded input and no network."""
from __future__ import annotations
import hashlib
import subprocess
import tempfile
from pathlib import Path
from .engine import LegalReviewRequired


def ocr_document(path: str) -> dict:
    source=Path(path)
    if not source.is_file() or source.stat().st_size > 40_000_000:
        raise LegalReviewRequired('OCR source missing or exceeds 40 MB')
    if source.suffix.lower() not in ('.pdf','.png','.jpg','.jpeg','.tif','.tiff'):
        raise LegalReviewRequired('OCR supports PDF, PNG, JPEG and TIFF')
    def run(args):
        try:
            result=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60,check=False)
        except (FileNotFoundError,subprocess.TimeoutExpired) as exc:
            raise LegalReviewRequired(f'OCR tool unavailable or timed out: {args[0]}') from exc
        if result.returncode:
            raise LegalReviewRequired(f'OCR tool failed: {args[0]}')
        if len(result.stdout)>2_000_000:
            raise LegalReviewRequired('OCR output exceeds size limit')
        return result.stdout.decode('utf8',errors='replace').strip()
    with tempfile.TemporaryDirectory(prefix='conveyancing-ocr-') as tmp:
        root=Path(tmp)
        if source.suffix.lower()=='.pdf':
            try:
                from pypdf import PdfReader
                reader=PdfReader(str(source))
                if reader.is_encrypted: raise LegalReviewRequired('Encrypted PDF requires an authorised decrypted copy')
                pages=len(reader.pages)
                for page in reader.pages:
                    box=page.mediabox
                    width=float(box.width)*150/72; height=float(box.height)*150/72
                    if width<=0 or height<=0 or width>10000 or height>10000 or width*height>40_000_000:
                        raise LegalReviewRequired('PDF page dimensions exceed OCR limits')
            except LegalReviewRequired: raise
            except Exception as exc: raise LegalReviewRequired('Cannot inspect PDF for OCR') from exc
            if pages>20: raise LegalReviewRequired('OCR supports at most 20 pages per file; split for review')
            images=[]
            for n in range(1,pages+1):
                prefix=root/f'page-{n}'
                run(['pdftoppm','-f',str(n),'-l',str(n),'-r','150','-singlefile','-png',str(source),str(prefix)])
                images.append((n,prefix.with_suffix('.png')))
        else:
            images=[(1,source)]
        try:
            from PIL import Image
        except ImportError as exc: raise LegalReviewRequired('OCR requires Pillow') from exc
        elements=[]
        for n,image in images:
            try:
                with Image.open(image) as im:
                    if getattr(im,'n_frames',1)>1: raise LegalReviewRequired('Multi-frame images must be split into separate files')
                    if im.width*im.height>40_000_000: raise LegalReviewRequired('OCR image exceeds 40 megapixels')
                    im.verify()
            except LegalReviewRequired: raise
            except Exception as exc: raise LegalReviewRequired(f'Unreadable OCR image at page {n}') from exc
            text=run(['tesseract',str(image),'stdout'])
            elements.append({'location':f'page {n}','text':text,'status':'unverified_ocr'})
    return {'file_name':source.name,'document_id':hashlib.sha256(source.read_bytes()).hexdigest()[:16],
            'elements':elements,'warnings':['OCR can omit or alter text; compare every citation with the original.',
            'Plans, boundaries, colour markings, signatures and execution are not verified.'],
            'legal_status':'UNVERIFIED OCR; human inspection required'}
