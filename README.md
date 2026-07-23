# career-ops

A human-reviewed job-search copilot for Claude. It screens job postings,
builds evidence-backed resume drafts, prepares application answers, tracks
applications, and researches companies across industries.

career-ops is designed to improve application quality, not maximize unattended
application volume. It does **not** create accounts, bypass logins, guarantee
file uploads, or submit applications for you.

Adapted from [santifer/career-ops](https://github.com/santifer/career-ops).

## Install in Claude or Cowork

Plugins are available on paid Claude plans.

### Install directly from this repository

1. Open Claude. In Cowork, open the **Cowork** tab first.
2. Open **Customize** in the left sidebar, then **Plugins**.
3. In **Personal plugins**, click **+**, then **Add marketplace**.
4. Choose **Add from a repository** and enter:
   `andrew-shwetzer/career-ops-plugin-do-not-fork-currently-updating-v2-`
5. Open the added marketplace and install **career-ops**.
6. Start a new conversation or Cowork task. Type `/` or click **+** to
   confirm the career-ops skills appear.

### Install from a ZIP

1. Download `career-ops-2.0.0.zip` from this repository's latest release.
   Do not unzip it.
2. Open **Cowork > Customize > Plugins**.
3. In **Personal plugins**, click **+** and choose the custom plugin upload
   option.
4. Upload the ZIP, confirm **career-ops** appears as installed, and start a
   new task.

If the ZIP is not attached to a release yet, a developer can build it with:

```bash
python3 scripts/package_plugin.py
```

Claude's current plugin-install instructions are maintained in the
[Claude Help Center](https://support.claude.com/en/articles/13837440-use-plugins-in-claude).

### Claude Code development install

These commands are for Claude Code developers, not Cowork installation:

```bash
git clone https://github.com/andrew-shwetzer/career-ops-plugin-do-not-fork-currently-updating-v2-.git
cd career-ops-plugin-do-not-fork-currently-updating-v2-
claude --plugin-dir .
```

## Quick start

1. Say **"set up my profile"** and provide your resume.
2. Paste a job posting and ask **"should I apply?"** for a compact screen.
3. Ask **"run the full evaluation"** for promising roles.
4. Ask **"tailor my resume"**. career-ops creates a draft and a claim audit;
   review both before approving the resume.
5. Ask **"prepare my application packet"**. Copy the approved answers into
   the application yourself, upload the approved resume, and submit manually.
6. Tell career-ops when you submitted so it can update the tracker.

The workflow is deliberately gated:

```text
Screen -> Full evaluation -> Resume draft -> Human approval
       -> Application packet -> Manual submit -> Track outcome
```

career-ops will not silently reuse a generic resume for a different job.

## Skills

| Skill | What it does | Try saying |
|---|---|---|
| **screen** | Compact, low-token fit check | "Should I apply to this?" |
| **evaluate** | Full evidence-backed evaluation | "Run the full evaluation" |
| **tailor-resume** | Create and audit a role-specific resume draft | "Tailor my resume for Acme" |
| **scan** | Find possible openings on public career pages | "Scan Stripe for openings" |
| **triage** | Rank scan results with confidence labels | "Triage my pipeline" |
| **apply** | Prepare a reviewed application-answer packet | "Prepare my Acme application packet" |
| **track** | View and update application outcomes | "Show my applications" |
| **research** | Build a sourced company brief | "Research this company" |
| **outreach** | Draft evidence-backed messages | "Draft outreach to the hiring manager" |
| **compare** | Compare evaluated opportunities | "Compare my top options" |
| **help** | Explain the workflow and next safe action | "How does career-ops work?" |

## What career-ops can and cannot do

| Capability | Supported behavior |
|---|---|
| Find jobs | Best-effort public web search. Results may be incomplete or stale. |
| Score fit | Evidence-backed guidance, not a hiring prediction. |
| Tailor resumes | Drafts only from facts in your profile, with a claim audit for review. |
| Write answers | Produces copy-ready drafts and flags missing facts. |
| Fill forms | May assist when Claude has working browser tools, but never promises compatibility. |
| Accounts and login | You create accounts, sign in, handle MFA, and manage passwords. |
| Resume upload | You verify and upload the approved file. |
| Submit | You make the final submission. career-ops never auto-submits. |

## Duplicate handling

Definitive duplicates require the same ATS job ID or the same normalized
posting URL. Similar company/title combinations are shown as **possible
duplicates** for your review; they are not silently discarded. See
[`references/job-identity.md`](references/job-identity.md).

## Privacy

Profile, resume, and application files are written to the current Cowork
project or Claude Code working directory under `data/` and are excluded from
git by this repository's `.gitignore`. Claude can access information you
provide while helping you, and web-enabled skills may send search queries to
Claude's web tools.

Do not store Social Security numbers, government ID numbers, passwords,
authentication codes, full birth dates, or other secrets in the profile.
Enter sensitive form fields yourself.

## Testing

Run both checks before packaging or publishing:

```bash
claude plugin validate .
python3 scripts/validate_plugin.py
python3 scripts/package_plugin.py
```

The static validator checks plugin and marketplace metadata, component frontmatter,
resource links, workflow gates, tracker schemas, stale repository URLs, and
packaging safety. Manual acceptance scenarios live in
[`tests/scenarios.md`](tests/scenarios.md). Current results and remaining
release blockers are in [`TEST_REPORT.md`](TEST_REPORT.md).

## Project status

Version 2.0.0 is a corrective release based on public user feedback. The
audit and issue-to-fix mapping are in [`AUDIT.md`](AUDIT.md), and release
details are in [`CHANGELOG.md`](CHANGELOG.md).

## License

MIT. See [ATTRIBUTION.md](ATTRIBUTION.md) for credits.
