"""Read-only, source-aware public legal publication monitor.

Change detection is technical evidence for solicitor review, never an approval of
legal meaning, commencement, amended forms or a client transaction. No client
information is sent. Only allowlisted public HTTPS hosts may be fetched.
"""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler
from xml.etree import ElementTree

from .engine import load, LegalReviewRequired

HOSTS = {
    'www.gov.uk', 'gov.uk', 'www.legislation.gov.uk', 'legislation.gov.uk',
    'www.gov.wales', 'gov.wales', 'www.lawsociety.org.uk', 'lawsociety.org.uk',
    'www.sra.org.uk', 'sra.org.uk', 'www.ukfinance.org.uk', 'ukfinance.org.uk',
    'lendershandbook.ukfinance.org.uk', 'www.judiciary.uk', 'judiciary.uk',
    'www.gov.scot', 'www.bailii.org', 'bailii.org',
    'developers.openai.com', 'platform.claude.com', 'docs.anthropic.com',
    'cursor.com', 'geminicli.com', 'help.openai.com'
}
MAX_RESPONSE = 2_000_000
TIMEOUT = 8


def is_official_url(url: str) -> bool:
    try:
        p = urlparse(url)
        return (p.scheme == 'https' and p.hostname in HOSTS and
                p.username is None and p.password is None and
                p.port in (None, 443) and not p.fragment)
    except (TypeError, ValueError):
        return False


class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not is_official_url(newurl):
            raise LegalReviewRequired('Redirect outside approved HTTPS origin not followed')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _space(value):
    return re.sub(r'\s+', ' ', value).strip()


class _VisibleText(HTMLParser):
    """Prefer the publication body and skip repeated site-wide navigation."""
    SKIP = {'script', 'style', 'nav', 'header', 'footer', 'aside', 'form',
            'noscript', 'svg', 'iframe', 'template'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.all = []
        self.focus = []
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        desc = ' '.join(str(attrs.get(k, '')) for k in ('class', 'id', 'role')).lower()
        avoid = (tag in self.SKIP or any(word in desc for word in
                 ('cookie-banner', 'cookie-notice', 'global-header',
                  'global-footer', 'site-navigation', 'feedback-banner')))
        inherited = self.stack[-1][1] if self.stack else False
        skipped = avoid or inherited
        is_main = (tag in ('main', 'article') or attrs.get('role') == 'main') and not skipped
        self.stack.append((tag, skipped, is_main))
        self.depth += bool(is_main)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                for _, _, is_main in self.stack[i:]:
                    self.depth -= bool(is_main)
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.stack and self.stack[-1][1]:
            return
        text = _space(data)
        if text:
            self.all.append(text)
            if self.depth:
                self.focus.append(text)


def _canonical_html(raw):
    parser = _VisibleText()
    parser.feed(raw.decode('utf-8', errors='replace'))
    return _space(' '.join(parser.focus if len(parser.focus) > 10 else parser.all))


def _canonical_govuk_json(raw):
    item = json.loads(raw)
    details = item.get('details') or {}
    # Publishing API 'updated_at' and navigation 'links' can change without
    # changing the published guidance. Preserve publication date and body.
    document = {
        'title': item.get('title'), 'description': item.get('description'),
        'public_updated_at': item.get('public_updated_at'),
        'document_type': item.get('document_type'),
        'withdrawn_notice': item.get('withdrawn_notice'),
        'details': details,
    }
    return json.dumps(document, sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def _canonical_xml(raw):
    root = ElementTree.fromstring(raw)
    text = _space(' '.join(root.itertext()))
    return text


def _target(url):
    p = urlparse(url)
    if p.hostname in ('gov.uk', 'www.gov.uk') and not p.path.startswith('/api/'):
        return 'https://www.gov.uk/api/content' + p.path.rstrip('/'), 'govuk-content-v1'
    if p.hostname in ('legislation.gov.uk', 'www.legislation.gov.uk') and not p.path.endswith(('.xml', '.pdf')):
        return 'https://www.legislation.gov.uk' + p.path.rstrip('/') + '/data.xml', 'legislation-xml-v1'
    return url, 'publisher-content-v1'


def _read(url, opener):
    if not is_official_url(url):
        raise LegalReviewRequired('Not an allowlisted public source')
    req = Request(url, headers={
        'User-Agent': 'ConveyancingLegalSkill/0.4 (publication review only)',
        'Accept': 'application/json,application/xml,text/xml,text/html,application/pdf,text/plain',
    })
    with opener.open(req, timeout=TIMEOUT) as response:
        if not is_official_url(response.geturl()):
            raise LegalReviewRequired('Unapproved final origin')
        raw = response.read(MAX_RESPONSE + 1)
        if len(raw) > MAX_RESPONSE:
            raise LegalReviewRequired('Source too large to safely snapshot')
        return raw, response.headers.get('Content-Type', ''), response.status, response.headers.get('Last-Modified')


def _canonical(raw, ctype, mode):
    ctype = ctype.lower()
    if mode == 'govuk-content-v1':
        return _canonical_govuk_json(raw)
    if mode == 'legislation-xml-v1' or 'xml' in ctype:
        return _canonical_xml(raw)
    if 'pdf' in ctype or raw.startswith(b'%PDF-'):
        return raw
    if 'html' in ctype or raw.lstrip().startswith((b'<!DOCTYPE', b'<html', b'<HTML')):
        return _canonical_html(raw)
    return _space(raw.decode('utf-8', errors='replace'))


def _fetch_source(url, opener):
    preferred, mode = _target(url)
    try:
        raw, ctype, status, modified = _read(preferred, opener)
        canonical = _canonical(raw, ctype, mode)
        return preferred, mode, canonical, status, modified, False
    except (HTTPError, URLError, TimeoutError, ValueError, ElementTree.ParseError, json.JSONDecodeError):
        if preferred == url:
            raise
        # The structured API can legitimately lack a particular page. A
        # fallback is reported as degraded, not automatically equivalent.
        raw, ctype, status, modified = _read(url, opener)
        canonical = _canonical(raw, ctype, 'publisher-content-v1')
        return url, 'publisher-content-v1', canonical, status, modified, True


def watch(*, allow_network=False, baseline=None, limit=12):
    if type(limit) is not int or limit < 1:
        raise LegalReviewRequired('Source limit must be a positive integer')
    sources = [s for s in load('knowledge/legislation/source-index.json') if s.get('monitor')]
    previous = baseline if isinstance(baseline, dict) else {}
    now = datetime.now(timezone.utc).isoformat()
    opener = build_opener(SafeRedirect)
    result = {
        'checked_at_utc': now, 'network_enabled': bool(allow_network),
        'status': 'UNVERIFIED_SOURCE_WATCH', 'comparison_version': 2,
        'sources': [], 'legal_review_queue': [], 'source_access_queue': [],
        'summary': {},
        'note': 'A stable publication fingerprint is a technical signal, NOT proof of a legal amendment. No automatic approval or legal-rule change.',
    }
    for s in sources[:limit]:
        sid, url = s['id'], s['url']
        old = previous.get(sid)
        entry = {'source_id': sid, 'url': url, 'status': 'not_checked',
                 'old_sha256': old, 'legal_review_approved': False}
        if not is_official_url(url):
            entry['status'] = 'blocked_non_allowlisted_origin'
        elif not allow_network:
            entry['status'] = 'not_checked_network_disabled'
        else:
            try:
                used_url, mode, canonical, http_status, modified, fallback = _fetch_source(url, opener)
                buf = canonical if isinstance(canonical, bytes) else canonical.encode('utf-8')
                digest = sha256(buf).hexdigest()
                # Include representation/version in the baseline to avoid
                # falsely comparing an XML payload with the HTML fallback.
                fingerprint = mode + ':' + digest
                entry.update(status='fetched', sha256=fingerprint,
                             mode=mode, check_url=used_url, http_status=http_status,
                             last_modified=modified, degraded_fallback=fallback)
                if not old:
                    entry['comparison_status'] = 'first_baseline'
                elif old == fingerprint:
                    entry['comparison_status'] = 'unchanged'
                elif isinstance(old, str) and ':' not in old:
                    entry['comparison_status'] = 'legacy_baseline_migrated'
                    entry['review_note'] = 'Old raw-byte fingerprint replaced by structured comparison; prior manual-review backlog remains open.'
                elif str(old).split(':', 1)[0] != mode:
                    entry['comparison_status'] = 'representation_changed'
                    entry['review_note'] = 'Monitoring representation changed; not treated as a legal content change.'
                else:
                    entry['comparison_status'] = 'change_detected_review_required'
                    result['legal_review_queue'].append({
                        'source_id': sid, 'url': url, 'check_url': used_url,
                        'old_sha256': old, 'new_sha256': fingerprint,
                        'detected_at_utc': now, 'status': 'awaiting_legal_review',
                        'affected_modules': 'to be assessed', 'reviewer': None,
                        'decision': None, 'change': 'Publication-content fingerprint differs',
                        'action': 'Compare revisions, effect, territorial extent, commencement and rule/form version; solicitor approval required.'
                    })
            except HTTPError as exc:
                status = 'access_restricted' if exc.code in (401, 403) else 'fetch_failed'
                entry.update(status=status, http_status=exc.code, error=str(exc)[:180])
            except (URLError, TimeoutError, OSError, ValueError, LegalReviewRequired) as exc:
                entry.update(status='fetch_failed', error=str(exc)[:180])
            if entry['status'] in ('access_restricted', 'fetch_failed', 'blocked_non_allowlisted_origin'):
                result['source_access_queue'].append({
                    'source_id': sid, 'url': url, 'error': entry.get('error', entry['status']),
                    'status': 'manual_source_verification_required',
                    'action': 'Use publisher-approved access and manually verify; never bypass site controls or treat a failed fetch as unchanged law.'
                })
        result['sources'].append(entry)
    result['summary'] = {name: sum(row.get('comparison_status', row['status']) == name for row in result['sources'])
                         for name in ('first_baseline', 'unchanged', 'legacy_baseline_migrated',
                                      'representation_changed', 'change_detected_review_required',
                                      'access_restricted', 'fetch_failed', 'blocked_non_allowlisted_origin')}
    result['summary']['total_checked'] = len(result['sources'])
    return result
