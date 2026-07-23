# Job identity and duplicate rules

Duplicate handling must be conservative and explainable.

## Canonical job key

Build the key in this order:

1. **ATS job ID:** Extract the stable posting or requisition ID from the page,
   URL path, or structured result. Store as `{ats}:{id}`.
2. **Canonical URL:** If no job ID exists, normalize the posting URL:
   - lowercase the scheme and host;
   - remove the fragment;
   - remove tracking parameters (`utm_*`, `source`, `ref`, `referrer`);
   - remove a trailing slash;
   - preserve path segments and any query parameter that identifies the job.
3. **Fallback fingerprint:** If neither is available, use normalized company,
   exact normalized title, and normalized location. Mark confidence `fallback`.

Keep both `Job Key` and `Posting URL` in the tracker.

## Duplicate decisions

| Match | Decision |
|---|---|
| Same ATS job ID | Definitive duplicate |
| Same canonical URL | Definitive duplicate |
| Same company + title + location, but different IDs/URLs | Possible duplicate |
| Similar title or company only | Not a duplicate |
| Same title at different locations | Not a duplicate unless ATS ID is the same |
| Reposted role with a new requisition ID | New posting; optionally link it to the prior role |

## Required behavior

- Collapse definitive duplicates within the same scan.
- Never silently discard a possible duplicate.
- Show both records, the fields that matched, and the fields that differ.
- Let the user choose `Keep Both`, `Merge`, or `Ignore New`.
- Record that decision in `data/scan-history.md`.
- A role being seen previously does not prove it is still live. Label freshness
  separately from identity.
