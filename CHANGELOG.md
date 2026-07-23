# Changelog

## 2.0.0 - 2026-07-23

Corrective release based on public user feedback and a full workflow audit.

### Changed

- Replaced the broken Cowork installation instructions with current custom
  plugin upload steps, direct repository marketplace installation, and a
  separately labeled Claude Code developer setup.
- Added a low-token `screen` skill so a pasted job does not automatically
  trigger the full A-F report.
- Added hard workflow gates before application preparation: exact-role
  evaluation, exact-role resume draft, human resume approval, and answer
  review.
- Reframed `apply` as an application-packet assistant. Account creation,
  login, MFA, file upload, and final submission remain user-controlled.
- Replaced fuzzy silent deduplication with canonical job IDs and
  user-reviewed possible-duplicate flags.
- Added confidence labels to scan and triage results and stopped presenting
  search-engine results as an exhaustive or live job inventory.
- Added a source-evidence audit for every generated resume and a required
  human approval step before `Resume Ready`.
- Added voice preferences and sensitive-data safeguards to profile setup.
- Corrected the repository and author URLs in the manifest.

### Added

- `AUDIT.md` with the public-feedback-to-fix mapping.
- A self-contained marketplace manifest for direct repository installation.
- `references/workflow-gates.md` and `references/job-identity.md`.
- Static validation, safe ZIP packaging, CI, and manual acceptance scenarios.

### Removed

- Claims that career-ops can reliably create accounts, sign in, upload files,
  or complete forms across job sites.
- The implication that WebSearch results or generated materials are
  automatically accurate without user review.
