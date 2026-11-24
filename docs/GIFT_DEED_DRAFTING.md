# Deed of Gift drafting workflow (money, property transaction)

**Scope:** an original monetary Deed of Gift for a property purchase or remortgage in England and Wales. This is a supervised drafting convenience, not lender-approved wording, a declaration of trust, or a prescribed HMLR transfer.

## Source and output

- Word source: `templates/DEED_OF_GIFT_TEMPLATE.docx`. Maintains the user's two-page conventional format, clauses 1–8, recitals and donor/witness execution block. The template deliberately excludes donor birth dates and occupation and witness occupation. Donor and witness execution particulars remain blank.
- Input (private, never checked into the plugin): JSON following `examples/gift-deeds-fictional-example.json`. `donors` is an array: one deed is generated per donor, with individual amount and placeholders. For `donees`, supply names and residential addresses for each recipient.
- Optional local generator (requires the `documents` extras):

  ```sh
  pip install -e '.[documents]'
  conveyancing-gift-deeds --input /private/matter/gifts.json --output-dir /private/matter/draft-gifts --review-out /private/matter/gift-review.json
  ```

- The generator **never overwrites** existing deed files. Use a new output directory when revising. It reports missing donor residence, source-of-funds, account holder, bank name and bank identifiers. It never fills the execution date, signature, witness signature or witness name/address; those remain write-in lines.

## Supported structured fields

`transaction_type`: `purchase` or `remortgage`.

`recipient_allocation`: for two or more donees, set `"joint"` only when expressly instructed. Different allocations require manual drafting and legal review; the generator refuses to infer joint entitlement.

`property_address`: the exact supplied property address, required.

`donees`: list of `{ "name": "...", "address": "..." }`. One donee produces singular wording; two or more produce plural wording, with joint gift phrasing. Confirm the legally agreed allocation of gifts before relying on joint wording.

`donors`: list of objects with `name` and `amount` required; `address`, `source_of_funds` and `bank` optional. `bank` can hold `name`, `account_holder`, `account_number_iban`, `sort_code_swift_bic`. These are *administrative blanks*, not a substitute for source-of-funds verification.

`lender` (optional for remortgage): `{ "name": "...", "address": "...", "loan_description": "interest-only", "offer_date": "...", "loan_amount": "500000.00", "application_reference": "..." }`. This supplies recital data but does **not** determine whether a lender accepts a gift or whether exact loan wording should appear in the instrument. For purchases, lender details are deliberately excluded from recital A until the solicitor agrees the wording.

`output_prefix` (optional): alphanumeric, underscore or hyphen filename prefix, default `Deed_of_Gift`.

Amounts are GBP numeric strings or non-negative integral integers. Each gift must be positive and at most £999,999,999.99; fractional pence is refused, not rounded. Figures and English words are generated from the same decimal value. Ensure bank/source-of-funds fields and lenders' signed instructions are reviewed independently.

## Drafting and validation checklist

1. **Evidence:** Record origin and file IDs of lender offer, registration evidence, donor identity and statements, the exact gift instructions and independent advice/solicitor review when applicable. A file *name* is insufficient to confirm the title number or proprietor.
2. **Parties:** One donor per deed; identify all donees. Verify ownership, gift allocation, spelling, and source of the donor's funds. Never infer sibling relationship from a surname.
3. **Purpose:** Use purchase wording only for a purchase; use remortgage wording only for a remortgage. Do not silently convert one transaction into the other.
4. **Terms:** Check no loan, no repayment, no interest, no beneficial interest, no claim and suitable subordination to the lender. Confirm no undisclosed conditions, trust, private agreement or occupier interest contradict the deed.
5. **Lender-specific checks:** Review current UK Finance Handbook (if incorporated/applicable), relevant Part 2, mortgage offer, and any bespoke lender conditions. Do not present the deed as accepted, adequate or signed off without lender confirmation.
6. **Execution:** Section 1 of LP(MP)A 1989 requires valid execution and delivery by an individual and attestation by a witness in their presence for the usual signature route. HMLR PG8 describes legible witness name and address. A witness occupation is not included in this template. Check execution circumstances, genuine date, signatures, and any separate lender requirement.
7. **Visual QA:** Render each DOCX and inspect both pages, including whether the signature block is kept together and no orphaned lines or placeholders remain. Compare each deed with the user-supplied template and include a short change log.
8. **Completion gate:** A solicitor must sign off wording and lender requirements before the donor signs and delivery/use is authorised. The generator never verifies signing or funds.

**Source check:** legislation.gov.uk s.1 and GOV.UK HMLR practice guide 8 accessed on 20 November 2026. Re-check at point of use; no live legal verification is done by the offline generator.
