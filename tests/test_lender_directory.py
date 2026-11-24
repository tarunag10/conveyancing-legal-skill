"""Offline data-only checks; cannot prove live lender instructions are current."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/'knowledge/lenders/lender-directory.json'

class LenderDirectoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db=json.loads(REGISTRY.read_text(encoding='utf-8'))
        cls.by_name={e['lender']:e for e in cls.db['lenders']}

    def test_research_coverage_not_a_completeness_claim(self):
        self.assertGreaterEqual(len(self.db['lenders']),110)
        self.assertIn('Not exhaustive',self.db['disclaimer'])
        self.assertEqual(len(self.db['lenders']),len(self.by_name))

    def test_all_sourced_entries_have_dated_https_sources(self):
        for e in self.db['lenders']:
            self.assertEqual(e['jurisdiction'],'England and Wales')
            self.assertIn(e['research_status'],self.db['status_meanings'])
            self.assertTrue(e['submission']['instructions'])
            for source in e['sources']:
                self.assertTrue(source['url'].startswith('https://'),e['lender'])
                self.assertEqual(source['checked_on'],'2026-11-20')
            if e['research_status'] in ('verified_submission','verified_conditional','verified_document_only'):
                self.assertTrue(e['sources'],e['lender'])

    def test_unknown_routes_not_misdescribed_as_electronic(self):
        for e in self.db['lenders']:
            if e['research_status'] in ('lookup_only','verified_document_only','verified_directory_or_panel'):
                self.assertIn(e['submission']['method'],('unknown','case_instructions'),e['lender'])
                self.assertIsNone(e['notice'],e['lender'])

    def test_distinct_brand_rules_and_routing(self):
        pairs=[('Rely Mortgages','Kent Reliance'),('HSBC UK Bank plc','HSBC Private Bank'),('Barclays Bank UK PLC','Barclays Business / Commercial Lending'),('NatWest personal mortgages','NatWest Group Commercial / Panel Firms'),('Lloyds Bank plc','Halifax')]
        for a,b in pairs:
            self.assertNotEqual(self.by_name[a]['slug'],self.by_name[b]['slug'])
        cases={'HSBC UK Bank plc':'lms_ecot','Skipton Building Society':'lms_ecot','Atom Bank plc':'lms_ecot','Santander UK plc':'lender_exchange','Metro Bank plc':'email','Virgin Money':'email','Kensington Mortgage Company Ltd':'email','Principality Building Society':'smoove'}
        for name,channel in cases.items():
            self.assertEqual(self.by_name[name]['submission']['method'],channel)
        self.assertEqual(self.by_name['Together']['submission']['method'],'specialist_rot')
        self.assertEqual(self.by_name['Bank of Ireland (UK) plc']['submission']['method'],'multiple_conditional')

    def test_no_unsupported_timing_defaults(self):
        for e in self.db['lenders']:
            notice=e['notice']
            if notice is None: continue
            if isinstance(notice,dict) and 'minimum' in notice:
                self.assertGreater(notice['minimum'],0)
                self.assertTrue(notice['requires_live_confirmation'])
                self.assertIn(notice['unit'],('working_days','business_days','calendar_days','days_unspecified','hours'))
            else:
                self.assertIn('options',notice)
            self.assertTrue(e['sources'])

if __name__=='__main__':unittest.main()
