"""Synthetic registration, security and post-completion unit tests."""
from __future__ import annotations
from copy import deepcopy
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from conveyancing_skill.matter_store import new_matter
from conveyancing_skill.matter_lifecycle import security_map,requisitions,post_completion,form_preflight
from conveyancing_skill.workbench import main,lender_data

class LifecycleTests(TestCase):
 def setUp(self):
    self.m=new_matter('ANON-CASE','England','auction_purchase')
 def test_security_map_multiple_properties(self):
    self.m['securities']=[{'id':'S1','title_number':'AA1234','property_id':'P1','intended_rank':'first','charge_instrument_ref':'CH1'},
                          {'id':'S2','title_number':'BB5678','property_id':'P2','intended_rank':'second','charge_instrument_ref':'CH2'}]
    r=security_map(self.m);self.assertEqual(r['identified_estates'],2)
    self.assertTrue(any(i['id']=='SEC-RANK-S2' for i in r['preflight_issues']))
 def test_security_map_duplicate_title_warns(self):
    self.m['securities']=[{'id':'S1','title_number':'AA1234'},{'id':'S2','title_number':'AA1234'}]
    self.assertEqual(security_map(self.m)['warnings'][0]['code'],'DUPLICATE-SECURITY-TITLE')
 def test_requisition_never_invents_deadline(self):
    self.m['registration']={'requisitions':[{'id':'REQ1','status':'open','issued_on':'2026-11-20'}]}
    self.assertIsNone(requisitions(self.m)['items'][0]['effective_deadline_if_confirmed'])
 def test_requisition_requested_extension_not_accepted(self):
    self.m['registration']={'requisitions':[{'id':'REQ1','issued_on':'2026-11-20','deadline':'2026-12-04',
           'extension_requested':True,'extension_confirmed_to':'2026-12-12','status':'open'}]}
    x=requisitions(self.m)['items'][0]
    self.assertEqual(x['effective_deadline_if_confirmed'],'2026-12-04')
    self.assertTrue(any('not evidenced' in warning for warning in x['warnings']))
 def test_requisition_approved_extension_applies(self):
    self.m['registration']={'requisitions':[{'id':'REQ1','issued_on':'2026-11-20','deadline':'2026-12-04',
           'extension_requested':True,'extension_confirmed_to':'2026-12-12','extension_approval_ref':'HMLR-confirmation', 'status':'open'}]}
    self.assertEqual(requisitions(self.m)['items'][0]['effective_deadline_if_confirmed'],'2026-12-12')
 def test_past_due_requires_as_of(self):
    self.m['registration']={'requisitions':[{'id':'REQ1','deadline':'2026-12-04','status':'open'}]}
    self.assertFalse(requisitions(self.m)['items'][0]['overdue_as_of_supplied_date'])
    self.assertTrue(requisitions(self.m,'2026-12-05')['items'][0]['overdue_as_of_supplied_date'])
 def test_postcompletion_submission_not_registration(self):
    self.m['registration']={'submission_status':'application_submitted','filing_acknowledgement':'A1'}
    x=post_completion(self.m)
    self.assertEqual(x['registration_completion_status'],'NOT CONFIRMED')
 def test_postcompletion_evidence_required(self):
    self.m['post_completion']={'hmlr':{'status':'completed'}}
    x=post_completion(self.m)
    item=next(t for t in x['tasks'] if t['id']=='hmlr')
    self.assertEqual(item['status'],'claimed_done_without_external_evidence')
 def test_postcompletion_company_if_applicable(self):
    self.m['specialist']={'uk_company_or_llp_borrower':True}
    self.assertIn('company_charge',[i['id'] for i in post_completion(self.m)['tasks']])
 def test_postcompletion_no_company_if_not_applicable(self):
    self.assertNotIn('company_charge',[i['id'] for i in post_completion(self.m)['tasks']])
 def test_form_first_registration_requires_epitome(self):
    self.m['registration']={'application_type':'FR1'}
    self.assertIn('FORM-FR1-EPITOME',[x['id'] for x in form_preflight(self.m)['issues']])
 def test_form_no_prescribed_facsimile_claim(self):
    self.m['registration']={'application_type':'AP1'}
    self.assertIn('No form has been signed',form_preflight(self.m)['warnings'][1])
 def test_requisition_missing_acknowledgement(self):
    self.m['registration']={'requisitions':[{'id':'REQ1','deadline':'2026-12-04','status':'response_sent'}]}
    self.assertTrue(any('Sending a response' in w for w in requisitions(self.m)['items'][0]['warnings']))
 def test_new_cli_routes_work(self):
    with TemporaryDirectory() as d:
        f=Path(d)/'m.json'
        self.assertEqual(main(['init',str(f),'--matter-id','ANON-CASE','--jurisdiction','England','--transaction-type','purchase']),0)
        for action in ('post-completion','requisitions','security-map','form-preflight'):
            self.assertEqual(main([action,str(f),'--output',str(Path(d)/(action+'.json'))]),0)
 def test_lender_directory_runtime_access(self):
    self.assertGreaterEqual(len(lender_data()['lenders']),110)
