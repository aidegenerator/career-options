# Test report

Date: 2026-07-23
Branch: `codex/reddit-audit-v2`

## Automated checks

| Check | Result |
|---|---|
| `claude plugin validate .` | Pass |
| Marketplace strict validation | Pass |
| `python3 scripts/validate_plugin.py` | Pass, 157 cross-file checks |
| Validator unit tests | Pass, 4 tests |
| Safe upload ZIP build | Pass |
| ZIP manifest at archive root | Pass |
| ZIP excludes `.git`, `data`, `config`, tests, and development scripts | Pass |
| `git diff --check` | Pass |

Generated artifact: `dist/career-ops-2.0.0.zip`

## Runtime smoke test

A synthetic profile and Director of Operations posting are available under
`tests/fixtures/`. A live Claude Code prompt test was attempted in an isolated
temporary workspace, but the local Claude CLI returned:

`Not logged in - Please run /login`

No inference ran and no runtime behavior was claimed as verified.

## Release blockers

- Complete the eight Cowork acceptance scenarios in `tests/scenarios.md`.
- Test ZIP upload and skill discovery on macOS and Windows.
- Validate generated resume claims with at least two job seekers.
- Attach the verified ZIP to the public release only after those checks pass.
