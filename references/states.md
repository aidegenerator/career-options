# Application States

Source of truth for the status field in data/applications.md.

## State Machine

| State | Description | Can Transition To |
|---|---|---|
| Evaluated | Full JD evaluation saved | Resume Draft, Skipped |
| Resume Draft | Exact-role resume created but not user-approved | Resume Ready, Evaluated, Skipped |
| Resume Ready | User approved the exact-role resume | Application Ready, Skipped |
| Application Ready | User reviewed the application-answer packet | Applied, Resume Draft, Skipped |
| Applied | Application submitted | Responded, Interview, Rejected, Withdrawn |
| Responded | Company sent a response | Interview, Rejected |
| Interview | Interview scheduled or in progress | Offer, Rejected, Withdrawn |
| Offer | Received an offer | Accepted, Withdrawn |
| Accepted | Accepted the offer | (terminal) |
| Rejected | Application rejected at any stage | (terminal) |
| Withdrawn | You withdrew from the process | (terminal) |
| Skipped | Decided not to apply after evaluation | (terminal) |

## Rules

1. The Status field in applications.md must contain EXACTLY one of these values
2. Status is case-insensitive when reading but should be written in Title Case
3. Withdrawn can be reached from any non-terminal state
4. Only update status with user confirmation
5. `Resume Ready` requires explicit user approval; file creation alone only
   reaches `Resume Draft`
6. `Applied` requires the user's confirmation that they submitted the
   application; form preparation does not count
