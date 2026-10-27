"""Only fictional scenarios and original text. No personal client data."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
FX=R/'tests'/'fixtures';FX.mkdir(exist_ok=True,parents=True)
EX=R/'examples';EX.mkdir(exist_ok=True,parents=True)
T=R/'templates';T.mkdir(exist_ok=True,parents=True)
D=R/'docs';D.mkdir(exist_ok=True,parents=True)

def write_json(target,data):target.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')

def matter(id,description,**kwargs):
    d={'matter_id':id,'test_case_description':description,'jurisdiction':'England','documents':[{'document_id':id+'-OC1','property_address':'Example Property, Test Town','title_number':'XX123456','source':'fictional case fixture'}],'charges':[], 'lender_requirements':[]}
    d.update(kwargs)
    write_json(FX/(id+'.json'),d)
    return d

matter('registered-freehold','Registered freehold without any asserted issues; no legal sign-off is implied')
matter('historic-charge','Unregistered historic further charge claimed vacated by correspondence',charges=[{'id':'22.01.1976 further charge','status':'vacated','evidence_type':'email','evidence_ref':'fictional seller email §4'}])
matter('auction-special','Auction special conditions require purchaser to discharge existing charges',charges=[{'id':'auction seller security','status':'outstanding','evidence_type':'auction pack','evidence_ref':'special conditions clause 7'}],missing_documents=['contract completion funds apportionment schedule'])
matter('leasehold-management','Leasehold transfer, absent LPE1/management receipts',missing_documents=['LPE1 replies','service-charge account statements','licence or notice evidence'])
matter('mortgage-guarantee','Guarantee and ILA requested, deed and lender advice forms unresolved',lender_requirements=[{'id':'ILA-001','text':'Director independent legal advice certificate','status':'outstanding','source_ref':'fictional lender letter para 10','blocking':True}])
matter('company-borrower','Corporate finance security needs documentary corporate authority',lender_requirements=[{'id':'CO-01','text':'Board resolution and current company identity evidence','status':'outstanding','source_ref':'fictional lender instruction schedule 3','blocking':True}])
matter('public-highway','Road shown adjacent on plan but adoption unverified',access={'public_highway_claimed':True,'official_highways_confirmation':False,'critical_to_lender':True,'evidence_ref':'seller marked-up plan (fictional)'})
matter('restrictive-covenants','Restrictive covenant not consented to',restrictions=[{'required':True,'wording':'Entry restricting dispositions absent management certificate','status':'unknown','evidence_ref':'fictional register B4'}])
matter('undisclosed-restriction','Restriction missed from transaction pack',restrictions=[{'required':True,'wording':'No disposition without certificate by management company','status':'outstanding','evidence_ref':'official copy register B7'}])
matter('imminent-completion','Completion in two business days, redemption and lender conditions unresolved',charges=[{'id':'seller mortgage','status':'outstanding','evidence_ref':'fictional seller statement'}],lender_requirements=[{'id':'COF-01','text':'Certificate of Title acceptance','status':'pending','source_ref':'fictional lender instructions','blocking':True}])
matter('commercial-vat-togc','Commercial opted property with disputed TOGC status',missing_documents=['Seller option-to-tax evidence','Tenancy and rental-business continuation documents','Purchaser VAT and option election advice'])
matter('sdlt','Simple England tax matter requiring up-to-date relief and return review',missing_documents=['Executed completion contract to prove SDLT effective date'])
matter('ltt','Wales LTT transaction fixture',jurisdiction='Wales',missing_documents=['Welsh property location verification and actual LTT rates at effective date'])
matter('land-registry-requisition','HMLR AP1 lacking evidence to satisfy restriction',restrictions=[{'required':True,'wording':'Certificate of compliance condition','status':'not supplied','evidence_ref':'fictional register restriction'}])
matter('contradictory-pack','Different title numbers and postal addresses in legal pack',documents=[{'document_id':'A','title_number':'XX123456','property_address':'1 Example Road'}, {'document_id':'B','title_number':'XX987654','property_address':'3 Example Road'}])
matter('ambiguous-discharge','An ambiguous stamped annotation is not a proven release',charges=[{'id':'1973 charge','status':'discharged','evidence_type':'ambiguous_endorsement','evidence_ref':'fictional deed p2 margin'}])
matter('building-safety','Flat possibly within England building-safety protections',building_safety={'potentially_applicable':True,'documented_assessment':False},missing_documents=['Building height/storey confirmation','Landlord and leaseholder certificates if applicable'])
matter('bridging-finance','Bridging loan day-one requirement schedule unconfirmed',lender_requirements=[{'id':'BR-01','text':'Lender-approved property insurance','status':'awaiting','blocking':True,'source_ref':'fictional special conditions §8'}])

write_json(EX/'matter-input.json',{'matter_id':'DEMO-001','jurisdiction':'England','documents':[{'document_id':'OC1-A','title_number':'AB123456','property_address':'1 Example Street, London','source':'fictional extract page 1'}], 'charges':[{'id':'mortgage dated 01.01.1999','status':'vacated','evidence_type':'email','evidence_ref':'seller-email-demo paragraph 3'}],'restrictions':[{'required':True,'wording':'No disposition without certificate','status':'unknown','evidence_ref':'OC1-A register B3'}],'lender_requirements':[{'id':'L1','text':'Proof of redemption in agreed form','status':'outstanding','blocking':True,'source_ref':'lender-example schedule 1'}]})
write_json(EX/'completion-input.json',{'side':'buyer','purchase_price':'250000.00','deposit_paid':'25000.00','seller_debits':[{'description':'service-charge apportionment (illustrative)','amount':'125.75'}],'seller_credits':[{'description':'credit for prepaid ground rent (illustrative)','amount':'25.00'}],'other_payments':[{'description':'professional fee + VAT + tax and disbursements (example only)','amount':'4200.00'}],'cleared_client_funds':'150000.75','cleared_lender_funds':'79000.00','bank_evidence_confirmed_by_human':False,'lender_conditions_satisfied_by_human':False})
write_json(EX/'lender-requirements.json',{'lender':'FICTIONAL lender, DO NOT TREAT AS ACTUAL HANDBOOK','matter_id':'DEMO-001','requirements':[{'id':'LTR-001','requirement':'Buildings insurance acceptable to named lender','source':'example lender instruction clause 4','evidence_status':'outstanding','completion_blocker':True,'owner':'acting solicitor','due':'before certificate of title or completion as specifically instructed'},{'id':'LTR-002','requirement':'Certificate confirming no adverse occupiers','source':'example special conditions clause 5','evidence_status':'not reviewed','completion_blocker':True,'owner':'acting solicitor','due':'before completion'}]})
write_json(EX/'field-values.json',{'values':{'PROPERTY_ADDRESS':'1 Example Road, Test Town','TITLE_NUMBER':'XX123456'},'allowed_fields':['PROPERTY_ADDRESS','TITLE_NUMBER'],'source_refs':{'PROPERTY_ADDRESS':'fictional register OC1-A page 1','TITLE_NUMBER':'fictional official copy OC1-A heading'}})

# Source verification: exhaustive machine-readable human audit with exact check date.
sources=json.loads((R/'knowledge/legislation/source-index.json').read_text(encoding='utf8'))
rules=json.loads((R/'knowledge/legislation/rules.json').read_text(encoding='utf8'))
forms=json.loads((R/'knowledge/forms/catalogue.json').read_text(encoding='utf8'))
lines=['# Source verification register','', 'Research reference date: **27 October 2026**. Each listed site was selected as an official or profession-authorised primary source for a particular proposition and the page was checked on the recorded date; this does not validate all page sections, current revisions of downloadable forms, or later changes.', '', 'A **separate practising property lawyer** must review applicability, commencement, amendments and transitional effects before a matter is certified. The legal rule registry also marks `legal_reviewer_approved: false` for each rule.','', '| Source ID | Publisher / source | Jurisdiction | Checked | Verification scope |','|---|---|---|---|---|']
for x in sources:
    scope=x['scope_note'].replace('|','/')
    lines.append(f'| `{x["id"]}` | [{x["title"]}]({x["url"]}) | {x["jurisdiction"]} | {x["last_verified_date"]} | {scope} |')
lines+=['','## Rule-level approval','',f'{len(rules)} indexed rules/acts. Automated importer preserves authority URLs, jurisdiction, references, effective-date assumptions, current applicability, transitional notes, source check date and flag `legal_reviewer_approved: false`. These are **research scaffolding** pending supervised legal approval, not a standing legal opinion.','','## Form-level approval','',f'{len(forms)} indexed entries. '+str(sum(f['file_revision_verified'] for f in forms))+' have an independently validated underlying form binary. Therefore **all individual form version claims must be checked at use**. Current editions of TA6 and TA7 and relevant CQS dates are recorded but Law Society originals are not reproduced.','', '## Re-check triggers','', '- Any actual effective transaction date later than the recorded legal/tax source verification date.', '- Statutory amendments, new commencement regulations, revised lender Handbook, updated HMLR form/guidance, tax Budget, practice/case law developments, or anomalies in a matter.', '- An unverified source, unavailable web link, or conflicting professional instruction.', '', 'The machine watcher only flags raw HTTP content differences; it cannot approve changed law.']
(D/'SOURCE_VERIFICATION_REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf8')

features='''# Feature inventory and deployment status

| Feature | Implemented | Verified / readiness |
|---|---|---|
| Canonical portable skill instructions | Yes | Filesystem review; live platform import not tested |
| Claude Code, Codex, Cursor, Gemini CLI folder adapters | Yes | Installed directories and short launchers; host discovery not tested |
| ChatGPT Projects fallback | Yes | Copy-ready instructions; manual upload required |
| ChatGPT Plugin package | Candidate only | Current schema-dependent importer compatibility not live-tested |
| 15 end-to-end conveyancing stages | Yes | Stage definitions include tasks, conditional tasks, responsibilities, evidence, dependencies and unproven default status |
| 28 matter-specific profiles | Yes | Detailed variation tasks; workflow approval remains manual |
| Registered/unregistered title, deeds, charges, access | Yes (reference and risk triage) | No automatic title opinion or visually verified plan interpretation |
| Auction, buy-to-let, bridging, corporate borrowers, ILA | Yes (reference and checklist) | No lender-specific Part 2 content, approved security package or lawyer certification |
| Leasehold, building safety, commercial, VAT/TOGC | Yes (reference) | Specialist provisions require matter-specific review |
| Forms library (89 entries) | Yes (index) | Zero original form binary revisions independently hash-validated; individual panel coverage selective |
| Dated source registry (42) | Yes | Source pages checked 27 Oct 2026; 33 rule records await legal sign-off |
| Buyer-side completion money reconciliation | Yes, executable | Input-only; actual client account/lender evidence not confirmed |
| Narrow basic residential SDLT/LTT calculator | Yes, executable | Time-gated illustrative bands; complex cases refused |
| Selected statutory days / OS priority date | Yes, executable | Holiday list required; contractual notice analysis manual |
| PDF/Word evidence text extraction | Yes, optional dependencies | Text only; OCR/visual signature or plan checks not provided |
| Editable original Word and replacement change logs | Yes, optional dependency | Only literal same-run placeholders; no protected form mutation or guaranteed preservation of layout |
| Content change watcher | Yes, opt-in | Domain allowlist and SHA256; no actual law effect determination |
| GitHub Actions CI / periodic watch definitions | Yes | Not remotely activated or scheduled until GitHub repository installed |
| Test scenarios | Yes | Fictional stress tests in `tests/fixtures` with Python unit tests |
| Full DMS, access control, authenticated user actions | No | Integrate only after firm security design and approval |
| Automatic exchange, payment, filing and third-party communications | Intentionally no | Requires explicit professional authorisation plus tool permissions |

### Most important gaps before a true production deployment

1. Form binary validation and precise per-form panel, execution and version details; licensed form source access.
2. Exhaustive legal sign-off for operative, transitional and jurisdictional status; live lender conditions.
3. Adversarial document parsing and OCR validation, scanned plans and boundary interpretation.
4. Independent legal and QA review, platform-by-platform acceptance, secure file storage and live CI deployment.
'''
(D/'FEATURE_INVENTORY.md').write_text(features,encoding='utf8')

original_templates={
 'REPORT_ON_TITLE.md':'''# Report on Title to Lender (draft only)

**Property:** {{PROPERTY_ADDRESS}}  
**Title:** {{TITLE_NUMBER}}  
**Lender:** [insert evidenced lender]  
**Borrower:** [insert evidenced identity]  
**Solicitor:** [insert authorised signatory]  
**Date:** [insert actual report date]

## Nature and extent of title

[Set out registered/freehold/leasehold or unregistered title and chain, supported by official copies or original deeds with evidence refs. Avoid automatic certification.]

## Existing legal charges

[Identify each charge, beneficiary, date, affected land, registered status, exact evidence for its discharge or undertaking and any outstanding priorities. Do not treat correspondence alone as a release.]

## Access, rights and title matters

[Identify highway adoption source, private access rights, restrictive covenants, planning/building safety status, easements and boundary enquiries.]

## Searches and enquiries

[List searches, precise dates, material adverse entries, outstanding enquiries and lender implications.]

## Outstanding conditions and reportable matters

| Lender condition / title point | Evidence | Risk | Remedy | Blocking? |
|---|---|---|---|---|
| [actual condition] | [source page] | [R level] | [enquiry] | [Yes / No, confirmed] |

## Recommendation for lender consideration

[State what consent or directions are specifically sought. Do not issue a Certificate of Title until all actual lender requirements satisfied and authorised by solicitor.]

**Status:** DRAFT FOR SOLICITOR REVIEW. NOT A CERTIFICATE OF TITLE.
''',
 'AUCTION_RISK_REPORT.md':'''# Auction buyer pre-bid / post-bid legal risk report

**Property:** [actual address]  
**Lot:** [lot number]  
**General conditions edition:** [actual version]  
**Special conditions:** [actual signed terms]  
**Contractual date:** [date evidenced in auction contract, not assumed]

## Contractual obligations and auction fees

[Quote and reference exact clauses on deposit, buyer premium, auction/admin fee, title guarantee, uninsured risks, VAT, completion period, seller remedies, search packages, notice to complete and interest.]

## Title and registration defects

[Analyse the actual chain, existing mortgages, releases, restrictive covenants, searches, physical access and all requisitions. Note if unregistered and first registration required.]

## Lender readiness

[Record whether lender was aware of contract and completion time; independent finance and offer conditions.]

## Risk register

| Source clause/page | Fact established | Unverified fact | Risk level | Consequence | Remedy |
|---|---|---|---|---|---|
| [ ] | [ ] | [ ] | [R0-R4] | [ ] | [ ] |

## Client advice and urgent decisions

[State binding contract status and precise extension/notice terms separately from statutory rights; do not assume extension consent.]

**Status:** DRAFT. Review complete legal pack and current conditions before reliance.
''',
 'TITLE_ENQUIRIES.md':'''# Additional enquiries before exchange / completion

**Re:** [property and file reference]

Dear Colleagues,

We write further to the title documentation and your replies. Would you please clarify the following outstanding matters, with copies of the underlying documents where requested?

1. **Historic mortgage:** The document at [source, page/paragraph] refers to [charge and date]. Please supply the actual executed release/discharge or other acceptable evidence confirming how this charge has been removed or will be released on completion, including the affected title and any Land Registry entry.
2. **Rights of access:** The plan appears to show the land adjoining [road]. Please provide documentary confirmation of the public highway extent/adoption, or evidence of legally enforceable access rights, as applicable. Adjacency on the plan is not itself sufficient evidence.
3. **Restrictions:** Please explain precisely how restriction [verbatim entry/ref] will be complied with and provide the form of certificate or consent for approval.
4. **Completion:** Please provide an up-to-date completion statement showing deposit, apportionments, agreed deductions and redemption mechanics, with any contractual adjustments explained.

We reserve the right to raise further reasonable enquiries on receipt of the supporting documents.

Kind regards,

[Conveyancer / firm, not fabricated]
''',
 'LENDER_OUTSTANDING_REQUIREMENTS.md':'''# Outstanding lender requirements schedule

**Lender:** [full name from instructions]  
**Borrower:** [identity and capacity]  
**Security:** [property/title(s)]  
**Relevant instructions:** [exact issue date/edition/Part/section and uploaded file ref]

| Ref | Requirement (verbatim or faithful paraphrase) | Source | Evidence | Status | Completion blocker | Owner / due |
|---|---|---|---|---|---|---|
| [ ] | [ ] | [ ] | [ ] | Outstanding / evidence received unverified / verified / lender waived | [Yes/No] | [ ] |

## Matters for lender confirmation

[Raise only lender-reportable matters, cite Part 1/2 or bespoke condition, and ask for written directions where needed.]

## Solicitor review

No statement is marked 'satisfied' from a client assertion or unexplained copy. Written waivers must come from an authorised lender source. **No automatic completion approval.**
''',
 'COMPLETION_CHECKLIST.md':'''# Buyer-side completion checklist

**Matter:** [ ]  
**Contractual completion date and time:** [ ]  
**Source of agreed time:** [contract clause/source]

- [ ] Latest title and priority search for correct title and transaction, correct OS1/OS2 priority period
- [ ] Bankruptcy search / lender-name searches as instructed, correctly scoped
- [ ] All lender conditions and reporting/consents, insurance and COT accepted as required
- [ ] Sufficient cleared client and lender funds actually verified by authorised staff
- [ ] Seller completion statement approved and independently reconciled
- [ ] Executed TR1/TP1/deed and any lease covenants checked in current prescribed form
- [ ] Agreed undertakings and mortgage redemption/release documents sufficient
- [ ] Restrictions and third-party certificates/consents accounted for
- [ ] Keys, vacant possession or tenancy continuation and agreed arrangements confirmed
- [ ] Completion mechanism and notice to complete consequences reviewed
- [ ] Authorised lawyer approves release and records actual funds transfer and receipt
- [ ] SDLT/LTT return and payment deadline recorded from actual effective date
- [ ] AP1/FR1 and registration fees, deed attachments and lender charge registration ready
- [ ] Any Companies House MR01 deadline and security filing instructions checked

**Result:** Not completed by the checklist itself. Annotate evidence references and supervising lawyer's approval.
''',
 'ILACERTIFICATE_REVIEW.md':'''# Independent legal advice: interview and certificate preparation checklist

**Proposed guarantor:** [identified person]  
**Proposed borrower:** [company/person]  
**Lender:** [from actual package]  
**Facility / security:** [exact offer]

## Before meeting

- Confirm independent retainer, conflict check and whether the lender's chosen certificate wording is acceptable.
- Obtain and read the full facility, guarantee, indemnity, mortgage, debenture and actual lender advice instructions.
- Confirm adviser can act independently, speak directly and privately to client, and assess capacity/understanding and interpreter needs.

## Advice record

[Record advice on nature, scope, unlimited/continuing liability, all-monies clause, primary indemnity obligations, lender calls, joint and several terms, charging property, insolvency, independent negotiation and alternatives as applicable. Explain observed questions and client response.]

## Execution and release controls

[Record actual identity and witnessed signing details only when observed. Never state advice delivered or signatures witnessed before the meeting. Verify actual execution and lender form wording.]

**Document status:** INTERNAL PREPARATION ONLY. Not a certificate that any independent advice was given.
''',
 'NOTICE_TO_COMPLETE_REVIEW.md':'''# Notice to complete: solicitor issue checklist and optional draft shell

**WARNING:** Contract-specific legal analysis is indispensable before service. This shell is **not** an operative notice without approval and correct service.

Re: [property and parties identified by actual contract]

We refer to the contract dated [actual exchange/contract date] and clause [exact operative edition/condition] regarding completion.

[Insert contract-compliant demand and actual notice terms only after calculating the relevant **working-day or calendar-day** service period under the incorporated conditions and any special amendments. Review whether party serving is ready, able and willing to complete, and correct service method, recipient and deemed receipt.]

Nothing in this draft is authority to serve a notice. Client/lender directions and supervisor approval are required.
''',
 'LAND_REGISTRY_REQUISITION.md':'''# HM Land Registry requisition response draft

**Application reference:** [ ]  
**Title number:** [ ]  
**Date of requisition:** [ ]  
**Actual deadline, extensions and evidence:** [ ]

Dear Sir or Madam,

We refer to the requisition dated [date] in the above application.

**Requisition 1** ([quote exact requisition]): [reply with evidence and legally correct attachment reference]

**Requisition 2** ([quote exact requisition]): [reply with evidence]

Please let us know if any further information is required. We have not represented any outstanding item as satisfied without accompanying documentary evidence.

Yours faithfully,

[Authorised practitioner]
''',
 'TOGC_VAT_QUESTIONS.md':'''# Commercial transfer: VAT and TOGC enquiries

**Transaction:** [property and buyer/seller entities]  
**Completion/effective date:** [ ]

Dear Colleagues,

Before the VAT provisions can be agreed, please clarify the seller's asserted option to tax and provide suitable evidence of the election and its effective date, together with the VAT invoice position.

Please confirm whether a property rental business is being transferred as an ongoing undertaking, the tenancies continuing at completion, and the factual basis upon which the parties say that the transaction does or does not satisfy the TOGC provisions. We also require confirmation of any pre-completion purchaser VAT registration and option-to-tax steps said to be necessary, with dates and supporting documents.

Pending this information and specialist VAT advice, we cannot confirm the correct contractual treatment or the allocation of risk if the expected TOGC treatment fails. We invite a proposal for a suitable VAT, invoice, adjustments and indemnity clause tailored to the verified facts.

Kind regards,

[Authorised conveyancer]
''',
 'CLIENT_TITLE_REPORT.md':'''# Report to buyer on title

**Property:** [ ]  
**Tenure, title number and legal owners:** [ ]  
**Purchase price and deposit:** [ ]  
**Lender and proposed security:** [ ]

## The interest you will acquire

[Identify exactly the contractual estate and the reliable register/deed/lease evidence.]

## Your rights, obligations and restrictions

[Explain access, easements, restrictions, covenants, lease obligations, service charges, ground rent and building safety risks in plain English.]

## Searches and condition

[Summarise actual search results with dates, planning, highways, contamination, flood and other appropriate scope. State limits: solicitor does not inspect physical condition.]

## Financial and contractual obligations

[Explain actual contractual completion mechanics and verified known sums. SDLT/LTT estimate is not a tax advice substitute.]

## Outstanding enquiries and recommendations

[Number evidence gaps, material lender-reportable matters, remedies and whether completion is blocked.]

## Instructions sought

[Ask for informed written instructions on specific unresolved risk. Do not imply acceptance by silence.]

**DRAFT; solicitor to approve and issue.**
''',
 'COMPLETION_CONFIRMATION.md':'''# Completion confirmation to other side (issue only after actual completion)

**Property:** [ ]  
**Contractual parties:** [ ]

Dear Colleagues,

We write to confirm completion of the above transaction has taken place today, [insert evidenced completion date], in accordance with the agreed completion arrangements.

Please arrange the release of the keys and any agreed post-completion documents, and provide evidence of the discharge of any relevant charge pursuant to the completion undertakings.

Kind regards,

[Authorised practitioner]

**Do not send unless completion funds receipt and legal completion are confirmed.**
'''
}
for name,content in original_templates.items(): (T/name).write_text(content,encoding='utf8')
print(f'Generated {len(list(FX.glob("*.json")))} fictional case scenarios; {len(original_templates)} original templates; {len(sources)} cited source report rows')
