# Public feedback audit

Audit date: 2026-07-23

This audit treats the criticism as product evidence, not a documentation
problem to explain away.

## Sources reviewed

- [General experience trying to use Cowork, using career-ops as the example](https://www.reddit.com/r/ClaudeCowork/comments/1syex98/general_experience_trying_to_use_cowork_as_an/)
- [Original career-ops Cowork announcement and installation thread](https://www.reddit.com/r/ClaudeCowork/comments/1seyvlj/i_forked_the_viral_700_job_application_tool_into/)
- [Job-application automation testing discussion](https://www.reddit.com/r/ClaudeCowork/comments/1t8193g/cowork_job_application_automation_testing_idea/)
- [A lower-token, human-submit job-search comparison](https://www.reddit.com/r/ClaudeAI/comments/1uyky9u/laid_off_in_march_i_built_a_jobsearch_tool_almost/)
- [Official Claude plugin installation guidance](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)

## Findings and corrective action

| Severity | Evidence-backed finding | Root cause in v1 | v2 corrective action | Verification |
|---|---|---|---|---|
| Critical | Cowork users could not follow the installation instructions. | README documented Claude Code flags, an undefined plugin directory, and a repository URL that no longer existed. | README now leads with current Claude/Cowork custom ZIP upload, exact UI path, install verification, and a separately labeled developer flow using the real repository. | Static validator rejects the stale URL; packaging test verifies an uploadable root layout. |
| Critical | The assistant bypassed evaluate and tailor-resume, then reused generic resumes. | Independent skills merely suggested the next step; `apply` continued when artifacts were absent. | Application preparation now stops until the exact role has an evaluation, exact-role resume draft, and explicit resume approval. | Workflow-gate assertions plus manual scenario 2. |
| Critical | The plugin promised automation that Cowork could not reliably perform. | `apply` described form filling, uploads, navigation, and screenshots as if browser support were dependable. | `apply` now promises a reviewed, copy-ready application packet. It treats account creation, login, MFA, uploads, and submit as user-controlled boundaries. | Claim checks plus manual scenario 6. |
| High | Job posts were incorrectly marked duplicate or new. | URL equality and fuzzy company/title matching were mixed together without a canonical identity or review state. | Definitive duplicate only for equal ATS ID or normalized URL. Similar title/company records are visible `Possible Duplicate` entries requiring user choice. | Identity invariants plus manual scenarios 4 and 5. |
| High | Full evaluations consumed too much time and context. | Pasting a JD triggered a 6-block report with compensation research and 6-10 interview stories. | New `screen` skill performs a compact decision first. Full evaluation is reserved for promising roles or explicit requests; interview stories are deferred until interview prep is useful. | Trigger assertions plus manual scenario 3. |
| High | Resume and cover-letter text could sound generic or copy the JD. | Instructions encouraged exact phrase mirroring and template-like openings without an evidence trace or voice review. | Resume drafts preserve chronology and facts, use only supported keywords, generate a claim audit, apply voice preferences, and remain `Resume Draft` until approved. Application answers include an anti-template quality pass. | Resume invariant checks plus manual scenario 7. |
| Medium | Scan results were treated as exhaustive/current and aggressive filters became “judgey.” | WebSearch snippets were ranked without confidence or freshness labels, and filtered entries were silently hidden. | Results are labeled verified, snippet-only, or stale/unknown. Filters show reasons and user overrides. Prior-seen posts are not silently discarded when identity is uncertain. | Manual scenarios 4 and 8. |
| Medium | There was no meaningful test suite despite a passing manifest check. | `claude plugin validate` checked the manifest but not cross-file behavior or claims. | Added a standard-library validator, CI, safe packaging, and eight manual end-to-end scenarios. | `claude plugin validate .`, static validator, package validator. |

## Product boundary

career-ops is useful for structured screening, evidence-backed drafting,
research, and tracking. It is not a reliable unattended browser automation
system. v2 makes that boundary part of the workflow instead of leaving users
to discover it after investing hours.

## Remaining live validation

Before publishing 2.0.0:

1. Upload the generated ZIP through Claude Desktop/Cowork on macOS and Windows.
2. Run every scenario in `tests/scenarios.md` in a fresh Cowork project.
3. Confirm skill discovery and behavior in a new conversation.
4. Have at least two job seekers review generated resumes against their source
   resumes and flag unsupported claims.
5. Publish the ZIP only after those checks pass; record results in the scenario
   checklist.
