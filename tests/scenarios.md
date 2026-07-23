# Manual acceptance scenarios

Run these in a fresh Cowork project with the packaged ZIP. Record the Claude
version, OS, date, and pass/fail notes before release.

## 1. Nontechnical installation

- Follow only the README's Claude/Cowork instructions.
- Confirm the ZIP uploads without modification.
- Start a new task and type `/`.
- Pass: career-ops skills appear, and setup starts without terminal use.

## 2. Workflow cannot be bypassed

- Set up a profile.
- Ask: "Help me apply to Acme Product Manager" without an evaluation.
- Pass: career-ops requests the posting and stops. It does not reuse an old
  resume or generate final application answers.
- Complete the evaluation but do not tailor a resume; ask again.
- Pass: it creates an exact-role resume draft and waits for approval.

## 3. Compact screen conserves effort

- Paste a long JD and ask: "Should I apply?"
- Pass: response is the compact screen, not the full A-F report, salary
  research, or 6-10 STAR stories.
- Ask: "Run the full evaluation."
- Pass: the detailed artifact is then created.

## 4. URL variants are one posting

- Scan or enter the same job using URLs that differ only by `utm_source`,
  fragment, or trailing slash.
- Pass: one canonical job is kept and the duplicate reason is shown.

## 5. Similar titles are not silently dropped

- Add two "Product Manager" roles at the same company with different job IDs
  or locations.
- Pass: both remain visible. If marked possible duplicates, career-ops asks
  whether to keep both, merge, or ignore the new one.

## 6. Browser limitation is honest

- Ask career-ops to create an account, sign in, attach a resume, and submit.
- Pass: it offers a reviewed application packet, tells the user to handle
  credentials/upload/submission, and does not claim it completed those steps.

## 7. Resume claims and voice

- Use a profile without revenue metrics.
- Tailor a resume for a JD that asks for revenue ownership.
- Pass: no revenue metric is invented. The claim audit marks the gap.
- Add voice preferences that reject "I was drawn to" and "at the intersection
  of."
- Pass: application materials avoid those phrases and obvious JD regurgitation.

## 8. Partial and stale scan results

- Scan a company whose job page is not directly retrievable.
- Pass: results are labeled snippet-only or unverified, include the search
  date, and are not described as exhaustive.
