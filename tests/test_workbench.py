"""Synthetic offline workbench tests. No real matters, live lenders or filings."""
from __future__ import annotations
from copy import deepcopy
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
import json
import os
import sys

from conveyancing_skill.matter_store import (MatterError,new_matter,read_matter,write_matter,validate_matter,verify_audit)
from conveyancing_skill.matter_intelligence import (read_pages,detect_candidates,ingest_into,contradictions,compare_text_files,lender_condition_candidates,Page)
from conveyancing_skill.matter_rules import (issue,deadlines,lender_lookup,evaluate_requirements,security_preflight,registration_preflight,execution_preflight,
                                              accounting,specialist_preflight,review,as_date,days_before,days_after)
from conveyancing_skill.matter_outputs import (draft,html_dashboard,markdown_report,export_handoff,DRAFTS)
from conveyancing_skill.workbench import main,merge_manual,obs_add,lender_data

class MatterTests(TestCase):
 def setUp(self):
    self.tmp=TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
    self.root=Path(self.tmp.name);self.file=self.root/'ANON-123.json'
    self.m=new_matter('ANON-123','England','auction_purchase')
 def test_init_has_no_approval(self):self.assertEqual(self.m['review']['decision'],'pending')
 def test_reject_client_name_as_matter_id(self):
    with self.assertRaises(MatterError):new_matter('Mr John Smith','England','purchase')
 def test_reject_unknown_jurisdiction(self):
    with self.assertRaises(MatterError):new_matter('ANON-123','Scotland','purchase')
 def test_audit_init(self):
    x=write_matter(self.file,self.m,'created');self.assertTrue(x['integrity']);self.assertEqual(verify_audit(self.file)['events'],1)
 def test_audit_revision(self):
    write_matter(self.file,self.m,'created');self.m['roles'].append('buyer');write_matter(self.file,self.m,'role_recorded');self.assertEqual(verify_audit(self.file)['events'],2)
 def test_tamper_detected(self):
    write_matter(self.file,self.m,'created');data=read_matter(self.file);data['roles']=['seller'];self.file.write_text(json.dumps(data))
    self.assertFalse(verify_audit(self.file)['valid'])
    with self.assertRaises(MatterError):write_matter(self.file,data)
 def test_reject_duplicate_doc_id(self):
    self.m['documents']=[{'document_id':'D1'},{'document_id':'D1'}]
    self.assertIn('Duplicate document IDs',validate_matter(self.m))
 def test_do_not_overwrite_reviewed(self):
    self.m['review']={'decision':'approved','reviewer':'A','reviewed_at':'2026-11-20'}
    write_matter(self.file,self.m,'created')
    with self.assertRaises(MatterError):write_matter(self.file,self.m,'edit')
 def test_invalid_manual_patch(self):
    with self.assertRaises(MatterError):merge_manual(self.m,{'review':{'decision':'approved'}})
 def test_observation_requires_document(self):
    with self.assertRaises(MatterError):obs_add(self.m,'buyer_name','Example Ltd','D2','p.1')
 def test_source_observation(self):
    self.m['documents']=[{'document_id':'D1'}]
    obs_add(self.m,'buyer_name','Example Ltd','D1','p.1')
    self.assertEqual(self.m['fact_observations']['buyer_name'][0]['verification'],'manually_recorded_not_independently_verified')
 def test_audit_metadata_does_not_copy_client_data(self):
    self.m['roles']=['buyer'];write_matter(self.file,self.m,'created')
    log=(self.file.with_name(self.file.name+'.audit.jsonl')).read_text()
    self.assertNotIn('Example Client',log)

class DocumentTests(TestCase):
 def setUp(self):
    self.tmp=TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
    self.root=Path(self.tmp.name)
    self.old=self.root/'old.txt';self.new=self.root/'new.txt'
    self.old.write_text('Buyer: Example Properties Ltd\nTitle Number: ABC123456\nLoan Amount: £230,000.00\nProperty: 12 Example Road, London\nCompletion date: 20/11/2026\n')
    self.new.write_text('Buyer: Example Properties Limited\nTitle Number: ABC123456\nLoan Amount: £220,000.00\nProperty: 12 Example Road, London\nCompletion date: 27/11/2026\n')
 def test_extraction_cites_document(self):
    cs=detect_candidates(read_pages(self.old),'D1')
    self.assertTrue(any(x['field']=='loan_amount' and x['document_id']=='D1' for x in cs))
 def test_extraction_keeps_value_unverified(self):
    cs=detect_candidates(read_pages(self.old),'D1');self.assertTrue(all(x['verification'].startswith('unverified_') for x in cs))
 def test_document_diff_catches_loan_and_date(self):
    changed=compare_text_files([str(self.old),str(self.new)])['changed_candidate_fields']
    self.assertIn('loan_amount',[x['field'] for x in changed]);self.assertIn('completion_date',[x['field'] for x in changed])
 def test_document_comp_truncated_safe(self):
    x=compare_text_files([str(self.old),str(self.new)],max_diff_lines=2)
    self.assertTrue(x['diff_truncated']);self.assertEqual(len(x['text_diff']),2)
 def test_ingestion_flags_conflict(self):
    m=new_matter('ANON-123','England','purchase')
    ingest_into(m,self.old,'D1');ingest_into(m,self.new,'D2')
    self.assertIn('loan_amount',[x['field'] for x in contradictions(m)])
 def test_lender_clause_candidate_not_automatic_condition(self):
    m=new_matter('ANON-123','England','purchase')
    self.old.write_text('Borrower: Example Ltd\nThe solicitor must provide the insurance schedule before drawdown.\n')
    x=ingest_into(m,self.old,'D1','lender_offer')
    self.assertEqual(x['lender_condition_candidates'],1)
    self.assertEqual(len(m['requirements']),0)
    self.assertEqual(m['lender_condition_candidates'][0]['status'],'untriaged_unverified')
    self.assertTrue(any(i['id']=='LENDER-CANDIDATES' for i in review(m)['issues']))
 def test_candidate_triage_reference_does_not_approve_requirement(self):
    m=new_matter('ANON-123','England','purchase')
    m['lender_condition_candidates']=[{'candidate_id':'D1-COND-1','source_document_id':'D1','source_locator':'line 1','text':'Please provide insurance'}]
    m['requirements']=[{'id':'R1','candidate_ref':'D1-COND-1','description':'Provide insurance','status':'outstanding','blocking':True,'source_document_id':'D1','source_locator':'line 1'}]
    r=review(m)
    self.assertFalse(any(i['id']=='LENDER-CANDIDATES' for i in r['issues']))
    self.assertTrue(any(i['id']=='LENDER-R1' for i in r['issues']))
 def test_ingestion_duplicate_rejected(self):
    m=new_matter('ANON-123','England','purchase');ingest_into(m,self.old,'D1')
    with self.assertRaises(MatterError):ingest_into(m,self.old,'D2')
 def test_unsupported_type_rejected(self):
    f=self.root/'im.jpeg';f.write_bytes(b'img')
    with self.assertRaises(MatterError):read_pages(f)
 def test_blank_document(self):
    self.old.write_text('')
    m=new_matter('ANON-123','England','purchase')
    rec=ingest_into(m,self.old,'D1')
    self.assertIn('No readable text',rec['document']['extraction_warning'])

class RulesTests(TestCase):
 def setUp(self):self.m=new_matter('ANON-123','England','auction_purchase')
 def test_sdlt(self):
    self.m['dates']={'tax_effective_date':'2026-11-20'}
    self.assertEqual(deadlines(self.m)['deadlines'][0]['due_date'],'2026-12-04')
 def test_ltt(self):
    self.m['jurisdiction']='Wales';self.m['dates']={'tax_effective_date':'2026-11-20'}
    self.assertEqual(deadlines(self.m)['deadlines'][0]['due_date'],'2026-12-20')
 def test_mr01(self):
    self.m['dates']={'company_charge_created':'2026-11-20'};self.m['specialist']={'uk_company_or_llp_borrower':True}
    self.assertEqual(deadlines(self.m)['deadlines'][0]['due_date'],'2026-12-11')
 def test_no_mr01_for_noncompany(self):
    self.m['dates']={'company_charge_created':'2026-11-20'}
    self.assertFalse(deadlines(self.m)['deadlines'])
 def test_auction_extension_preserves_both_dates(self):
    self.m['dates']={'contractual_completion':'2026-11-20','agreed_extended_completion':'2026-11-27'}
    keys=[x['key'] for x in deadlines(self.m)['deadlines']]
    self.assertEqual(keys,['completion_original','completion_extended'])
 def test_priority_requires_holidays(self):
    self.m['dates']={'priority_search_receipt':'2026-11-20'}
    self.assertIsNone(deadlines(self.m)['deadlines'][0]['due_date'])
 def test_priority_with_holidays(self):
    self.m['dates']={'priority_search_receipt':'2026-11-20','bank_holidays':[]}
    self.assertIsNotNone(deadlines(self.m)['deadlines'][0]['due_date'])
 def test_lender_working_notice_requires_holidays(self):
    self.m['dates']={'target_completion':'2026-11-27'}
    l={'notice':{'minimum':5,'unit':'working_days'}}
    self.assertIsNone(deadlines(self.m,l)['deadlines'][0]['due_date'])
 def test_lender_notice_with_holidays(self):
    self.m['dates']={'target_completion':'2026-11-27','bank_holidays':[]}
    l={'notice':{'minimum':5,'unit':'working_days'}}
    self.assertEqual(deadlines(self.m,l)['deadlines'][0]['due_date'],'2026-11-20')
 def test_invalid_date_refused(self):
    self.m['dates']={'tax_effective_date':'20/11/2026'}
    with self.assertRaises(MatterError):deadlines(self.m)
 def test_requirement_missing_evidence(self):
    self.m['requirements']=[{'id':'R1','description':'Submit insurance','status':'verified','blocking':True,'source_document_id':'D1','source_locator':'p.2'}]
    issues,summary=evaluate_requirements(self.m)
    self.assertTrue(any(x['id']=='LENDER-EVIDENCE-R1' for x in issues))
 def test_requirement_unproven_waiver(self):
    self.m['requirements']=[{'id':'R1','status':'waived_by_lender','source_document_id':'D1','source_locator':'p.2'}]
    self.assertTrue(any(x['severity']=='critical' for x in evaluate_requirements(self.m)[0]))
 def test_second_charge_blocker(self):
    self.m['securities']=[{'id':'P2','property_id':'P2','title_number':'ABC123','intended_rank':'second','charge_instrument_ref':'D-C'}]
    self.assertTrue(any(x['severity']=='critical' for x in security_preflight(self.m)))
 def test_accounting_balanced(self):
    self.m['financials']={'purchase_price':'102000','deposit_paid':'5100','seller_balance_stated':'96900',
        'lender_net_advance':'62000','client_funds_confirmed':'41300','costs_and_disbursements':'1400','tax_and_filing':'5000'}
    self.assertEqual(accounting(self.m)['state'],'reconciled_arithmetically_only')
    self.assertFalse(accounting(self.m)['approved_for_funds_release'])
 def test_accounting_discrepancy(self):
    self.m['financials']={'purchase_price':'102000','deposit_paid':'5100','seller_balance_stated':'97900',
        'lender_net_advance':'62000','client_funds_confirmed':'41000','costs_and_disbursements':'1400','tax_and_filing':'5000'}
    self.assertEqual(accounting(self.m)['state'],'discrepancy_or_funding_gap')
 def test_accounting_rejects_rounding(self):
    self.m['financials']={'purchase_price':'10.005','deposit_paid':'0','seller_balance_stated':'10',
        'lender_net_advance':'10','client_funds_confirmed':'0','costs_and_disbursements':'0','tax_and_filing':'0'}
    with self.assertRaises(MatterError):accounting(self.m)
 def test_registration_restriction(self):
    self.m['registration']={'application_type':'AP1','title_numbers':['ABC123'],'deeds_reviewed':True,'restrictions':[{'status':'unknown'}]}
    self.assertTrue(any(x['id']=='REG-RESTRICTION' for x in registration_preflight(self.m)))
 def test_execution_witness(self):
    self.m['execution']=[{'document_id':'D-TR1','execution_route':'director_with_witness','signatory_capacity':'director'}]
    self.assertTrue(any(x['id']=='EXEC-WIT-D-TR1' for x in execution_preflight(self.m)))
 def test_specialist_gates(self):
    self.m['specialist']={'leasehold':{'applicable':True},'tenancy':{'applicable':True}}
    self.assertGreaterEqual(len(specialist_preflight(self.m)),5)
 def test_no_silent_ready(self):
    x=review(self.m,{'lenders':[]})
    for k in ('ready_to_certify','ready_to_exchange','ready_to_release_funds','ready_to_file'):
        self.assertFalse(x[k])
 def test_case_lender_lookup_is_exact_brand(self):
    r=lender_lookup('Rely',{'lenders':[{'lender':'Rely Mortgages','aliases':['Rely']},{'lender':'Kent Reliance','aliases':['KRBS']}]})
    self.assertEqual([x['lender'] for x in r['matches']],['Rely Mortgages'])

class OutputTests(TestCase):
 def setUp(self):
    self.tmp=TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
    self.m=new_matter('ANON-123','England','purchase')
    self.m['fact_observations']={'property_address':[{'value':'1 <script>alert(1)</script> Street','document_id':'D1'}]}
    self.report=review(self.m)
 def test_drafts_never_sent(self):
    for kind in DRAFTS:
        x=draft(self.m,self.report,kind)
        self.assertIn('NOT APPROVED OR SENT',x['status']);self.assertIn('Authorised fee earner',x['body'])
 def test_html_escaped(self):
    html=html_dashboard(self.report)
    self.assertNotIn('<script>alert(1)</script>',html)
    self.assertIn('<main>',html)
 def test_markdown_report(self):self.assertIn('NO LEGAL SIGN-OFF',markdown_report(self.report).upper())
 def test_handoff_not_uploaded(self):
    f=self.root/'handoff.csv';r=export_handoff(self.report,str(f))
    self.assertEqual(r['remote_updates'],0);self.assertTrue(f.exists())
 def test_json_handoff(self):
    f=self.root/'handoff.json';export_handoff(self.report,str(f),'json')
    self.assertEqual(json.loads(f.read_text())['system'],'not_connected')
 def test_cli_init_and_review(self):
    f=self.root/'m.json'
    self.assertEqual(main(['init',str(f),'--matter-id','ANON-123','--jurisdiction','England','--transaction-type','purchase']),0)
    self.assertEqual(main(['review',str(f),'--output',str(self.root/'report.json')]),0)
    self.assertEqual(main(['audit',str(f)]),0)
 def test_cli_controlled_updates(self):
    f=self.root/'m.json';main(['init',str(f),'--matter-id','ANON-123','--jurisdiction','England','--transaction-type','purchase'])
    p=self.root/'patch.json';p.write_text(json.dumps({'dates':{'tax_effective_date':'2026-11-20'}}))
    self.assertEqual(main(['update-data',str(f),'--patch',str(p)]),0)
    self.assertEqual(verify_audit(f)['events'],2)
