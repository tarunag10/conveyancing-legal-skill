# Remortgage reconciliation module

`conveyancing_skill.remortgage.reconcile_remortgage` provides a deterministic,
evidence-presence-gated calculation for gross and net advances, withheld lender
deductions, multiple intended securities, dated redemptions, client funds,
professional fees, VAT, disbursements and the balance.

## Relationship to the MetroLaw completion statement plugin

The separate MetroLaw Completion Statements plugin already includes a
remortgage workbook template, a synthetic JSON example, VAT and redemption
calculation rules, and `scripts/reconcile.py`. Do not duplicate or replace those
assets. Its arithmetic is useful for preparing the plugin output. This module
adds stricter checks where the existing script does not enforce each documentary
locator, exact intended security matching, deduction cross-references, and a
date-valid exact-day lender redemption figure. It can be called by a future
plugin adapter before populating the existing remortgage template.

The plugin's client-facing workbook and this module serve different purposes:
the plugin produces the statement in the approved layout; this module supplies
structured calculation and blockers. Retain the original template formatting
and payment warning when integrating the module.

## Input and control requirements

- Use decimal strings for GBP values. Each financial input needs a source
  reference and a precise page, line, cell or ledger locator.
- Itemise deductions from gross advance and compare the result with the lender's
  confirmed net remittance. Do not repeat a withheld deduction as a payment.
- List the securities intended to be redeemed with their own source reference
  and locator. Each redemption must map to one of those identifiers and be a
  lender quote valid for the actual completion date. The module does not
  extrapolate daily interest.
- Apply an explicit VAT treatment to each payment. VAT rates are accepted only
  for net taxable items. Reconcile calculated VAT to the approved invoice.
- Return blockers for missing human confirmations. The result never authorises
  issuing a statement, sending a payment instruction, releasing money or
  completing.

See `examples/remortgage-reconciliation-synthetic.json` and
`tests/test_remortgage.py`. All values and document references in that example
are fictional.
