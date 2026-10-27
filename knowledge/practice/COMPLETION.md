# Pre-completion, completion and post-completion

**Load when:** seller completion statement, funds reconciliation, pre-completion requisitions, notice to complete, mortgage redemption, completion undertakings, priority searches, Land Registry application or client closing letter.

## Pre-completion gate

Obtain approved contract, special conditions, price and deposit evidence, lender drawdown notice and confirmed settlement amount, client money bank confirmation, proof-of-funds sign-off, TA13/pre-completion requisitions, seller completion statement and verified bank destination (follow internal call-back controls). Verify title search freshness and priority (OS1/OS2), current bankruptcy search, mortgage redemption statements, lender report/condition decisions, insurance on risk, vacant possession/tenancy and correct execution of transfer and mortgage documents.

Reconcile **written** seller completion figures against contract: purchase price less exchange deposit, apportionments credited/debited according to agreed terms, auction fees/interest if actually due, retentions, VAT and any allowances. A solicitor must determine whether each term is contractually due; code only adds/subtracts instructed figures.

## Notice to complete

Read actual contract incorporated general and special conditions, exchange, original completion and notice dates, service route, times, business/calendar day definition, interest clause and whether time is of essence. Compute only after identifying these inputs; never apply a generic deadline to all auction contracts. Seller solicitor notice to complete is different from Land Registry completion notification and from contractual mortgage drawdown deadline. Keep a dated evidentiary timeline.

## Completion day: no autopilot

Only authorised conveyancer: confirm cleared client and lender funds, bank details, completion statement, lawful payment purpose, outstanding assurances/undertakings and possession. Do not send money or undertake release based on an AI checklist. On confirmation, record actual date/time, confirmation method, deed dating, keys release, insurance trigger and any gap in registration security.

## Post-completion

- SDLT or LTT return/payment based on correct effective date, not assumed completion if substantially performed earlier.
- DS1/e-DS1 discharge receipt/cancellation; register the transferee and lender security with correct fee/document bundle and maintain priority.
- Where UK company charge, separately complete Companies House MR01 within applicable statutory period; verify accepted certificate.
- Serve valid landlord/estate notices, deed of covenant and compliance certificates where applicable; pay evidenced fees.
- Check final official copy for accurate registered proprietor, estate, charges, restrictions, notices and lender priority. Inform lender/client of registration and residual risks.
- Reconcile client ledger and residual balances; record undertakings discharged, store final deeds and close file subject to retention policy.

## Calculations and safeguards

Use `conveyancing completion <json>` for deterministic Decimal reconciliation. Negative or unbalanced totals and missing cleared funds are flagged. Time utilities calculate **unadjusted statutory** deadlines with explicit holiday inputs where applicable. These computations are not a replacement for actual banking cut-offs, contract definitions or legal review.
