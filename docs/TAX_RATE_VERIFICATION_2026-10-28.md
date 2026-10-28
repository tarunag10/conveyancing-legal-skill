# Residential SDLT and LTT rate verification

**Checked:** 28 October 2026  
**Scope:** the four basic residential rate tables in `knowledge/legislation/tax-rates.json`. The table values and effective dates were compared with the current official guidance and cited legislation. This is a dated research record, not solicitor approval or a tax opinion.

## Verified rate tables

Tax is calculated progressively on the portion of consideration in each band. Limits below are upper limits in pounds; the final row has no upper limit.

| Jurisdiction and table | Effective from | Upper limits | Rates |
|---|---:|---|---|
| England standard | 1 April 2025 | £125,000; £250,000; £925,000; £1,500,000 | 0%; 2%; 5%; 10%; 12% |
| England higher | 1 April 2025 | £125,000; £250,000; £925,000; £1,500,000 | 5%; 7%; 10%; 15%; 17% |
| Wales main residential | 10 October 2022 | £225,000; £400,000; £750,000; £1,500,000 | 0%; 6%; 7.5%; 10%; 12% |
| Wales higher residential | 11 December 2024 | £180,000; £250,000; £400,000; £750,000; £1,500,000 | 5%; 8.5%; 10%; 12.5%; 15%; 17% |

## Authorities and effective dates

- **England standard:** [HMRC residential rates](https://www.gov.uk/stamp-duty-land-tax/residential-property-rates) lists the current single-property table and says a 5% higher rate may apply if the buyer owns another residential property. The underlying residential table is in [Stamp Duty Land Tax Act 2015, section 1](https://www.legislation.gov.uk/ukpga/2015/1/section/1); the temporary nil-rate threshold changes ended on 31 March 2025.
- **England higher:** [HMRC higher rates guidance](https://www.gov.uk/guidance/stamp-duty-land-tax-buying-an-additional-residential-property) gives the current table and qualification guidance. [Finance Act 2025, section 51](https://www.legislation.gov.uk/ukpga/2025/8/section/51) substitutes the rates for effective dates on or after 1 April 2025 and includes contract-date exceptions. Those exceptions require a facts-and-contract review and are outside the calculator.
- **Wales main residential:** [Welsh Revenue Authority rates guidance](https://www.gov.wales/land-transaction-tax-rates-and-bands) gives the current table. [The 2022 Amendment Regulations, SI 2022/1027](https://www.legislation.gov.uk/wsi/2022/1027/made) brought the table into force on 10 October 2022 and provide transitional elections for certain earlier contracts or substantial performance.
- **Wales higher residential:** the same [WRA guidance](https://www.gov.wales/land-transaction-tax-rates-and-bands) lists the table from 11 December 2024. [The 2024 Amendment Regulations, SI 2024/1311](https://www.legislation.gov.uk/wsi/2024/1311/made) make the rate change and include a transition for contracts exchanged before that date. The calculator cannot determine that transition.

## Scope and exceptions

The calculator illustrates only a simple, unlinked, single residential purchase using one selected rate table. It does not decide whether standard or higher rates apply. A caller must not use `additional=True` as a substitute for checking the purchaser, related parties, ownership interests, trust or company status, dwelling use, contract and effective-date facts under the relevant statute and guidance.

Do not use this calculator where the answer may depend on first-time buyer or other relief, non-UK residence, a corporate flat rate, trusts or partnerships, multiple dwellings or linked transactions, mixed-use/non-residential property, lease premium or rent NPV, VAT/TOGC, anti-avoidance, a main-residence replacement/refund, contract-date transitional protection, or any other unusual facts. Refer those cases for current specialist review. Welsh higher rates are affected by contract exchange date; England higher rates may also be affected by a pre-31 October 2024 contract and statutory exceptions.

The metadata permits calculation only through the earlier of `last_verified_date` and `review_by`. It is currently verified through 28 October 2026 and review is due by 4 November 2026, so a requested date of 29 October or later is refused until the rates have been checked again and the metadata updated. Later changes can take effect before the review date, so the actual transaction date and official sources still need to be checked before reliance.

## Representative calculations

These calculations confirm implementation against the official guidance examples/rates; they do not determine legal eligibility:

- England standard, £295,000: £4,750.
- England higher, £300,000: £20,000.
- Wales main, £295,000: £4,200.
- Wales higher, £250,000: £14,950.

The engine adds no reliefs, surcharges or special rates to these totals.
