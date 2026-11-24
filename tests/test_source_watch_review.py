"""Regression tests for publication monitoring, security and manual-review gates."""
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from conveyancing_skill import source_watch as watchmod

SOURCE = {'id': 'hmlr-pg8', 'url': 'https://www.gov.uk/government/publications/execution-of-deeds', 'monitor': True}


class SourceWatchReviewTests(unittest.TestCase):
    def test_govuk_api_strips_dynamic_metadata(self):
        base = {'title':'Deeds', 'description':'Guidance', 'public_updated_at':'2026-11-10T00:00:00Z',
                'document_type':'guide', 'details':{'body':'A meaningful section'},
                'links':{'navigation':['random']}, 'updated_at':'2026-11-23T00:00:00Z'}
        next_page = dict(base, updated_at='2026-11-24T00:00:00Z', links={'navigation':['different']})
        x = watchmod._canonical_govuk_json(json.dumps(base).encode())
        y = watchmod._canonical_govuk_json(json.dumps(next_page).encode())
        self.assertEqual(x, y)
        next_page['details']={'body':'A legally changed paragraph'}
        self.assertNotEqual(x, watchmod._canonical_govuk_json(json.dumps(next_page).encode()))

    def test_html_excludes_scripts_navigation_and_cookie(self):
        a = b'<html><header>Menu A</header><nav>Links</nav><main><h1>Statutory text</h1><p>Binding provision</p></main><script>noise1</script></html>'
        b = a.replace(b'Menu A',b'Menu B').replace(b'noise1',b'noise2').replace(b'Links',b'Other')
        self.assertEqual(watchmod._canonical_html(a), watchmod._canonical_html(b))
        self.assertNotEqual(watchmod._canonical_html(a), watchmod._canonical_html(a.replace(b'Binding provision',b'Different provision')))

    def test_network_disabled_is_safe(self):
        with patch.object(watchmod, 'load', return_value=[SOURCE]):
            result = watchmod.watch(allow_network=False, limit=1)
        self.assertEqual(result['sources'][0]['status'], 'not_checked_network_disabled')
        self.assertFalse(result['legal_review_queue'])

    def test_first_and_legacy_baseline_have_no_false_alert(self):
        with patch.object(watchmod, 'load', return_value=[SOURCE]), patch.object(watchmod, '_fetch_source', return_value=(SOURCE['url'],'govuk-content-v1','corrected wording',200,None,False)):
            first=watchmod.watch(allow_network=True, limit=1)
            legacy=watchmod.watch(allow_network=True, baseline={SOURCE['id']:'a'*64}, limit=1)
            current=watchmod.watch(allow_network=True, baseline={SOURCE['id']:first['sources'][0]['sha256']}, limit=1)
        self.assertEqual(first['sources'][0]['comparison_status'], 'first_baseline')
        self.assertEqual(legacy['sources'][0]['comparison_status'], 'legacy_baseline_migrated')
        self.assertEqual(current['sources'][0]['comparison_status'], 'unchanged')
        self.assertFalse(first['legal_review_queue'])
        self.assertFalse(legacy['legal_review_queue'])
        self.assertFalse(current['legal_review_queue'])

    def test_real_change_produces_review_not_approval(self):
        with patch.object(watchmod, 'load', return_value=[SOURCE]), patch.object(watchmod, '_fetch_source', return_value=(SOURCE['url'],'govuk-content-v1','new operative words',200,None,False)):
            result=watchmod.watch(allow_network=True, baseline={SOURCE['id']:'govuk-content-v1:'+'b'*64},limit=1)
        self.assertEqual(result['summary']['change_detected_review_required'], 1)
        self.assertEqual(result['legal_review_queue'][0]['status'], 'awaiting_legal_review')
        self.assertFalse(result['sources'][0]['legal_review_approved'])
        self.assertEqual(result['sources'][0]['status'],'fetched')

    def test_representation_change_not_automatically_classified_as_law(self):
        with patch.object(watchmod, 'load', return_value=[SOURCE]), patch.object(watchmod, '_fetch_source', return_value=(SOURCE['url'],'publisher-content-v1','fallback text',200,None,True)):
            result=watchmod.watch(allow_network=True, baseline={SOURCE['id']:'govuk-content-v1:'+'a'*64},limit=1)
        self.assertEqual(result['sources'][0]['comparison_status'],'representation_changed')
        self.assertFalse(result['legal_review_queue'])

    def test_http_403_gets_manual_access_queue(self):
        def denied(*_args, **_kwargs):
            raise HTTPError(SOURCE['url'],403,'Forbidden',None,None)
        with patch.object(watchmod, 'load', return_value=[SOURCE]), patch.object(watchmod, '_fetch_source', side_effect=denied):
            result=watchmod.watch(allow_network=True,limit=1)
        self.assertEqual(result['sources'][0]['status'],'access_restricted')
        self.assertEqual(len(result['source_access_queue']),1)
        self.assertFalse(result['legal_review_queue'])

    def test_security_for_redirect_and_url(self):
        self.assertFalse(watchmod.is_official_url('http://www.gov.uk/x'))
        self.assertFalse(watchmod.is_official_url('https://www.gov.uk.evil.example/'))
        self.assertFalse(watchmod.is_official_url('https://www.gov.uk:999/x'))
        self.assertTrue(watchmod.is_official_url('https://www.gov.uk/api/content/government/publications/x'))
        handler=watchmod.SafeRedirect()
        with self.assertRaises(watchmod.LegalReviewRequired):
            handler.redirect_request(None,None,302,'Found',{},'https://unapproved.example/x')


if __name__=='__main__':
    unittest.main()
