#!/usr/bin/env python3
"""Deduplicate GitHub review issues from a technical source-watch report.

No approval, legal-rule edits, client data or privileged documents. Requires
GITHUB_TOKEN (issues:write) and GITHUB_REPOSITORY in GitHub Actions.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

API = 'https://api.github.com'
MARKER = 'conveyancing-source-watch-v2'


def _safe(value, limit=200):
    return str(value or '').replace('\r',' ').replace('\n',' ').replace('`','\'')[:limit]


def _api(repo, token, method, suffix, data=None):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
        raise ValueError('Invalid repository identifier')
    url = f'{API}/repos/{repo}/{suffix}'
    raw = None if data is None else json.dumps(data, ensure_ascii=False).encode('utf-8')
    req = Request(url, data=raw, method=method, headers={
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'ConveyancingLegalSkill/0.4 legal-review-queue',
        'Content-Type': 'application/json',
    })
    with urlopen(req, timeout=12) as response:
        data = response.read(2_000_000)
        return json.loads(data) if data else {}


def _list_issues(repo, token):
    results = []
    for page in range(1, 11):
        data = _api(repo, token, 'GET', f'issues?state=all&per_page=100&page={page}')
        results.extend(x for x in data if 'pull_request' not in x)
        if len(data) < 100:
            break
    return results


def _marker(kind, source_id):
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,96}', source_id):
        raise ValueError('Invalid source ID')
    return f'<!-- {MARKER}:{kind}:{source_id} -->'


def _new_issue(kind, row):
    sid = row['source_id']
    marker = _marker(kind, sid)
    fingerprint = _safe(row.get('new_sha256', 'none'), 120)
    if kind == 'change':
        title = f'[Legal source review] Publication update: {sid}'
        intro = 'The stable publication-content fingerprint differs from the last recorded technical baseline. This is NOT a confirmed statutory or regulatory change.'
    else:
        title = f'[Source access] Manual verification required: {sid}'
        intro = 'Automated retrieval was restricted (or the publisher could not be reached). No assertion is made that the law is unchanged.'
    lines = [marker, '', f'**Source ID:** `{sid}`', f'**Official URL:** {row.get("url", "")}',
             f'**Observed at (UTC):** {_safe(row.get("detected_at_utc"), 64) or datetime.now(timezone.utc).isoformat()}',
             f'**Latest fingerprint:** `{fingerprint}`', '', intro, '']
    if kind == 'change':
        lines += [f'**Earlier fingerprint:** `{_safe(row.get("old_sha256"), 120)}`',
                  f'**Technical check URL:** {row.get("check_url", row.get("url", ""))}', '']
    else:
        lines += [f'**Access error:** {_safe(row.get("error"), 400)}', '']
    lines += ['### Mandatory reviewer checklist',
              '- [ ] Obtain publisher-approved source text and verify its currency',
              '- [ ] Identify the exact provision, form edition, guidance change and publication date',
              '- [ ] Check territorial extent, commencement and transitional treatment',
              '- [ ] Compare affected rules, skills, search templates and practice modules',
              '- [ ] Record qualified solicitor approval (or decision that no legal change occurred)',
              '- [ ] If approved, propose source-backed changes in a tested PR and review plugin release separately',
              '- [ ] Record decision and close issue only after human review',
              '', '**Legal status:** Unverified; no automatic amendment, legal sign-off or client action.']
    return title, '\n'.join(lines)


def _review_items(report):
    # One open review per specific monitored source and class of issue.
    seen = set()
    for kind, key in (('change','legal_review_queue'), ('access','source_access_queue')):
        for row in report.get(key, []):
            sid = row.get('source_id')
            if not sid or (kind,sid) in seen:
                continue
            if kind == 'access' and not ('403' in str(row.get('error','')) or
                                           '401' in str(row.get('error','')) or
                                           'blocked' in str(row.get('error','')).lower()):
                # An isolated timeout is not a verified access restriction.
                continue
            seen.add((kind,sid))
            yield kind,row


def sync(report, *, repo, token, dry_run=False):
    items = list(_review_items(report))
    if dry_run:
        return {'draft_issues':[{'kind':kind,'source_id':row['source_id']} for kind,row in items], 'issues_created':0}
    if not token:
        raise RuntimeError('GITHUB_TOKEN required; no unauthenticated writes')
    existing = _list_issues(repo, token)
    counters = {'issues_created':0,'issues_updated':0,'unchanged':0,'review_items':len(items)}
    for kind,row in items:
        marker=_marker(kind,row['source_id'])
        title,body=_new_issue(kind,row)
        current=next((i for i in existing if marker in (i.get('body') or '')),None)
        if current is None:
            issue=_api(repo,token,'POST','issues',{'title':title,'body':body})
            existing.append(issue)
            counters['issues_created']+=1
        else:
            issue_no=current['number']
            fingerprint=_safe(row.get('new_sha256','none'),120)
            if fingerprint and f'**Latest fingerprint:** `{fingerprint}`' in (current.get('body') or '') and current.get('state')=='open':
                counters['unchanged']+=1
                continue
            if current.get('state') == 'closed':
                _api(repo,token,'PATCH',f'issues/{issue_no}',{'state':'open'})
            _api(repo,token,'POST',f'issues/{issue_no}/comments',{'body':
                f'New technical observation at {_safe(row.get("detected_at_utc"),80)}. Fingerprint: `{fingerprint}`. Review required; no automatic legal update.'})
            _api(repo,token,'PATCH',f'issues/{issue_no}',{'title':title,'body':body})
            current['body']=body
            current['state']='open'
            counters['issues_updated']+=1
    return counters


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path,required=True)
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args(argv)
    report=json.loads(args.report.read_text(encoding='utf-8'))
    repo=os.getenv('GITHUB_REPOSITORY','')
    if not repo and not args.dry_run:
        parser.error('GITHUB_REPOSITORY is missing')
    result=sync(report,repo=repo,token=os.getenv('GITHUB_TOKEN',''),dry_run=args.dry_run)
    print(json.dumps(result,indent=2))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
