# Integration blueprint: deliberately disabled external actions

The workbench currently operates with local files, input data and deterministic checks. It **does not** have OAuth credentials, approved law-firm tenancy, access-control verification or supported APIs for your specific firm or lender. It cannot claim a successful upload, email, lender CoT submission, banking movement or Land Registry filing.

## Integration adapters for a later firm-approved deployment

| Capability | Proposed binding | Minimum safe control | Current implementation |
|---|---|---|---|
| Outlook/Microsoft 365 | Firm-authorised Graph connector | Verified tenant, matter confidentiality, draft-only default, recipient confirmation, audit | No live connection; produce correspondence draft |
| OneDrive/SharePoint/DMS | Firm-authorised, matter-scoped storage | Permission and sensitivity checks, legal privilege, retention, no bulk exports | Local approved path only; no encryption |
| Case-management software | Vendor API or import | Reconcile external case ID, field provenance, preview/diff, scoped write permission, rollback | CSV/JSON manual export with NOT SENT status |
| HMLR Business Gateway/portal | Approved HMLR account/API | Current official forms/rules, user authentication, fee and solicitor sign-off | Preflight only; no submissions |
| LMS/Lender Exchange/Smoove | Provider-authorised API or web workflow | Matter instruction, credential boundaries, signed certification and audit | Public-directory read only; no login/submission |
| Companies House | Approved filing service | Correct legal entity, instrument, day-limit and lawyer review | Deadline/checklist only; no filings |
| Banking/client ledgers | Approved read-only accounting integration | Independent bank-details checks, role separation and SRA Accounts Rules | Decimal arithmetic on user-supplied data only |
| Official source monitoring | Existing opt-in source-watch | Public allowlist, review queue, human promotion gate | Read-only watcher defined, not scheduled here |

### Integration acceptance contract

An adapter must provide: `capability`, `provider`, `firm_tenant`, `permission_scope`, `case_ref`, `action_type`, `preview`, `human_authorisation_ref`, `submission_id`, `external_acknowledgement`, `audit_event`, `rollback_or_reversal_path`, `status`. Actions need distinct `proposed`, `approved`, `submitted`, `acknowledged`, `rejected`, `completed` statuses. **Never** infer submission/acceptance from file generation or button click. No automatic retry for irreversible actions; duplicates and wrong recipient must be checked first.

The `handoff` command creates a **manual import preview** containing outstanding tasks and never contacts a provider. A real connector must be built/tested with authorised credentials before changing this label or enabling a network call. Live deployment requires law-firm IT/SRA/data-protection/security approval, vendor terms review, fine-grained secrets management and a staging environment.
