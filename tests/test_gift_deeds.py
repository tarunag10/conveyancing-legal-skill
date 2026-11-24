"""Small local fixtures for the original Gift Deed generator; no real client data."""
from decimal import Decimal
from pathlib import Path
import tempfile
import unittest

from docx import Document
from conveyancing_skill.gift_deeds import generate_gift_deeds, _money_words, _amount, _donees, TEMPLATE


class GiftDeedTests(unittest.TestCase):
    def test_amount_words_and_pence(self):
        self.assertEqual(_money_words(Decimal('87000.00')),'eighty-seven thousand pounds')
        self.assertEqual(_money_words(Decimal('2001.25')),'two thousand and one pounds and twenty-five pence')
        with self.assertRaises(ValueError): _amount('1.235','donors[1].amount')

    def test_draft_does_not_claim_executed_or_disclose_dob(self):
        payload={
            'transaction_type':'remortgage',
            'recipient_allocation':'joint',
            'property_address':'1 Example Street, Example Town, EX1 1AA',
            'donees':[{'name':'Alex Example','address':'1 Example Street, Example Town, EX1 1AA'},
                      {'name':'Taylor Example','address':'1 Example Street, Example Town, EX1 1AA'}],
            'lender':{'name':'Fictional Mortgage Ltd','loan_amount':'100000','offer_date':'1 November 2026'},
            'donors':[{'name':'Jordan Example','amount':'25000','bank':{}},
                      {'name':'Casey Example','amount':'5000.50'}]
        }
        with tempfile.TemporaryDirectory() as temp:
            outcome=generate_gift_deeds(payload,temp)
            self.assertEqual(outcome['total_gift'],'£30,000.50')
            self.assertEqual(len(outcome['documents']),2)
            for row in outcome['documents']:
                doc=Document(Path(temp)/row['filename'])
                text='\n'.join(p.text for p in doc.paragraphs)
                self.assertIn('EXAMPLE',text.upper())
                self.assertNotIn('{{',text)
                self.assertNotIn('Occupation of witness',text)
                self.assertNotIn('Date of birth',text)
                self.assertIn('Signature of Donor:',text)
                self.assertIn('Signature of witness:',text)
                self.assertTrue(row['missing_fields'])

    def test_single_recipient_is_singular(self):
        ident,ref,phrase,subject,missing=_donees([{'name':'Alex Example','address':'Example Road'}])
        self.assertIn('the “Donee”',ident)
        self.assertEqual(ref,'the Donee')
        self.assertEqual(phrase,'the Donee')
        self.assertEqual(subject,'The Donee intends')

    def test_template_exists(self):
        self.assertTrue(TEMPLATE.is_file(),TEMPLATE)


if __name__=='__main__':unittest.main()
