# Publisher access exceptions: legal review required

These are source-level technical access restrictions, not legal determinations. Evidence: GitHub Actions reports from 2, 9, 16 and 23 November 2026.

| Source | Observed automated issue | Safe review approach |
|---|---|---|
| `ls-ta` | HTTP 403 on Law Society transaction forms information | Visit the Law Society's published guidance with permitted access. Obtain current edition from authorised licensee/firm provider; do not duplicate proprietary forms. |
| `ls-ta6` | HTTP 403 on Law Society TA6/TA7 guidance | Verify latest edition, effective CQS date and applicable transition using approved Law Society channel, then record signed review. |
| `uk-finance` | HTTP 403 on UK Finance Lenders' Handbook | Review current Parts 1/2/3 through the permitted UK Finance portal and the actual lender instruction; never infer lender consent from website cache. |
| `uk-finance-update` | Intermittent access, previously HTTP 403 | Manually check official published change notices; do not equate permitted access with an approved rule change. |

Never bypass restrictions through third-party mirrors as proof of current authoritative content. The automatic monitor should report these pages as `access_restricted` and open a manual-access issue; manual checks should remain pending until documented.
