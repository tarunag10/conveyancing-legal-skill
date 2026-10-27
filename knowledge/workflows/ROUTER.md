# Transaction router

Load the profile in `knowledge/workflows/profiles.json` matching the matter type, combined with the mandatory stage engine in `stages.json`. The CLI can render the combined workflow. Do not infer that a stage passed because it appears in a checklist.

| Trigger | Read |
|---|---|
| Register, charges, right of way, title plans, defects | `knowledge/practice/TITLE_REGISTERED.md` |
| Epitome, root, Land Charges, old mortgage, FR1 | `knowledge/practice/TITLE_UNREGISTERED.md` |
| Auction legal pack, special conditions, notice to complete | `knowledge/practice/AUCTIONS.md` |
| UK Finance / lender letter, company borrower, guarantee, ILA | `knowledge/practice/LENDERS_AND_ILA.md` |
| Leaseholds, LPE1, management pack, BSA, enfranchisement | `knowledge/practice/LEASEHOLD_AND_BUILDING_SAFETY.md` |
| VAT, option to tax, SDLT/LTT, commercial tenure | `knowledge/practice/COMMERCIAL_AND_TAX.md` |
| Completion funds, undertakings, redemption, notices | `knowledge/practice/COMPLETION.md` |
| Form AP1/FR1/TR1/TP1, company charge filings | `knowledge/practice/REGISTRATION.md` |
| New build, shared ownership, overseas owner, probate, trusts | `knowledge/practice/DEVELOPMENT_AND_SPECIAL.md` |

The generic stages apply to **every** matter, but can be marked not applicable only with recorded rationale and legal review. For a lender-only matter, check third-party borrower solicitor instructions and the UK Finance Part 3 if incorporated into that lender's instructions.
