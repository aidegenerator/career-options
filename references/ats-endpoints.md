# ATS URL Patterns for Public Search

This file is intentionally limited to URL recognition and site-scoped search.
Direct ATS APIs may be blocked, rate-limited, undocumented, or unavailable in
Cowork. Do not call an ATS API from this plugin.

Use `WebSearch` as described in `skills/scan/SKILL.md`. Treat results as
best-effort and label freshness/confidence.

## Recognize the ATS

| Public job URL pattern | ATS | Site-scoped query |
|---|---|---|
| `job-boards.greenhouse.io/{slug}/jobs/{id}` | Greenhouse | `site:job-boards.greenhouse.io/{slug} {role terms}` |
| `boards.greenhouse.io/{slug}/jobs/{id}` | Greenhouse legacy | `site:boards.greenhouse.io/{slug} {role terms}` |
| `jobs.lever.co/{slug}/{id}` | Lever | `site:jobs.lever.co/{slug} {role terms}` |
| `jobs.ashbyhq.com/{slug}/{id}` | Ashby | `site:jobs.ashbyhq.com/{slug} {role terms}` |
| `jobs.smartrecruiters.com/{company}/{id}` | SmartRecruiters | `site:jobs.smartrecruiters.com/{company} {role terms}` |
| `{tenant}.myworkdayjobs.com/.../job/...` | Workday | `site:{tenant}.myworkdayjobs.com {role terms}` |
| `{company}.recruitee.com/o/{slug}` | Recruitee | `site:{company}.recruitee.com/o {role terms}` |
| `apply.workable.com/{company}/j/{id}` | Workable | `site:apply.workable.com/{company} {role terms}` |

If the pattern is unknown, search:

`{company name} careers {primary role terms}`

## Stable identity hints

Extract an explicit job ID from the URL path when the pattern provides one.
Store it using the ATS prefix:

- `greenhouse:{id}`
- `lever:{id}`
- `ashby:{id}`
- `smartrecruiters:{id}`
- `workday:{requisition-or-path-id}`
- `recruitee:{slug}`
- `workable:{id}`

If no stable ID is visible, use the canonical URL or fallback fingerprint from
`references/job-identity.md`.

## Search limits

- One primary-role query and one secondary-role query per company by default.
- Do not claim the result list is complete.
- Do not retry blocked pages repeatedly.
- Do not interpret search-result order as relevance.
- Record whether each result is `Verified page`, `Snippet-only`, or
  `Stale/unknown`.
