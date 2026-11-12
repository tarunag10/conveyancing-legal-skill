import tempfile
import unittest
import json
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from pathlib import Path
from unittest.mock import patch
from conveyancing_skill.engine import LegalReviewRequired, completion, review_matter, statutory_deadline, money
from conveyancing_skill.source_watch import is_official_url, watch

class RegressionTests(unittest.TestCase):
    def test_false_strings_cannot_clear_funds_gates(self):
        result=completion({'side':'buyer','purchase_price':'100','deposit_paid':'0',
            'cleared_client_funds':'100','cleared_lender_funds':'0',
            'bank_evidence_confirmed_by_human':'false','lender_conditions_satisfied_by_human':'false'})
        self.assertEqual(2,len(result['completion_blockers']))

    def test_malformed_observations_refused(self):
        for matter in ([],{'charges':[None]}, {'access':{'checked_by_human':'false'}},
                       {'lender_requirements':[{'checked_by_human':1}]}, {'documents':'not a list'}):
            with self.subTest(matter=matter),self.assertRaises(LegalReviewRequired):review_matter(matter)

    def test_unknown_charge_status_refused(self):
        with self.assertRaises(LegalReviewRequired):review_matter({'charges':[{'status':'looks fine'}]})

    def test_excessive_amount_refused(self):
        with self.assertRaises(LegalReviewRequired):money('1e1000')

    def test_malformed_completion_refused(self):
        for statement in ([],{'side':'buyer','seller_debits':[{}]}, {'side':'buyer','other_payments':'100'}):
            with self.subTest(statement=statement),self.assertRaises(LegalReviewRequired):completion(statement)

    def test_priority_warns_about_delivery(self):
        result=statutory_deadline('os1','2026-10-27',holidays=[])
        self.assertEqual(result['due_date'],result['delivery_by_noon_date'])
        self.assertIn('noon',result['warning'])

    def test_network_origin_and_limit(self):
        for url in ('https://www.gov.uk:444/test','https://user:pass@www.gov.uk/test',
                    'https://www.gov.uk:bad/test'):
            self.assertFalse(is_official_url(url))
        for limit in (-1,0,True):
            with self.assertRaises(LegalReviewRequired):watch(limit=limit)

    def test_changed_source_does_not_advance_baseline(self):
        from conveyancing_skill.cli import main
        with tempfile.TemporaryDirectory() as temp:
            baseline=Path(temp)/'baseline.json'
            baseline.write_text(json.dumps({'rule':'old'}))
            result={'sources':[{'source_id':'rule','status':'change_detected_review_required','sha256':'new'}],
                    'legal_review_queue':[{'source_id':'rule'}]}
            with patch('conveyancing_skill.cli.watch',return_value=result), redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                rc=main(['source-watch','--baseline',str(baseline),'--baseline-out',str(baseline),'--fail-on-change'])
            self.assertEqual(3,rc)
            self.assertEqual({'rule':'old'},json.loads(baseline.read_text()))

    def test_docx_replacements_are_simultaneous(self):
        from docx import Document
        from conveyancing_skill.documents import fill_placeholders
        with tempfile.TemporaryDirectory() as temp:
            src=Path(temp)/'in.docx';out=Path(temp)/'out.docx'
            d=Document();d.add_paragraph('{{A}} and {{B}}');d.save(src)
            fill_placeholders(str(src),str(out),{'A':'literal {{B}}','B':'second'},allowed=['A','B'],source_refs={'A':'D1','B':'D2'})
            self.assertEqual('literal {{B}} and second',Document(out).paragraphs[0].text)

    def test_partial_split_placeholder_refused_without_output(self):
        from docx import Document
        from conveyancing_skill.documents import fill_placeholders
        with tempfile.TemporaryDirectory() as temp:
            src=Path(temp)/'in.docx';out=Path(temp)/'out.docx'
            d=Document();p=d.add_paragraph('{{A}} then ');p.add_run('{{');p.add_run('A}}');d.save(src)
            with self.assertRaises(LegalReviewRequired):
                fill_placeholders(str(src),str(out),{'A':'new'},allowed=['A'],source_refs={'A':'D1'})
            self.assertFalse(out.exists())

    def test_table_conversion_does_not_drop_extra_cell(self):
        from conveyancing_skill.documents import to_docx
        with tempfile.TemporaryDirectory() as temp:
            src=Path(temp)/'in.md';out=Path(temp)/'out.docx'
            src.write_text('|A|B|\n|---|---|\n|1|2|MATERIAL TEXT|\n')
            with self.assertRaises(LegalReviewRequired):to_docx(str(src),str(out))
            self.assertFalse(out.exists())

if __name__=='__main__':unittest.main()
