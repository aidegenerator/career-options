# Workflow gates

These gates are the source of truth for application work.

## Artifact sequence

```text
Screened
  -> Evaluated
  -> Resume Draft
  -> Resume Ready (user approved)
  -> Application Ready (answers reviewed)
  -> Applied (user confirmed submission)
```

`Skipped`, `Rejected`, `Withdrawn`, and `Accepted` are handled by
`references/states.md`.

## Gate 1: Screen before spending

- A pasted job description or "should I apply?" request uses the compact
  `screen` skill by default.
- Run the full `evaluate` skill only when the user explicitly asks or the
  screen meets the user's configured threshold.
- A screen is guidance, not a hiring-outcome prediction.

## Gate 2: Exact-role evaluation

Before resume tailoring or application preparation:

- Match the company, role, and canonical job key.
- Do not reuse an evaluation from a similarly named role.
- If the posting changed materially, create a new evaluation.

## Gate 3: Exact-role resume

Before application preparation:

- A resume draft must reference the same canonical job key.
- Every changed or added claim must map to source evidence in the profile or
  source resume.
- Unsupported facts remain questions or placeholders; never infer them.
- The resume stays `Resume Draft` until the user explicitly approves it.

## Gate 4: Application-answer review

- Produce answers as a packet before any form interaction.
- Show source evidence or `NEEDS USER INPUT` for factual claims.
- Run the anti-template quality check.
- Ask the user to review the packet.

## Gate 5: User-controlled submission

career-ops never:

- creates accounts;
- enters or stores passwords, MFA codes, government identifiers, or full
  birth dates;
- claims it can bypass bot detection or access controls;
- promises file upload compatibility;
- clicks the final Submit button.

Only set status to `Applied` after the user confirms that they submitted.

## Low-score override

The default full-evaluation threshold is 3.5/5. A user may pursue a role below
the threshold. Show the main gap once, ask whether they want to continue, and
respect their decision without repeatedly discouraging them.
