---
name: screen
description: "Give a compact, low-token fit screen before spending time on a full job evaluation. Use by default when someone pastes a job description, asks 'should I apply', 'is this a fit', 'quick score', or wants a first-pass decision. Do not use for an explicitly requested full evaluation."
argument-hint: "<job posting URL, file, or pasted text>"
user-invocable: true
allowed-tools:
  - Read
  - WebFetch
---

# Screen a Job

Give the user a fast, evidence-backed decision before running expensive
research or producing a full report.

Read `references/workflow-gates.md`, `references/scoring-rubric.md`, and
`references/job-identity.md`.

## 1. Load the minimum context

Read `data/profile.yml` and `data/resume.md` if available. If the profile is
missing, run the setup flow before scoring.

Accept pasted text, a readable file, or a URL. For an inaccessible URL, ask
the user to paste the job description. Do not repeatedly retry a blocked page.

Extract only:

- company, role, location, and canonical job key;
- hard requirements;
- target seniority;
- up to five core responsibilities.

## 2. Check hard constraints first

Compare location, work authorization, required licenses, compensation floor,
and explicit user exclusions. Distinguish:

- `Pass`
- `Conflict`
- `Unknown - ask user`

Do not turn an unknown into a rejection.

## 3. Score compactly

Use:

- hard-requirement evidence: 50%;
- seniority and scope: 25%;
- domain and role alignment: 15%;
- logistics and user preferences: 10%.

Every positive match must point to a specific profile field, role, project, or
proof point. Never invent evidence.

## 4. Return one decision card

```markdown
## Job Screen: {Company} - {Role}

**Score:** {X.X}/5.0
**Decision:** Full evaluate / User choice / Skip
**Confidence:** Full JD / Partial JD / Title-only
**Job key:** {canonical key or "fallback"}

**Why:** {two or three evidence-backed sentences}

**Strongest evidence**
- {source-backed match}
- {source-backed match}

**Main risk**
- {gap, conflict, or missing information}

**Next step:** {one action}
```

Decision bands:

- 3.5-5.0: Recommend a full evaluation.
- 2.5-3.4: User choice; explain the tradeoff without discouraging repeatedly.
- 1.0-2.4: Recommend skipping unless the user has a strategic reason.

If the user asks to continue, run the full `evaluate` workflow. Do not add a
screen-only result to the application tracker.
