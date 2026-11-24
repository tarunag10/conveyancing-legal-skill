# Accessibility and readable legal output

Use semantic Markdown headings and evidence labels for narrative reviews. The optional static HTML dashboard uses a real document outline, accessible tables with header cells, legible scalable system fonts, high contrast, prefers-colour-scheme dark styling and keyboard focus indication. The page requires no JavaScript, tracking or third-party CDN.

For low vision or screen readers, prefer the `review --output report.json`, `report-md` or `dashboard` commands; keep headings predictable, short issue titles, human-readable document locators and plain, expandable fields. Never use only colour to communicate a completion blocker or urgency. Avoid decorative document scans where selectable accessible text can be provided, but retain original scans for execution/plan verification.

**Not certified:** no formal WCAG audit or assistive technology matrix has been performed. Verify screen readers, text scaling, contrast, focus and browser support with real users before a production rollout. Avoid putting client information into public accessibility test artifacts.
