---
name: apply
description: "Prepare a reviewed, copy-ready application packet for one evaluated role with an approved exact-role resume. Never auto-submits. Use when someone says 'help me apply', 'prepare my application', 'answer these application questions', or 'application for'."
argument-hint: "<company and role, plus pasted application questions when available>"
user-invocable: true
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Glob
---

# Prepare an Application Packet

Prepare accurate, role-specific answers for the user to review and enter.

Read `references/workflow-gates.md`, `references/job-identity.md`, and
`references/states.md`.

**CRITICAL: never auto-submit an application.** Account creation, login, MFA,
passwords, sensitive identity fields, resume upload, and the final Submit
button remain under the user's control.

## Step 1: Identify the exact posting

Resolve the company, role, canonical `Job Key`, and `Posting URL`.

Load:

1. `data/profile.yml` and `data/resume.md`;
2. the exact-key row in `data/applications.md`;
3. the exact-key evaluation from `data/evaluations/`;
4. the exact-key resume and claim audit from `data/resumes/`;
5. optional company research from `data/research/`.

Do not use a resume or evaluation merely because the company and title look
similar. Follow `references/job-identity.md`.

## Step 2: Enforce the gates

Stop at the first unmet gate:

1. **No exact-role evaluation:** ask for the posting and run the screen/full
   evaluation workflow before continuing.
2. **Score below the configured threshold:** show the main gap once and ask
   whether the user still wants to continue. Respect the answer.
3. **No exact-role resume:** run the tailoring workflow.
4. **Resume status is `Resume Draft`:** ask the user to review the resume and
   claim audit. Do not continue until the user explicitly approves it.
5. **Resume status is not `Resume Ready`:** explain which artifact is missing.

Never substitute one of the user's older or generic resumes to get around a
missing artifact.

## Step 3: Collect the actual questions

Ask the user to paste the application questions or fields. If they only
provide a URL and its form is not readable, ask them to paste the text instead
of repeatedly retrying access.

For private or sensitive fields, return `ENTER YOURSELF`:

- password or MFA code;
- Social Security or government ID number;
- full birth date;
- demographic/EEO answers;
- disability or veteran disclosure;
- signature or legal attestation.

Explain that optional EEO fields are the user's choice. Do not answer them.

## Step 4: Draft with evidence

For every answer:

- use only facts in the profile, source resume, approved tailored resume,
  evaluation, or sourced company research;
- cite the internal source used;
- write `NEEDS USER INPUT` when a fact is absent;
- follow the user's `voice` preferences;
- answer yes/no fields directly;
- do not imply a relationship, credential, tool, metric, or work authorization
  status that is not documented.

Common fields:

| Field | Source and behavior |
|---|---|
| Name, email, phone | Direct copy from profile |
| Resume | Point to the approved exact-role file; user verifies and uploads it |
| Work authorization | Direct profile value or `NEEDS USER INPUT` |
| Salary | Profile target plus stated JD range; ask before changing the target |
| Start date | `NEEDS USER INPUT` unless the user provided it |
| Why this role? | Role requirements plus source-backed experience |
| Why this company? | Sourced company fact plus user's specific motivation |
| Behavioral question | One real story; ask for missing Situation/Action/Result facts |

## Step 5: Cover letter when requested

Do not create a cover letter unless the form requires one or the user asks.
When needed, keep it specific and source-backed:

1. a concrete reason for this role or company;
2. one or two relevant accomplishments;
3. a direct closing.

Apply the anti-template check:

- remove phrases listed in `voice.avoid_phrases`;
- avoid "I was drawn to," "at the intersection of," "I am excited to apply,"
  and generic praise unless the user explicitly prefers them;
- do not repeat a sentence from the JD with the subject changed to "I";
- do not manufacture enthusiasm, familiarity, or company knowledge;
- vary sentence structure and prefer the user's normal vocabulary.

## Step 6: Present the complete packet

Write `data/applications/{company-slug}-{role-slug}-packet.md`:

```markdown
# Application Packet: {Company} - {Role}

Job Key: {job-key}
Posting URL: {canonical-url}
Approved resume: {resume-file}

| # | Field or Question | Draft Answer | Evidence | Review |
|---|---|---|---|---|
| 1 | {question} | {answer or NEEDS USER INPUT} | {profile/resume/evaluation source} | Pending |

## User-entered fields

- {sensitive, legal, login, or unknown fields}

## Pre-submit checklist

- [ ] Every answer is accurate
- [ ] Resume matches this Job Key
- [ ] Resume file opens and renders correctly
- [ ] Dates, salary, authorization, and contact details are correct
- [ ] User completed sensitive and voluntary fields
- [ ] User reviewed the final form before submitting
```

Show all answers in chat. Ask the user to correct missing facts and approve the
packet. Do not describe a form as filled, uploaded, or submitted unless the
user confirms that action occurred.

## Step 7: Track honestly

After the user approves the packet:

- set status to `Application Ready`;
- add the packet path to Notes.

After the user confirms they submitted:

- set status to `Applied`;
- set Date Applied to today;
- record the confirmed resume filename.

If they have not confirmed submission, leave the status at
`Application Ready`.
