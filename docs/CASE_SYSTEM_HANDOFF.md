# Case-system handoff

The project can export workflow action rows as CSV to a new local file. It does not connect to or modify any case system. In an approved private workspace:

```sh
conveyancing workflow registered-freehold-purchase > matter-workflow.json
# Review and complete the work record in the approved matter workspace.
conveyancing export-actions matter-workflow.json matter-actions.csv
```

The export has stage ID, action number, title, action, status, owner and due date. It escapes spreadsheet formula prefixes and refuses to overwrite an existing file. Keep the source and export under firm access and retention controls. Check the destination system's field mapping, import permissions and audit trail; import only with appropriate authority. The CSV is an exchange aid, not a tested vendor integration or authoritative matter record.

For supplier-specific integrations, obtain a supported API and sandbox plus the firm's credentials and authorisation. Actionstep documents an API at https://docs.actionstep.com/; HM Land Registry lists conveyancing software suppliers using Business Gateway at https://www.gov.uk/government/publications/software-suppliers-integrated-with-business-gateway/software-suppliers-integrated-with-business-gateway. Neither demonstrates that this project is integrated with those products. Supplier selection, mapping, credential handling, permissions, error recovery and sandbox acceptance remain outstanding.
