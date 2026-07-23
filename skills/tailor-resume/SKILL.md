---
name: tailor-resume
description: "Create an ATS-compatible resume draft for one evaluated job, plus a source-evidence claim audit. The user must review and approve it before it becomes Resume Ready. Use when someone says 'tailor my resume', 'make me a resume', 'create a resume for', or 'update my resume for'."
argument-hint: "<company name or 'for the latest evaluation'>"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Glob
---

# Tailor Your Resume

Generate an ATS-compatible resume draft customized for a specific job posting.
Read references/ats-rules.md before generating any HTML.
Read `references/workflow-gates.md` and `references/job-identity.md`.

## Step 0: Load Context

1. Read `data/profile.yml` for structured background data
2. Read `data/resume.md` if it exists (full resume text for detail)
3. Find the target evaluation:
   - If the user specified a company/role, search `data/evaluations/` for a match
   - If "latest" or no argument, use the most recent evaluation file
   - If ambiguous, list recent evaluations and ask which one
4. If no evaluation exists:
   > "I need to evaluate the job first so I know what to emphasize.
   > Paste the job posting and I'll assess it, then generate your resume."
5. Verify that the evaluation's company, role, and `Job Key` match the target
   tracker row. Never reuse an evaluation or resume from a similarly named
   role.

## Step 1: Keyword Extraction

From the evaluation + JD, extract 10-15 relevant keywords:

- Exact phrases from "Required Qualifications" (highest priority)
- Industry-standard terms (not creative synonyms)
- Certifications, tools, methodologies named in the JD
- Action verbs that match the responsibilities section

Only use a keyword when the source resume or profile supports the underlying
claim. Do not stuff a JD phrase into a bullet merely to increase keyword
overlap. A missing requirement stays a gap.

## Step 2: Detect Language & Locale

- JD in English + US company: Letter paper (8.5" x 11")
- JD in English + non-US: A4
- JD in another language: match that language, use A4
- Resume language MUST match JD language

## Step 3: Build Resume Content

Using the evaluation's Block E (Tailoring Plan) as a guide, construct
each resume section from profile data:

Preserve work history in reverse chronological order. Reorder bullets within a
role for relevance, but never reorder employers to make an older role appear
current. Preserve employer names, job titles, dates, credentials, and metrics
unless the user corrects them.

### Professional Summary (3-4 lines)
- Open with years of experience + core identity
- Include 3-5 top keywords from the JD naturally
- End with a forward-looking statement connecting to this specific role
- Use the narrative.headline from profile as a starting point
- Avoid generic claims such as "results-driven" unless the source evidence
  immediately proves them

### Experience Section
- Include roles from work_history in reverse chronological order
- For each role: Company, Title, Dates on one line
- 3-5 bullets per role, ordered by relevance to THIS JD
- Each bullet: Action verb + what you did + quantified result
- Mirror JD language exactly (if JD says "project management",
  write "project management", not "programme management")
- Pull specific numbers from proof_points and work_history highlights
- Never add a number, scope, tool, credential, or responsibility that does not
  appear in the source profile or resume

### Education Section
- Degree, School, Year
- Include relevant coursework or honors only if recent grad

### Skills Section
- List JD keywords FIRST, then additional skills
- Group by category if 10+ skills (Technical, Tools, Methodologies, etc.)
- Include both acronym and full form: "Search Engine Optimization (SEO)"

### Certifications Section (if applicable)
- From credentials in profile
- Include status, jurisdiction, number if relevant

### Projects / Portfolio (if applicable and relevant)
- Only include if the archetype values it (Creative, Technology)
- Brief description + link + key metric

## Step 4: Generate HTML

Read the template from references/resume-template.html.

Fill all `{{PLACEHOLDER}}` slots with the generated content.

ATS compliance rules (from references/ats-rules.md):
- Single column ONLY
- Standard section headers exactly: "Experience", "Education", "Skills"
- No images, icons, or graphics
- All text selectable (no text-in-images)
- Standard fonts: Arial, Calibri, Georgia, or system sans-serif
- Font size: 10-12pt body, 14-16pt name
- Margins: 0.5-1 inch
- No headers/footers (ATS strips them)
- Max 2 pages

## Step 5: Create a Claim Audit

For every materially changed or newly written summary sentence and bullet,
create:

`data/resumes/{company-slug}-{role-slug}-claim-audit.md`

```markdown
# Resume Claim Audit: {Company} - {Role}

Job Key: {job-key}

| Draft Claim | Source Evidence | Transformation | Status |
|---|---|---|---|
| {resume text} | {exact profile field or source-resume text} | Reordered / shortened / combined / unchanged | Supported |
```

If a desired claim lacks source evidence, do not place it in the resume. Add
it to a `NEEDS USER INPUT` section in the audit.

## Step 6: Output Draft

Write the HTML to `data/resumes/{company-slug}-{role-slug}.html`.

Show the user a preview of the content (not the HTML code):

```
## Resume Preview: {Name} - {Target Role} at {Company}

**Summary:** {first 2 lines}

**Experience:**
- {Role 1} at {Company} ({dates}) - {first bullet}
- {Role 2} at {Company} ({dates}) - {first bullet}

**Skills:** {top 10}

**Supported keywords used:** {n} of {total relevant keywords}
**Claim audit:** `data/resumes/{audit-filename}`
```

Run a quality pass before presenting the draft:

- Apply `voice.tone`, `voice.formality`, and `voice.avoid_phrases`.
- Remove empty adjectives, copied JD clauses, and repetitive verbs.
- Confirm chronology, company names, titles, dates, metrics, and credentials
  against the source.
- Label the result `Resume Draft`, not `Resume Ready`.

## Step 7: Review and PDF Instructions

> "Your tailored resume is saved at `data/resumes/{filename}.html`.
> Its source check is saved at `data/resumes/{audit-filename}`.
>
> **To save as PDF:**
> 1. Open the file in your browser (double-click it)
> 2. Press **Cmd+P** (Mac) or **Ctrl+P** (Windows)
> 3. Select **Save as PDF**
> 4. Done!
>
> The HTML is designed to print cleanly. Please compare the draft and claim
> audit with your original resume. Tell me what to change, or explicitly say
> 'approve this resume' when every claim is accurate."

## Step 8: Update Tracker

Update the matching row in `data/applications.md`:
- Status: `Resume Draft`
- Resume: `[Draft](resumes/{filename})`
- Notes: append `Claim audit: {audit-filename}`

Only after the user explicitly approves the draft:

1. Change status from `Resume Draft` to `Resume Ready`.
2. Record `User approved {date}` in Notes.
3. Offer application-packet preparation.

Until approval, do not proceed as though the resume is ready and do not
prepare final application answers.
