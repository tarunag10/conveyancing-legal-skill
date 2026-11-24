---
name: gift-deeds
description: Draft, amend, or generate property-related Deeds of Gift of money for England and Wales purchases and remortgages, including separate deeds for multiple donors and lender conditions.
---

# Draft Deeds of Gift: supervised England and Wales conveyancing

**Authority hierarchy:** Follow the canonical repository `../../SKILL.md`, `core/OPERATING_STANDARD.md`, `core/EVIDENCE_AND_RISK.md`, `knowledge/practice/EVIDENCE_GIFTS_AND_LOANS.md` and `knowledge/practice/LENDERS_AND_ILA.md`. This skill concerns an original private monetary gift deed, NOT a prescribed HM Land Registry instrument or a verified lender-approved form.

## Use the reusable template

- Start with `templates/DEED_OF_GIFT_TEMPLATE.docx` and `docs/GIFT_DEED_DRAFTING.md`; preserve the original two-page deed layout and clauses unless instructed and reviewed otherwise. The template uses `{{UPPERCASE_FIELDS}}` tokens for donor, donees, property, amount, purchase/remortgage recitals and optional banking details.
- One donor per deed. For multiple donors, create a separate deed for each donor and reconcile the total. Distinguish one donee from multiple joint donees, including the correct defined terms and addresses; for more than one recipient the JSON must explicitly state `"recipient_allocation": "joint"`. Do not assume joint entitlement if instructions are silent.
- Optional local generator: `conveyancing-gift-deeds --input /approved/private/input.json --output-dir /approved/private/output --review-out /approved/private/review.json` (install with `pip install -e '.[documents]'`). Use only where local file tools are available; ChatGPT-only skill use does not grant a live Python executable.
- The generator's example is deliberately fictional: `examples/gift-deeds-fictional-example.json`. Never place live client instructions or bank details in the plugin archive or a public Git repository.

## Required evidence and drafting gates

1. Record donor's actual full name, residential address or dotted placeholder, recipient(s) and address(es), gift amount (figures and words), property, purchase/remortgage purpose, intended recipient shares/joint entitlement, and basis of any existing or proposed security. Date, donor signature and witness signature are NEVER pre-filled.
2. For a lender-involved transaction verify the actual lender identity, offer and date, reference, loan and any special gift wording against the supplied offer and current lender instructions. A lender's acceptance is not inferred from this template or a covering email. Do not insert an unverified title number from a filename.
3. Leave missing donor residence, source-of-funds and bank fields as dotted spaces. Do not invent DOB, donor occupation or witness occupation: none of those fields appears in this template. Identity and AML checks remain outside the deed under the firm's approved policy; a blank field is not approval.
4. Verify the asserted gift is unconditional, nonrepayable, nonborrowed, and does not create an interest in the Property. Identify any inconsistency with a loan, condition, third-party funding, financial contribution arrangement, occupier claim, interest or insolvency concern and escalate before presenting it as an outright gift.
5. Confirm donor advice expectations and any conflicts, lender disclosures, tax/insolvency referrals and possible donor withdrawal/return of funds terms. The declaration that the donor was advised to obtain independent advice must not be treated as proof that advice was actually given.
6. The donor must validly execute and deliver the deed, with an attesting witness where the individual execution route applies. Leave donor and witness signatures, full witness name/address and date for actual completion. Consult the current [Law of Property (Miscellaneous Provisions) Act 1989, s.1](https://www.legislation.gov.uk/ukpga/1989/34/section/1) and [HMLR practice guide 8](https://www.gov.uk/government/publications/execution-of-deeds/practice-guide-8-execution-of-deeds) at point of use, along with any specific lender signing requirements.
7. Render and inspect the generated Word document page by page. Check each name, address, figures/words, lender, recital, gift allocation, defined terms and signature panel; report outstanding fields and provide a concise clause change log if revising an earlier deed. No automated delivery, signature, lender approval or legal sign-off.

## Final output

Provide editable `.docx` deeds (one per donor), the blank template when requested, a gift-total reconciliation, and a review report distinguishing facts from unverified instructions or dotted fields. Keep client-specific outputs in an approved confidential environment; this plugin stores only the blank template and fictional example.
