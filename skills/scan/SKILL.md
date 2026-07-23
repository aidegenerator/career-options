---
name: scan
description: "Scan company career pages for job openings that match your profile. Uses web search with site-scoped queries to find listings on Greenhouse, Lever, Ashby, SmartRecruiters, and other ATS platforms. Use when someone says 'scan for jobs', 'check careers page', 'find openings at', or 'search for roles'."
argument-hint: "<company name, careers URL, or 'all' to scan watchlist>"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - WebSearch
  - Glob
---

# Scan for Job Openings

Search company career portals for roles matching your profile.
Use ATS type and slug detection (see references/ats-endpoints.md) to build
targeted site-scoped WebSearch queries.

Read `references/job-identity.md` before deduplicating. Web search is a
best-effort discovery method, not an exhaustive or guaranteed-current
inventory.

## Step 0: Load Context

1. Read `data/profile.yml` for target roles, skills, seniority
2. Read `config/portals.yml` if it exists (company watchlist)
3. Read `data/scan-history.md` if it exists (dedup against seen postings)
4. Read `data/applications.md` to exclude roles already tracked

## Step 1: Determine What to Scan

Parse user input:

- **Company name:** Look up in portals.yml for ATS type and slug.
  If not found, use WebSearch to find their careers page and detect ATS.
- **URL:** Detect ATS type from URL pattern:
  - `boards.greenhouse.io/{slug}` or `{company}.greenhouse.io` -> Greenhouse
  - `jobs.lever.co/{slug}` -> Lever
  - `jobs.ashbyhq.com/{slug}` or `{company}.ashbyhq.com` -> Ashby
  - `jobs.smartrecruiters.com/{slug}` -> SmartRecruiters
  - Other -> use WebSearch with `{company name} careers {role keywords}`
- **"all" / "scan my watchlist":** Scan every enabled company in portals.yml.
  If no portals.yml exists, tell the user:
  > "You don't have a company watchlist yet. Tell me some companies
  > you're interested in and I'll set one up."
- **"scan {industry}":** Use WebSearch to find companies hiring in that
  industry, then scan their career pages.

## Step 2: Fetch Job Listings

### Tier 1: WebSearch (primary)

Use WebSearch with targeted site-scoped queries to find job listings.
Use the ATS type and slug identified in Step 1 to build precise queries.

**Search strategy by ATS:**

- **Ashby:** `site:jobs.ashbyhq.com/{slug} {target role keywords}`
- **Lever:** `site:jobs.lever.co/{slug} {target role keywords}`
- **Greenhouse:** `site:job-boards.greenhouse.io/{slug} {target role keywords}`
  (Note: Greenhouse pages are poorly indexed. If no results, try
  `{company name} careers {target role keywords} greenhouse`)
- **SmartRecruiters:** `site:jobs.smartrecruiters.com/{slug} {target role keywords}`
- **Workday:** `site:{tenant}.myworkdayjobs.com {target role keywords}`
- **Generic / unknown ATS:** `{company name} careers {target role keywords} {current year}`

**Build target role keywords** from the profile: combine primary_role,
secondary_roles, and top 3 skills. Example for a marketing director:
`marketing director OR head of marketing OR VP marketing`

**Parse search results:** Each result typically contains the job title
in the link text and the URL to the posting. Extract title and URL from
each search result. If the search returns descriptions, extract location
and department info as well.

**Query budget:** Run at most one primary-role query and one secondary-role
query per company unless the user asks for a broader scan. Canonicalize results
using `references/job-identity.md`.

### Tier 2: Manual Fallback

If WebSearch fails to return results:
> "I couldn't find listings automatically for {company}. Here's their
> careers URL: {url}. You can browse it and paste any interesting
> job postings for me to evaluate."

## Step 3: Filter & Match

For each job listing found:

1. **Title relevance:** Compare against target roles from profile.yml
   - Match target role keywords (primary + secondary roles)
   - Exclude roles that don't match seniority level
   - Exclude titles with negative keywords if profile has exclude_keywords

2. **Quick relevance score (0-10):**
   - Title match to target roles: 0-4 points
   - Skills/keyword overlap with profile: 0-3 points
   - Location/remote match: 0-2 points
   - Seniority alignment: 0-1 point

3. **Identity and freshness:**
   - Extract an ATS job ID when present and derive the canonical URL.
   - Same ATS ID or same canonical URL: definitive duplicate.
   - Similar company/title with different IDs, URLs, or locations:
     `Possible Duplicate`; keep both visible and ask the user before merging.
   - Previously seen does not mean currently live. Record the first/last seen
     dates separately from duplicate status.
   - Never call a role "new" unless it has a new definitive job key.

4. **Confidence label:**
   - `Verified page`: current job page content was retrieved.
   - `Snippet-only`: only a current search result snippet was available.
   - `Stale/unknown`: the result date or live status could not be confirmed.

## Step 4: Output

```
## Scan Results: {Company} - {date}

Found **{X}** possible openings in public search results; **{Y}** may match
your profile. This is not exhaustive.

### Matches (by relevance)

| # | Role | Location | Relevance | Confidence | Job Key | Link |
|---|---|---|---|---|---|---|
| 1 | {title} | {location} | {score}/10 | {confidence} | {job-key} | {URL} |
| 2 | ... | ... | ... | ... | ... | ... |

### Possible Duplicates

Show every possible pair and the fields that differ. Offer `Keep Both`,
`Merge`, or `Ignore New`. Do not decide from fuzzy title similarity alone.

### Filtered Out ({Z} roles)
{Brief list: "3 junior roles, 2 in unrelated departments, 1 requires
relocation to {city}"}
```

## Step 5: Save & Next Steps

Add all matches to `data/pipeline.md` (create if doesn't exist):

```markdown
# Job Pipeline

| Date Found | Company | Role | Job Key | Posting URL | Relevance | Confidence | Quick Score | Status |
|---|---|---|---|---|---|---|---|---|
| {today} | {company} | {title} | {job-key} | {canonical-url} | {score}/10 | {confidence} | | New |
```

Log ALL seen postings (matches + filtered) to `data/scan-history.md`:

```markdown
| Date | Company | Role | Job Key | Posting URL | Confidence | Action |
|---|---|---|---|---|---|---|
| {today} | {company} | {title} | {job-key} | {canonical-url} | {confidence} | Matched / Filtered: {reason} |
```

Filtered results remain visible in the response with a short reason. A user
may override a filter. Do not permanently suppress a role solely because a
previous scan filtered it.

> "Found {Y} matching roles at {company}.
>
> Want me to:
> - **Evaluate** the top match? Say 'evaluate #1'
> - **Triage** the full pipeline? Say 'triage my pipeline'
> - **Scan** another company? Say 'scan {company}'"
