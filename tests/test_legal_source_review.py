"""No network: checks review queue deduplication and mandatory human approval."""
import importlib.util
import pathlib
import unittest
from unittest.mock import patch

ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('legal_source_review', ROOT/'tools'/'legal_source_review.py')
review=importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
REPORT={'legal_review_queue':[{'source_id':'hmlr-pg8','url':'https://www.gov.uk/example','old_sha256':'A','new_sha256':'govuk-content-v1:BBB','detected_at_utc':'2026-11-24T00:00:00Z'}],
        'source_access_queue':[{'source_id':'ls-ta','url':'https://www.lawsociety.org.uk/x','error':'HTTP Error 403: Forbidden'}, {'source_id':'other','error':'The read operation timed out'}]}

class LegalSourceIssuesTests(unittest.TestCase):
    def test_review_only_restricted_sources_and_changes(self):
        result=review.sync(REPORT,repo='owner/repo',token='',dry_run=True)
        self.assertEqual([x['source_id'] for x in result['draft_issues']],['hmlr-pg8','ls-ta'])

    def test_no_token_means_no_write(self):
        with self.assertRaises(RuntimeError):
            review.sync(REPORT,repo='owner/repo',token='',dry_run=False)

    def test_new_issue_requires_human_checklist(self):
        title,body=review._new_issue('change',REPORT['legal_review_queue'][0])
        self.assertIn('Publication update',title)
        self.assertIn('solicitor approval',body)
        self.assertIn('no automatic amendment',body)
        self.assertIn('conveyancing-source-watch-v2',body)

    def test_repeat_observation_does_not_duplicate_issue(self):
        row=REPORT['legal_review_queue'][0]
        _,body=review._new_issue('change',row)
        existing={'number':3,'state':'open','body':body,'title':'some title'}
        calls=[]
        def fake_api(repo,token,method,suffix,data=None):
            calls.append((method,suffix))
            if suffix.startswith('issues?'):
                return [existing]
            return {'number':4,'body':data['body']}
        with patch.object(review,'_api',side_effect=fake_api):
            res=review.sync({'legal_review_queue':[row]},repo='owner/repo',token='dummy')
        self.assertEqual(res['unchanged'],1)
        self.assertEqual(calls,[('GET','issues?state=all&per_page=100&page=1')])

if __name__=='__main__':unittest.main()
