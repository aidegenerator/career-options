---
name: help
description: "See all available career-ops skills, what they do, and which one to use next based on where you are in your job search. Use when someone says 'help', 'what can you do', 'how does this work', or seems unsure what to do next."
argument-hint: "[skill name for detailed help]"
user-invocable: true
allowed-tools:
  - Read
  - Glob
---

# career-ops Help

Guide the user through available skills based on where they are in their
job search.

## Step 0: Check State

Read `data/profile.yml` - does it exist?
Read `data/applications.md` - how many entries?
Glob `data/evaluations/*.md` - how many evaluations?
Glob `data/resumes/*.html` - how many resumes?

## Step 1: Show Skill Directory

If the user asked about a specific skill, show detailed help for that skill.
Otherwise show the full directory:

```
## career-ops - Your Job Search Copilot

| Skill | What It Does | Try Saying |
|---|---|---|
| **screen** | Compact first-pass fit check | "Should I apply to this?" |
| **evaluate** | Full, saved job evaluation | "Run the full evaluation" |
| **tailor-resume** | Create and source-audit an exact-role resume draft | "Tailor my resume for the Acme role" |
| **scan** | Search company career portals for matching openings | "Scan Google for jobs" |
| **triage** | Quick-score your pipeline of scan results | "Triage my pipeline" |
| **track** | View and update your application tracker | "Show my applications" |
| **apply** | Prepare a reviewed application-answer packet | "Prepare my application packet" |
| **research** | Deep-dive a company before applying or interviewing | "Research Stripe" |
| **outreach** | Draft LinkedIn/email messages to contacts | "Draft outreach to the hiring manager" |
| **compare** | Side-by-side comparison of opportunities | "Compare my top options" |

**Commands:**
| Command | What It Does |
|---|---|
| **setup** | Set up or update your profile |
| **quick-eval** | Fast score + one paragraph (no full report) |
```

## Step 2: Smart Suggestion

Based on the user's current state, suggest the most valuable next action:

**No profile:**
> "Start here: paste your resume or tell me about yourself so I can
> evaluate jobs for you."

**Profile exists, no evaluations:**
> "You're all set! Paste a job posting (URL or text) and I'll screen the
> fit before running a full evaluation."

**Has evaluations, no resumes:**
> "You have {n} evaluations. Your top match is **{company} - {role}**
> ({score}/5.0). Want me to tailor a resume for it?"

**Has resume drafts awaiting approval:**
> "You have {n} resume drafts to review. Open the draft and claim audit,
> then approve or revise each one before preparing application answers."

**Has approved resumes, none applied:**
> "You have approved resumes for {n} roles. Say 'prepare my {company}
> application packet' and I'll draft answers for you to review and enter."

**Has applications:**
> "You have {n} active applications. Say 'show my applications' for a
> status overview, or 'update {company} to {status}' to track progress."

**Has interviews:**
> "You have interviews coming up! Say 'research {company}' to prepare."

## Step 3: Workflow Overview (if user asks "how does this work")

```
## The career-ops Workflow

1. **Set up** your profile (one time, 5 minutes)
   ↓
2. **Screen** job postings (compact decision first)
   ↓
3. **Evaluate** promising roles in detail
   ↓
4. **Tailor and approve** an exact-role resume
   ↓
5. **Prepare and review** an application packet
   ↓
6. **Submit manually**, then track the outcome

**Discovery tools** (use anytime):
- **Scan** company career pages for new openings
- **Research** companies before interviews
- **Outreach** to contacts at target companies
- **Compare** multiple opportunities side by side
```

If asked about automation limits, say plainly: career-ops does not create
accounts, handle passwords or MFA, guarantee uploads, or click Submit.
