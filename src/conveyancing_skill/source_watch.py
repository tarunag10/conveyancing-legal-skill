"""Allowlisted read-only public-source change detection, never automatic legal approval.

Network is opt-in, one official URL at a time, low-rate, timeout and content cap.
No confidential material is ever sent.
"""
from __future__ import annotations
from datetime import datetime,timezone
from hashlib import sha256
from urllib.parse import urlparse
from urllib.request import Request,build_opener,HTTPRedirectHandler
from .engine import load, LegalReviewRequired

HOSTS={'www.gov.uk','gov.uk','www.legislation.gov.uk','legislation.gov.uk','www.gov.wales','gov.wales','www.lawsociety.org.uk','lawsociety.org.uk','www.sra.org.uk','sra.org.uk','www.ukfinance.org.uk','ukfinance.org.uk','www.gov.uk','www.judiciary.uk','judiciary.uk','www.gov.scot','www.bailii.org','bailii.org','developers.openai.com','platform.claude.com','docs.anthropic.com','cursor.com','geminicli.com','help.openai.com','lendershandbook.ukfinance.org.uk'}

def is_official_url(url: str) -> bool:
    parsed=urlparse(url)
    return parsed.scheme=='https' and parsed.hostname in HOSTS


class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not is_official_url(newurl):
            raise LegalReviewRequired('Redirect outside approved HTTPS origin not followed')
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def watch(*, allow_network=False, baseline=None, limit=12):
    sources=[s for s in load('knowledge/legislation/source-index.json') if s.get('monitor')]
    now=datetime.now(timezone.utc).isoformat()
    previous=baseline if isinstance(baseline,dict) else {}
    result={'checked_at_utc':now,'network_enabled':allow_network,'status':'UNVERIFIED_SOURCE_WATCH','sources':[],'legal_review_queue':[]}
    for s in sources[:limit]:
        entry={'source_id':s['id'],'url':s['url'],'status':'not_checked','old_sha256':previous.get(s['id'])}
        if not is_official_url(s['url']):
            entry.update(status='blocked_non_allowlisted_origin')
        elif not allow_network:
            entry.update(status='not_checked_network_disabled')
        else:
            try:
                req=Request(s['url'],headers={'User-Agent':'ConveyancingLegalSkill/0.1 (+human review required)','Accept':'text/html,application/pdf,text/plain'})
                with build_opener(SafeRedirect).open(req,timeout=8) as resp:
                    if urlparse(resp.geturl()).hostname not in HOSTS:
                        raise LegalReviewRequired('Redirected to unapproved host')
                    raw=resp.read(2_000_001)
                    if len(raw)>2_000_000: raise LegalReviewRequired('Source too large to safely snapshot')
                    digest=sha256(raw).hexdigest()
                    entry.update(status='fetched',http_status=resp.status,sha256=digest,last_modified=resp.headers.get('Last-Modified'),etag=resp.headers.get('ETag'))
                    if previous.get(s['id']) and previous[s['id']]!=digest:
                        entry['status']='change_detected_review_required'
                        result['legal_review_queue'].append({'source_id':s['id'],'change':'HTTP content hash differs','action':'Compare official publication, amendments, commencement and affected rules; have solicitor approve; never auto-promote'})
            except Exception as exc:
                entry.update(status='fetch_failed',error=str(exc)[:180])
        result['sources'].append(entry)
    result['note']='Content hashes detect technical differences, not necessarily legislative changes. Baseline approval is a separate supervised step. Weekly workflow must be activated in GitHub after push.'
    return result
