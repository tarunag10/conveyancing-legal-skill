"""Build curated public-reference indexes. Dates mean publisher listing checked, NOT binary form inspection.
No connection to client files. All entries require fresh use-point checks and legal review.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
D='2026-10-27'

def write(name, value):
    path=ROOT/name;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n', encoding='utf8')

SOURCES = [
('hmlr-forms','HM Land Registry forms directory','https://www.gov.uk/government/collections/hm-land-registry-forms','official_guidance','England and Wales','Forms as publisher listed, including 26 October 2026 CIT form; file binary revisions not examined'),
('hmlr-guides','HM Land Registry practice guide collection','https://www.gov.uk/government/collections/land-registration-practice-guides','official_guidance','England and Wales','Updated 26 October 2026, including PG84'),
('hmlr-pg1','Practice guide 1: first registrations','https://www.gov.uk/government/publications/first-registrations/practice-guide-1-first-registrations','official_guidance','England and Wales','Form FR1, DL duplicate, supporting root, plan, lease'),
('hmlr-pg8','Practice guide 8: execution of deeds','https://www.gov.uk/government/publications/execution-of-deeds/practice-guide-8-execution-of-deeds','official_guidance','England and Wales','Updated 14 September 2026; prescribed attestation clauses'),
('hmlr-pg12','Practice guide 12: official searches','https://www.gov.uk/government/publications/official-searches-and-outline-applications/practice-guide-12-official-searches-and-outline-applications','official_guidance','England and Wales','Priority period normally ends 30th working day under LRR 2003 rule 131'),
('hmlr-pg19','Practice guide 19: notices and restrictions','https://www.gov.uk/government/publications/notices-restrictions-and-protection-of-third-party-interests-pg19/practice-guide-19-notices-restrictions-and-the-protection-of-third-party-interests-in-the-register','official_guidance','England and Wales','LRA 2002 ss32 and 40'),
('hmlr-pg31','Practice guide 31: discharge of charges','https://www.gov.uk/government/publications/discharge-of-charges-pg31/practice-guide-31-discharges-of-charges','official_guidance','England and Wales','Updated 1 June 2026'),
('hmlr-pg63','Practice guide 63: Land Charges','https://www.gov.uk/government/publications/the-land-charges-registers-and-agricultural-credits-register-registration-official-search-office-copy-and-cancellation-pg63/practice-guide-63-land-charges-applications-for-registration-official-search-office-copy-and-cancellation','official_guidance','England and Wales','Land Charges K15/K16; K15 includes bankruptcy register'),
('hmlr-pg78','Practice guide 78: overseas entities','https://www.gov.uk/government/publications/overseas-entities-pg78/practice-guide-78-overseas-companies-and-limited-liability-partnerships','official_guidance','England and Wales','Updated 21 September 2026; overseas companies, registration constraints'),
('hmlr-fees','HM Land Registry Registration Services fees','https://www.gov.uk/guidance/hm-land-registry-registration-services-fees','official_guidance','England and Wales','Published fee schedule says effective 9 Dec 2024; confirm fee route and scale per transaction'),
('hmlr-tr1','Form TR1 and guide','https://www.gov.uk/government/publications/registered-titles-whole-transfer-tr1','official_form','England and Wales','TR1 page updated 23 January 2024'),
('hmlr-tr1-guide','Completing TR1','https://www.gov.uk/government/publications/registered-titles-whole-transfer-tr1/guidance-completing-form-tr1-for-the-transfer-of-registered-property','official_guidance','England and Wales','Panel 7 must not be amended; date on completion; AP1/FR1'),
('hmlr-ap1','Form AP1','https://www.gov.uk/government/publications/change-the-register-ap1','official_form','England and Wales','Page last updated 23 December 2025'),
('hmlr-fr1','Form FR1','https://www.gov.uk/government/publications/first-application-registration-fr1','official_form','England and Wales','Page updated 18 March 2026'),
('hmlr-ch1','Form CH1','https://www.gov.uk/government/publications/legal-charges-registration-ch1','official_form','England and Wales','Form listed 29 August 2023'),
('hmlr-tp1','Form TP1','https://www.gov.uk/government/publications/registered-titles-part-transfer-tp1','official_form','England and Wales','Form listed 29 August 2023'),
('hmlr-os1','Form OS1','https://www.gov.uk/government/publications/official-search-with-priority-whole-title-os1','official_form','England and Wales','Form listed 28 February 2022'),
('hmlr-k15','Form K15','https://www.gov.uk/government/publications/land-charges-official-search-application-k15','official_form','England and Wales','Form updated 13 April 2026; searches only from 1855'),
('ls-ta','Law Society Transaction (TA) forms','https://www.lawsociety.org.uk/Topics/Property/Tools/Transaction-forms','licensed_form_guidance','England and Wales','Page 24 June 2026; CQS mandates TA6 sixth/TA7 fifth for new instructions from 30 March 2026; provider-licensed'),
('ls-ta6','TA6 sixth edition and TA7 fifth edition guidance','https://www.lawsociety.org.uk/topics/property/ta6-6th-edition','licensed_form_guidance','England and Wales','New CQS matters 30 March 2026; TA6 not designed for new-build or unmodified auctions'),
('uk-finance','UK Finance Mortgage Lenders Handbook','https://lendershandbook.ukfinance.org.uk/','contractual_instructions','England and Wales','Parts 1, 2 lender-specific, and 3 where lender-only; voluntary; newer platform from 29 June 2026'),
('uk-finance-update','UK Finance Handbook platform changes','https://www.ukfinance.org.uk/mortgage-lenders-handbook-update','professional_reference','England and Wales','Platform launched 29 June 2026; cannot reproduce proprietary lender content'),
('sdlt-res','HMRC SDLT residential rates','https://www.gov.uk/stamp-duty-land-tax/residential-property-rates','tax_guidance','England','Base rates from 1 Apr 2025; check current date and surcharges'),
('sdlt-higher','HMRC higher SDLT rates','https://www.gov.uk/guidance/stamp-duty-land-tax-buying-an-additional-residential-property','tax_guidance','England','5 percentage point surcharge qualifying additional dwellings from 1 Apr 2025'),
('sdlt-returns','HMRC SDLT return','https://www.gov.uk/guidance/check-if-you-need-to-send-a-stamp-duty-land-tax-return','tax_guidance','England','Usually within 14 days of effective transaction date'),
('sdlt-pay','HMRC SDLT payment rules','https://www.gov.uk/guidance/pay-stamp-duty-land-tax','tax_guidance','England','14 days; payment deadline weekend/bank holiday guidance'),
('wra-rates','WRA land transaction tax rates','https://www.gov.wales/land-transaction-tax-rates-and-bands','tax_guidance','Wales','2022 basic; 11 Dec 2024 higher residential rates'),
('wra-returns','WRA returns and payments technical guidance','https://www.gov.wales/land-transaction-tax-returns-and-payments-technical-guidance','tax_guidance','Wales','Section 44: 30 calendar days beginning the day after effective date'),
('vat-togc','HMRC VAT Notice 700/9 TOGC','https://www.gov.uk/guidance/transfer-a-business-as-a-going-concern-and-vat-notice-7009','tax_guidance','United Kingdom','TOGC mandatory if conditions satisfied; property and option-to-tax requirements must be checked'),
('co-mr01','Companies House filing MR01','https://www.gov.uk/government/publications/register-particulars-of-a-charge-mr01/how-to-complete-paper-form-mr01','official_guidance','United Kingdom','21 days beginning day after charge creation; signed instrument certified copy'),
('co-charge','Companies House register a charge','https://www.gov.uk/guidance/register-a-charge-mortgage-for-a-limited-company','official_guidance','United Kingdom','Late registration may require court order'),
('sra-accounts','SRA Accounts Rules','https://www.sra.org.uk/solicitors/standards-regulations/accounts-rules/','regulator_rules','England and Wales','Client money handling rules'),
('bsa-deed','Leaseholder deed of certificate','https://www.gov.uk/guidance/leaseholder-protections-deed-of-certificate-frequently-asked-questions','official_guidance','England','Qualifying leaseholder protections; landlord notice may trigger requirement'),
('bsa-mandatory','Landlord and leaseholder certificate requirements','https://www.gov.uk/guidance/mandatory-information-required-from-leaseholders-and-building-owners','official_guidance','England','BSA certificates; correct factual qualifying status'),
('leasehold-toolkit','Leasehold toolkit England','https://www.gov.uk/government/publications/leasehold-toolkit/leasehold-toolkit-england','official_guidance','England','Commenced reforms distinguished from prospective reform'),
('leasehold-prospective','Leasehold 2024 reform consultation','https://www.gov.uk/government/consultations/leasehold-enfranchisement-valuation-rates/plain-english-explainer-extending-your-lease-or-buying-your-freehold-its-getting-cheaper-and-easier','official_policy','England and Wales','Key 990-year and marriage-value reforms not assumed in force'),
('lp-1925-s52','Law of Property Act 1925 s52','https://www.legislation.gov.uk/ukpga/Geo5/15-16/20/section/52','legislation','England and Wales','Conveyance by deed subject to exceptions'),
('lpmp-1989-s2','LP(MP)A 1989 s2','https://www.legislation.gov.uk/ukpga/1989/34/section/2','legislation','England and Wales','Contract for disposition must be signed writing incorporating terms'),
('lra-2002-s27','Land Registration Act 2002 s27','https://www.legislation.gov.uk/ukpga/2002/9/section/27','legislation','England and Wales','Dispositions required to be completed by registration'),
('ca-2006-s44','Companies Act 2006 s44','https://www.legislation.gov.uk/ukpga/2006/46/section/44','legislation','United Kingdom','Company execution two authorised signatories or director witnessed'),
('ca-2006-s46','Companies Act 2006 s46','https://www.legislation.gov.uk/ukpga/2006/46/section/46','legislation','United Kingdom','Delivery as deed'),
('lfr-2024','Leasehold and Freehold Reform Act 2024','https://www.legislation.gov.uk/ukpga/2024/22/contents','legislation','England and Wales','Royal Assent alone not commencement; verify provision and start date')
]

# Supplementary official filing material verified on 27 October 2026.
SOURCES.extend([
 ('co-mr01-form','Companies House MR01 form and official filing landing page','https://www.gov.uk/government/publications/register-particulars-of-a-charge-mr01','official_form','United Kingdom','Page updated 5 March 2026; version of downloadable PDF not independently hash-validated'),
 ('co-charge-forms','Companies House security registration and release forms','https://www.gov.uk/government/collections/forms-for-mortgages-and-loans','official_form','United Kingdom','Forms MR01, MR02, MR04, MR05, MR06, MR07, MR08, MR09, MR10; actual binary revisions not independently checked'),
 ('sdlt-filing-guide','HMRC guidance on online and paper SDLT returns','https://www.gov.uk/guidance/how-to-send-a-stamp-duty-land-tax-return','tax_guidance','England','Published 26 June 2026; representatives should file online through HMRC Stamp Taxes service; unrepresented paper return exceptions'),
 ('sdlt1-guidance','HMRC SDLT1 paper return instructions','https://www.gov.uk/government/publications/sdlt-guide-for-completing-paper-sdlt1-return','official_form_guidance','England','Updated 20 February 2026; official scanner requires original UTRN-bearing form'),
 ('wra-file-ltt','Welsh Revenue Authority: file Land Transaction Tax','https://www.gov.wales/file-land-transaction-tax','tax_guidance','Wales','Online professional LTT service; unrepresented taxpayer paper return via WRA'),
 ('hmlr-pg2','HMLR Practice Guide 2: lost or destroyed deeds','https://www.gov.uk/government/publications/first-registration-of-title-where-deeds-have-been-lost-or-destroyed/practice-guide-2-first-registration-of-title-if-deeds-are-lost-or-destroyed','official_guidance','England and Wales','Updated 20 July 2026; FR1 DL ST3, original/reconstructed title and evidence of possession'),
 ('hmlr-pg21','HMLR Practice Guide 21: complex and unusual transfer forms','https://www.gov.uk/government/publications/using-transfer-forms-for-less-straightforward-transactions/practice-guide-21-using-our-forms-for-complex-and-more-unusual-transactions','official_guidance','England and Wales','Updated 7 September 2026; transfer forms where more than one title or more complex circumstances'),
 ('hmlr-pg67','HMLR Practice Guide 67: evidence of identity','https://www.gov.uk/government/publications/evidence-of-identity-conveyancers/practice-guide-67-evidence-of-identity-conveyancers','official_guidance','England and Wales','Updated 1 September 2026; when ID1, ID2, ID3 or ID5 evidence is required'),
 ('hmlr-pg26','HMLR Practice Guide 26: leases determination','https://www.gov.uk/government/publications/leases-determination-pg26/practice-guide-26-leases-determination','official_guidance','England and Wales','Updated 14 September 2026; surrenders, mergers and registration of determination'),
])
sources=[]
for sid,title,url,kind,jur,note in SOURCES:
    sources.append(dict(id=sid,title=title,url=url,authority_type=kind,jurisdiction=jur,last_verified_date=D,verification_status='official_source_checked',scope_note=note,monitor=True,licence='publisher terms apply; reference/link only',effective_date=None))
write('knowledge/legislation/source-index.json',sources)

# Each rule is independently traceable and does NOT signify that a whole Act was reviewed.
RULE_ROWS=[
('r-land-contract','LP(MP)A 1989 s2 requires written signed contract containing expressly agreed terms','lpmp-1989-s2','section 2','binding_law','England and Wales','1989-09-27','in_force','Exceptions and variation/factual construction require verification'),
('r-deeds','Conveyance of legal estates generally requires a deed, subject to s52(2) exceptions','lp-1925-s52','section 52(1) and (2)','binding_law','England and Wales','1926-01-01','in_force','Determine whether an exception applies'),
('r-registration','A registrable disposition of registered land does not operate at law until registration','lra-2002-s27','section 27(1)-(2)','binding_law','England and Wales','2003-10-13','in_force','Type of disposition and exceptions require review'),
('r-firstreg-dl','FR1 requires DL in duplicate and relevant supporting title documents','hmlr-pg1','4.4.1 and rule 24(1)(d) LRR 2003','official_guidance','England and Wales',None,'applicable_guidance','First registration may require original supporting documents, root, plan, leases'),
('r-restriction','Restrictions condition registration; notices protect interests differently','hmlr-pg19','sections 1 and 3; LRA 2002 sections 32,40','official_guidance','England and Wales',None,'applicable_guidance','Identify specific register wording and evidence to comply'),
('r-search-priority','Official search protection ends after 30th working day after receipt','hmlr-pg12','5.2; LRR 2003 rule 131','official_guidance','England and Wales',None,'applicable_guidance','Calculate from actual day-list receipt and applicable working-day calendar'),
('r-discharge','Discharge route depends on type of charge and electronic/paper evidence','hmlr-pg31','1 and 3.2.1','official_guidance','England and Wales',None,'applicable_guidance','For equitable charge endorsed receipt may be sufficient in circumstances; cannot generalise'),
('r-execution','HM Land Registry prescribed deeds require applicable prescribed execution words','hmlr-pg8','1.2, 1.3 and 15','official_guidance','England and Wales',None,'applicable_guidance','Individuals, companies, attorneys and overseas entities differ'),
('r-tr1-prescribed','TR1 panel 7 must not be amended; panel 3 is completion date','hmlr-tr1-guide','3.3 and 3.7','official_guidance','England and Wales',None,'applicable_guidance','Do not fill completion date in advance'),
('r-company-sign','Company document may be executed by two authorised signatories or director before attesting witness','ca-2006-s44','section 44(1)-(3)','binding_law','England and Wales',None,'in_force','Deed also requires delivery; company identity/capacity and other cases vary'),
('r-company-deed','For company deed execution, valid execution and delivery as deed both required','ca-2006-s46','section 46','binding_law','England and Wales',None,'in_force','Never equate company signature scan to delivered deed'),
('r-mr01','Companies House charge registration generally within 21 days beginning day after creation','co-mr01','When to file','official_guidance','United Kingdom',None,'applicable_guidance','Refer Companies Act 2006 Part 25 and qualifying exceptions'),
('r-sdlt-window','SDLT return/payment ordinarily due within 14 days of effective date','sdlt-returns','When you need to send a return','tax_guidance','England',None,'applicable_guidance','Determine notifiability and substantial performance; Northern Ireland also uses SDLT but out of skill scope'),
('r-ltt-window','LTT return for notifiable Welsh land transaction within 30 calendar days after effective date','wra-returns','LTTA/6010 section 44','tax_guidance','Wales',None,'applicable_guidance','Payment, return exemptions and effective date fact-specific'),
('r-sdlt-main','SDLT basic residential bands from 1 April 2025 are 0, 2, 5, 10 and 12 per cent','sdlt-res','Rates for a single property','tax_guidance','England','2025-04-01','published_as_applicable','Reliefs, surcharges, corporate and lease cases excluded from simple calculator'),
('r-wra-main','Welsh LTT main residential rates are 0,6,7.5,10,12 per cent at stated bands','wra-rates','Main residential tax rates','tax_guidance','Wales','2022-10-10','published_as_applicable','Wales has distinct higher rates, reliefs and transaction categories'),
('r-togc','Qualifying TOGC treatment is compulsory, cannot be chosen out of by contract','vat-togc','2.1-2.3.2','tax_guidance','United Kingdom',None,'applicable_guidance','Check actual business transfer, option to tax, dates and VAT registration; specialist advice'),
('r-lender-parts','Use UK Finance Part 1 and applicable lender Part 2; Part 3 if separate lender representation','uk-finance','Handbook homepage','contractual_instructions','England and Wales',None,'conditional_on_lender','Not every lender uses this handbook and all instruction versions are matter-specific'),
('r-law-society-ta6','CQS firms must use TA6 6th and TA7 5th for new matters instructed from 30 March 2026','ls-ta6','Complying with CQS','scheme_requirement','England and Wales','2026-03-30','applicable_scheme','Not a universal statutory requirement; limited older matter transitional use'),
('r-building-doc','England qualifying leaseholder may need landlord certificate and/or leaseholder deed of certificate','bsa-mandatory','Summary 1-3, 6-10,18-21','official_guidance','England',None,'conditional','Check building height, defect, leaseholder status, date and landlord parties'),
('r-lease-reform','Major 2024 enfranchisement valuation reforms are not wholly commenced','leasehold-prospective','When will changes go live','official_policy','England and Wales',None,'not_assumed_in_force','Check specific section and commencement order before relying'),
]
rules=[]
source_by_id={s['id']:s for s in sources}
for rid,summary,sid,clause,char,jur,effective,application,transition in RULE_ROWS:
    a=source_by_id[sid]
    rules.append(dict(id=rid,proposition=summary,source_id=sid,authority_url=a['url'],reference=clause,authority_type=char,jurisdiction=jur,effective_date=effective,applicability=application,transitional_or_scope_note=transition,last_verified_date=D,verification_status='checked_at_reference_date',legal_reviewer_approved=False))
# Important Acts indexed but individual sections deliberately unverified.
for rid,label,url in [
('act-land-charges-1972','Land Charges Act 1972','https://www.legislation.gov.uk/ukpga/1972/61/contents'),
('act-lrr-2003','Land Registration Rules 2003','https://www.legislation.gov.uk/uksi/2003/1417/contents'),
('act-lta-1985','Landlord and Tenant Act 1985','https://www.legislation.gov.uk/ukpga/1985/70/contents'),
('act-lta-1987','Landlord and Tenant Act 1987','https://www.legislation.gov.uk/ukpga/1987/31/contents'),
('act-lrhu-1993','Leasehold Reform Housing and Urban Development Act 1993','https://www.legislation.gov.uk/ukpga/1993/28/contents'),
('act-bsa-2022','Building Safety Act 2022','https://www.legislation.gov.uk/ukpga/2022/30/contents'),
('act-lfra-2024','Leasehold and Freehold Reform Act 2024','https://www.legislation.gov.uk/ukpga/2024/22/contents'),
('act-lpmp-1994','Law of Property Miscellaneous Provisions Act 1994','https://www.legislation.gov.uk/ukpga/1994/36/contents'),
('act-ltta-2017','Land Transaction Tax and Anti-avoidance of Devolved Taxes (Wales) Act 2017','https://www.legislation.gov.uk/anaw/2017/1/contents'),
('act-fa-2003','Finance Act 2003 SDLT Part 4','https://www.legislation.gov.uk/ukpga/2003/14/part/4'),
('act-lta-1954','Landlord and Tenant Act 1954','https://www.legislation.gov.uk/ukpga/Eliz2/2-3/56/contents'),
('act-ca-2006','Companies Act 2006','https://www.legislation.gov.uk/ukpga/2006/46/contents'),
]:
    rules.append(dict(id=rid,proposition=f'Legislative scope index only: {label}',source_id=None,authority_url=url,reference='provision-by-provision analysis required',authority_type='legislation',jurisdiction='verify extent per provision',effective_date=None,applicability='NOT VERIFIED FOR CURRENT MATTER',transitional_or_scope_note='Listed for research, not a verified operative proposition; assess amendments, commenced provisions, savings and territorial extent',last_verified_date=None,verification_status='needs_provision_verification',legal_reviewer_approved=False))
write('knowledge/legislation/rules.json',rules)

FORM_ROWS='''ACD|Standard form of charge: approval|2025-09-01
ADD|Standard form deed of variation/priority/postponement of a charge: approval|2022-08-22
ADV1|Adverse possession: registration|2023-08-29
ADV2|Adverse possession: notification|2023-08-29
AN1|Agreed notice: registration|2026-01-06
AP1|Change the register|2025-12-23
AS1|Whole of registered title: assent|2024-04-22
AS2|Charge (mortgage): assent|2024-04-22
AS3|Part of registered title: assent|2024-04-22
CH1|Legal charges: registration|2023-08-29
CH2|Legal charges: obligation for further advances|2018-05-25
CH3|Legal charges: security|2018-05-25
CIT|Investigation or enforcement proceedings (court, insolvency, tax)|2026-10-26
CS|Continuation sheet: applications and dispositions|2018-05-25
CT1|First registration caution|2023-08-29
DB|Exact line of boundary: registration|2026-09-03
DI|Disclosable overriding interests|2018-05-25
DJP|Deceased joint proprietor|2026-08-18
DL|Documents list|2018-08-20
DS1|Mortgage: cancellation of entries for lenders|2019-06-17
DS2|Cancel entries relating to a charge: registration|2023-08-29
DS2E|Remove a paid off mortgage: registration|2018-05-25
DS3|Mortgage: release of part of land for lenders|2022-11-21
FR1|First registration: application|2026-03-18
HC1|Historical register/title plan: official copy|2018-05-25
HR1|Notice of home rights: registration|2023-08-29
HR2|Notice of home rights renewal: registration|2023-08-29
HR3|Search of home rights by lenders|2018-05-25
HR4|Cancel home rights: registration|2023-10-30
ID1|Verify identity: private individual|2026-02-16
ID2|Verify identity: corporate body|2026-02-16
ID3|Certificate of identity for a private individual|2024-11-25
ID5|Certificate by conveyancer where identity verified by online video call|2026-02-16
JO|Jointly owned property trust: registration|2018-05-25
OC1|Official copies of register or plan: registration|2023-08-29
OC2|Official copies of documents: registration|2018-05-25
OS1|Official search with priority: whole title|2022-02-28
OS2|Official search with priority: part of title|2022-02-28
OS3|Official search without priority|2018-05-25
PN1|Proprietors' names: search of index|2025-11-21
PN1ID|IOPN search: verify identity|2024-05-13
RX1|Enter a restriction: registration|2019-07-01
RX2|Order to disapply/modify restriction|2018-05-25
RX3|Cancel a restriction: registration|2018-05-25
RX4|Withdraw a restriction: registration|2018-05-25
RXC|Restriction: consent or certificate|2024-08-19
SEV|Form A restriction: application to enter|2023-08-29
SIM|Index map: application for an official search|2020-11-05
ST1|Adverse possession: statement of truth|2018-05-25
ST2|Adverse possession of rentcharge: statement of truth|2018-05-25
ST3|Lost or destroyed deeds: statement of truth|2018-05-25
ST4|Prescriptive easements: statement of truth|2018-05-25
ST5|Cancellation of restriction: statement of truth|2024-05-13
TP1|Registered title(s): part transfer|2023-08-29
TP2|Registered title(s) under power of sale: part transfer|2023-08-29
TR1|Registered title(s): whole transfer|2024-01-23
TR2|Registered title(s) under power of sale: whole transfer|2023-08-29
TR4|Charge or portfolio of charges: transfer|2023-08-29
TR5|Portfolio of titles: transfer|2023-08-29
UN1|Unilateral notice: application to enter|2023-08-29
UN2|Unilateral notice: application to remove|2024-11-25
UN3|Existing unilateral notice: register beneficiary|2023-08-29
UN4|Unilateral notice: cancellation|2023-08-29
UT1|Upgrading title: application|2020-02-17
K1|Land Charge registration|2025-11-21
K2|Class F Land Charge registration|2025-11-21
K3|Pending Action registration|2025-11-21
K4|Writ or Order registration|2025-11-21
K6|Priority Notice registration|2025-11-21
K7|Renewal of Land Charge|2025-11-21
K8|Class F Land Charge renewal|2025-11-21
K9|Register entry rectification|2025-11-21
K11|Cancel Land Charge (except Class F/bankruptcy)|2025-11-21
K12|Cancellation under registrar special directions|2025-11-21
K13|Class F Land Charge cancellation|2025-11-21
K15|Official search of Land Charges Register|2026-04-13
K16|Bankruptcy-only official search|2025-11-21
K19|Land Charges register office copy|2025-11-21
K20|Land Charges register certificate of cancellation|2025-11-21'''
SPECIAL={
 'TR1':('Transfer whole of one or more titles; can be used in first registration','seller/transferor signs as deed; transferee if covenants/declarations require','Panels 1-12; evidence and date on completion','title/register, contractual terms, corporate power, tax certificate, AP1/FR1','hmlr-tr1-guide','https://www.gov.uk/government/publications/registered-titles-whole-transfer-tr1'),
 'TP1':('Transfer part of a registered title','transferor and any transferee covenant party under prescribed execution','Extent plan, new and retained easements, rights, reservations, consideration','compliant plan, title entries, tax evidence, AP1','hmlr-pg8','https://www.gov.uk/government/publications/registered-titles-part-transfer-tp1'),
 'AP1':('Apply to update register following registered disposition','applicant conveyancer or applicant as applicable','Application type/order, title numbers, parties, fee, evidence, identity and certificates','executed deed, tax certificate or exemption, discharge/compliance evidence','hmlr-forms','https://www.gov.uk/government/publications/change-the-register-ap1'),
 'FR1':('Application for first registration','applicant/conveyancer','Title and estate, applicant, declarations, fee and title documents','DL in duplicate, root/epitome, conveyance, plans, other deeds','hmlr-pg1','https://www.gov.uk/government/publications/first-application-registration-fr1'),
 'DL':('List first-registration supporting deeds','applicant/conveyancer','List in order all supporting instruments','FR1, originals where applicable','hmlr-pg1',None),
 'DS1':('Chargee discharge of registered mortgage','lender authorised signatory under prescribed execution','Mortgage/title details, execution, correct lender','redemption and valid release evidence; registration check','hmlr-pg31',None),
 'DS2':('Apply to cancel register entries relating to discharged charge','applicant/conveyancer','Identify affected charges entries and acceptable release evidence','DS1 or equivalent electronic discharge or eligible evidence','hmlr-pg31',None),
 'CH1':('Legal charge where lender charge deed not otherwise supplied or directed','borrower/chargor, required witness','Chargor, title, lender and debt security; legal charge formalities','offer, agreed charge conditions, capacity and lender authority','hmlr-pg8','https://www.gov.uk/government/publications/legal-charges-registration-ch1'),
 'OC1':('Obtain official copies of title register or title plan','applicant','Title identifiers and register/plan requirements','correct title number and fee','hmlr-forms',None),
 'OC2':('Obtain official copy of a filed deed/document','applicant','Identify filed deed with entry/date and title','filed reference and fee','hmlr-forms',None),
 'OS1':('Protect purchase or charge of whole registered title','buyer/lender conveyancer','Whole title, priority period and applicant details','correct existing title and transaction search details','hmlr-pg12','https://www.gov.uk/government/publications/official-search-with-priority-whole-title-os1'),
 'OS2':('Protect dealing affecting part of a registered title','buyer/lender conveyancer','Accurate part description/plan and priority applicant','sufficient plan and title identifier','hmlr-pg12',None),
 'K15':('Land Charges official search against named estate owners','applicant/conveyancer','Names, county names, periods from 1855 and bankruptcy search scope','full historical ownership chain and correct search period','hmlr-pg63','https://www.gov.uk/government/publications/land-charges-official-search-application-k15'),
 'K16':('Bankruptcy-only Land Charges search','applicant/conveyancer','Correct person/name and search scope','name identity history','hmlr-pg63',None),
 'RX1':('Apply to enter a restriction','owner/applicant as legally entitled','Required restriction text and entitlement','supporting instrument, evidence of entitlement','hmlr-pg19',None),
 'RX3':('Apply to cancel a restriction','applicant eligible','Basis and evidence restriction is no longer applicable','evidence, supporting consent/deeds','hmlr-pg19',None),
 'RX4':('Apply to withdraw restriction','beneficiary/applicant as entitled','Right beneficiary and restriction entry','proof applicant entitled to withdraw','hmlr-pg19',None),
 'ID1':('Verify identity of private individual in specified registration applications','individual and verifier as required','Identity details, verifier and photograph under current form','acceptable evidence; relevant PG67','hmlr-forms',None),
 'ID2':('Verify identity of corporate party in specified registration applications','representative/verifier as specified','Corporate identity and named authorised officers','companies evidence and PG67 guidance','hmlr-forms',None),
 'AN1':('Register an agreed notice','applicant with required consent or evidence','Identified interest, agreement and affected title','instrument and evidence of interest','hmlr-pg19',None),
 'UN1':('Apply to enter a unilateral notice','applicant asserting eligible interest','Nature and beneficiary of notice','basis of claimed interest, title','hmlr-pg19',None),
}
forms=[]
for line in FORM_ROWS.splitlines():
    code,title,listed=line.split('|')
    x=SPECIAL.get(code)
    kind='HMLR Land Charges' if code.startswith('K') else 'HM Land Registry'
    purpose=x[0] if x else f'{title} (check full statutory use and eligibility in official instructions)'
    sign=x[1] if x else 'See exact official form and latest execution/identity guidance; not independently panel-verified'
    sections=x[2] if x else 'Panel-by-panel completion guide not yet verified; preserve prescribed text'
    support=x[3] if x else 'Identify supporting evidence according to form, title and application'
    pg=x[4] if x else 'hmlr-pg8'
    direct=x[5] if x else None
    forms.append(dict(code=code,official_title=title,issuer='HM Land Registry',category=kind,publisher_listed_date=listed,publisher_date_last_checked=D,version='Publisher catalogue date; internal file revision not independently validated',file_revision_verified=False,purpose=purpose,when_required='Conditional on disposition and official guidance; do not assume required in all matters',completed_and_signed_by=sign,execution_formalities='Check prescribed execution / witnessing / identity requirements; case dependent',section_guidance=sections,supporting_documents=support,submission='Land Registry portal/Business Gateway or post as accepted for relevant application',fees='Consult HMLR current fee order and online calculator; conditional on application and route',deadlines='Check operative law, registration/priority period and any lender contractual deadline; no uniform deadline',common_errors=['incorrect title or legal parties','missing prescribed evidence, identity or fee','wrong form/version, incorrect execution or missing certificate'],official_catalogue_url=source_by_id['hmlr-forms']['url'],official_form_page_url=direct,official_download_link=None,practice_guide_source_id=pg,law_and_rules='Land Registration Act 2002; Land Registration Rules 2003 or Land Charges Act 1972 as applicable',copyright='Crown copyright subject to published licence; use genuine official prescribed file, never reconstruct or alter prescribed text',status='publisher_listing_checked_only' if not direct else 'publisher_listing_and_landing_page_checked'))
# Proprietary Law Society forms: no text/download redistribution.
for code,title,edition,note in [
('TA4','Required commonhold information','first edition 2007','Seller/commonhold association information'),
('TA6','Property Information Form','sixth edition (2025), required CQS new matters from 30 March 2026','Standard owner-occupier residential sale, not new build'),
('TA7','Leasehold Information Form','fifth edition (2025), required CQS new matters from 30 March 2026','Leasehold vendor information, alongside TA6'),
('TA10','Fittings and Contents Form','edition not independently verified','Sale inclusions/exclusions'),
('TA13','Completion Information and Undertakings','edition not independently verified','Precompletion requisitions and seller undertakings'),
('LPE1','Leasehold Property Enquiries','edition not independently verified','Landlord/managing agent responses and account statements'),
('FME1','Freehold Management Enquiries','edition not independently verified','Managed freehold estate management information'),
('CPSE1','Commercial Property Standard Enquiries 1','edition not independently verified','General pre-contract commercial property enquiries'),
('CPSE2','Commercial Property Standard Enquiries 2','edition not independently verified','Supplemental investment property enquiries'),
('CPSE3','Commercial Property Standard Enquiries 3','edition not independently verified','Supplemental occupational lease enquiries'),
]:
    checked=code in ('TA4','TA6','TA7','TA10','TA13')
    forms.append(dict(code=code,official_title=title,issuer='The Law Society / relevant licensed publisher',category='Law Society licensed / professional enquiries',publisher_listed_date='2026-06-24' if checked else None,publisher_date_last_checked=D if checked else None,version=edition,file_revision_verified=False,purpose=note,when_required='Dependent on transaction, Conveyancing Protocol/CQS status, contractual arrangements and purchaser requests',completed_and_signed_by='Supplier-issued form: confirm instructions and the named respondent',execution_formalities='Follow licensed form; signatures/declarations, if any, not assumed',section_guidance='Proprietary form not reproduced; review original licensed form with client',supporting_documents='Full replies, title, lease/management statements as applicable',submission='Through appropriate licensed conveyancing practice provider or solicitors',fees='Supplier licence or management fee may apply; case-specific',deadlines='Check contract/auction conditions and response times',common_errors=['outdated edition','unanswered or misleading replies','missing attachments or management information'],official_catalogue_url=source_by_id['ls-ta']['url'],official_form_page_url=None,official_download_link=None,practice_guide_source_id='ls-ta',law_and_rules='Conveyancing Protocol and CQS (where applicable), contract and general legal duties',copyright='PROPRIETARY: reference only; obtain from licensed supplier. No redistribution, reproduction or reconstruction.',status='publisher_guidance_checked' if checked else 'edition_or_provenance_requires_verification'))
# Other conveyancing-related official forms and filing certificates, intentionally
# separated from HMLR forms and from licensed Law Society enquiries.
EXTRA_FORMS=[
 ('MR01','Particulars of a charge','Companies House','Register a company mortgage/charge created on or after 6 April 2013; normally deliver within 21 days beginning day after creation','A person with interest in charge authenticates MR01; printed name required, no MR01 signature; charging company must execute instrument under applicable rules','Company details, date of charge creation/delivery, chargee, land, fixed/floating security, negative pledge and authentication','Certified copy of executed charging instrument and relevant Companies House fee','Online Companies House/WebFiling or compliant A4 paper MR01','21 days from day after creation (confirm start date and late filing rules)','co-mr01-form','2026-03-05'),
 ('MR04','Statement of satisfaction in full or in part of a charge','Companies House','Update company charge public record after satisfaction; separate from Land Registry charge cancellation','Authorised presenter as official instructions require','Company and charge identifier, full or partial satisfaction, authentication','Evidence of actual satisfied charge and Companies House records','Online or prescribed paper process','No universal 21-day initial-registration period; assess actual obligations','co-charge-forms','2023-02-06'),
 ('MR05','Statement of property released in part or whole','Companies House','Report property release from corporate security; separate from HMLR DS1/DS3','Authorised presenter as official instructions require','Company and charge identifier, details of property released and when','Underlying instrument/release and Companies House reference','Online or prescribed paper','Verify specific reporting requirement; no assumed deadline','co-charge-forms','2023-02-06'),
 ('SDLT1','Stamp Duty Land Tax paper return','HM Revenue & Customs','Paper tax return for unrepresented buyer; represented conveyancers should generally file online','Purchaser or authorised representative per current HMRC procedure','Actual effective date, land, consideration, parties, reliefs and return UTRN; complete genuine original paper form','Applicable supplementary returns SDLT2/3/4 and supporting tax calculations','Order original personalised paper SDLT1 from HMRC or authorised online filing','14 days after effective date for notifiable transaction, subject to law','sdlt1-guidance','2026-02-20'),
 ('SDLT2','Supplementary SDLT return additional buyers/sellers','HM Revenue & Customs','Paper continuation where there are more than two buyers or sellers','Actual SDLT applicant as instructed by HMRC','Additional parties; must reconcile to SDLT1','SDLT1 and original ordered supplementary form','Attach to paper SDLT1 or print/attach applicable online return certificate documentation','Same notifiable tax return deadline','sdlt-filing-guide','2026-06-26'),
 ('SDLT3','Supplementary SDLT for additional freehold property','HM Revenue & Customs','Paper supplementary return where freehold deal involves multiple properties','Actual SDLT applicant as instructed by HMRC','Additional freehold address and title particulars','SDLT1 and original ordered supplementary form','Paper with SDLT1 or relevant online return supporting copies for registration','Same notifiable tax return deadline','sdlt-filing-guide','2026-06-26'),
 ('SDLT4','Supplementary SDLT for leasehold or other extra transactions','HM Revenue & Customs','Paper supplementary return for specified complex leases and multi-property circumstances','Actual SDLT applicant as instructed by HMRC','Specified leasehold transaction data; consult instructions','SDLT1 and original ordered supplementary form','Paper with SDLT1 or relevant online return supporting copies for registration','Same notifiable tax return deadline','sdlt-filing-guide','2026-06-26'),
 ('SDLT5','HMRC land transaction return certificate','HM Revenue & Customs','Evidence return submission for registration; not a buyer-completed prescribed transfer deed','Issued by HMRC upon valid return processing, not signed by practitioner as a deed','Check UTRN, actual property details, and supporting SDLT2/3/4 when appropriate','Accepted tax return and UTRN; supplementary copies where required','Provide HMRC-issued SDLT5 with HMLR application when applicable','Tax return due under actual chargeability; register during valid priority period','sdlt-filing-guide','2026-06-26'),
 ('LTT-RETURN','Welsh Land Transaction Tax return / certificate','Welsh Revenue Authority','Online conveyancer professional return or paper return on application where allowed; WRA tax certificate supports registration','Registered tax professional or taxpayer using correct WRA route','Actual Wales property, effective date, consideration, parties and any relief','WRA account, valid tax data and generated WRA certificate','WRA online professional portal; unrepresented paper through WRA','Usually 30 calendar days beginning after effective date for notifiable transaction','wra-file-ltt','2026-10-27'),
]
for code,title,issuer,purpose,who,sections,support,submission,deadline,sid,page_date in EXTRA_FORMS:
    forms.append(dict(code=code,official_title=title,issuer=issuer,category='Companies House security' if issuer=='Companies House' else 'Tax return/certificate',publisher_listed_date=page_date,publisher_date_last_checked=D,version='Publisher guidance date; binary PDF version not independently validated',file_revision_verified=False,purpose=purpose,when_required='Required only where qualifying statutory conditions are established for the actual transaction',completed_and_signed_by=who,execution_formalities='Check current official instructions; document execution and electronic filing authentication are not interchangeable',section_guidance=sections,supporting_documents=support,submission=submission,fees='Consult issuer current fee schedule or tax portal; never assume a fixed amount',deadlines=deadline,common_errors=['incorrect taxpayer/company or title', 'wrong effective/creation date', 'missing certified instrument, return data or filing certificate'],official_catalogue_url=source_by_id[sid]['url'],official_form_page_url=source_by_id[sid]['url'],official_download_link=None,practice_guide_source_id=sid,law_and_rules='Companies Act 2006 Part 25, Finance Act 2003 Part 4 or Welsh land transaction tax legislation, depending on form',copyright='Use the current official issue or online service; do not recreate or claim scanned facsimiles as prescribed forms',status='publisher_listing_and_landing_page_checked'))
write('knowledge/forms/catalogue.json',forms)
print(f'created {len(sources)} source refs, {len(rules)} rules, {len(forms)} forms')
