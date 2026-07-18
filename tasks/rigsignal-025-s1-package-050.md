# Task: rigsignal-025-s1-package-050 — Integration 0.5.0: probe as TSDS dimension

Session: 2026-07-18-s2-spool. Workspace: the git worktree you are launched in (branch
`codex/rigsignal-025-s1-package-050` of `/home/dev/coding/RigSignal-Integration`, cut
from main `58b1263` / package 0.4.0). Do NOT commit — the orchestrator commits after
review.

## Contract (RIGSIGNAL-025-SPEC.md §S1, the package-side slice)

- **D4:** Integration package **0.5.0** — breaking TSDS mapping change on the ebpf
  stream (`rigsignal.ebpf.probe` becomes a time-series dimension). No reindex/backfill;
  old backing indices age out read-only.
- Deploy choreography step 1 (this task): "Package 0.5.0: `rigsignal.ebpf.probe` →
  `dimension: true`; gates pass." Canary/rollover/daemon are later orchestrator steps —
  NOT yours.
- Rationale (for the changelog): the probe discriminant was not a dimension, so all
  probe docs sharing a tick timestamp would collide on one `_tsid`; the daemon's interim
  workaround (per-probe 0–10 ms timestamp offsets) is retired daemon-side in 0.2.5.

## Scope — exactly three files

1. `data_stream/ebpf/fields/fields.yml` — the `rigsignal.ebpf.probe` keyword (line ~24):
   add `dimension: true`. Touch nothing else in the file.
2. `manifest.yml` — `version: 0.4.0` → `0.5.0`.
3. `changelog.yml` — new `0.5.0` entry on top, matching the existing entry style
   (`type: breaking-change`, link to https://github.com/MathewRJ/RigSignal-Integration/issues/5):
   describe the probe dimension promotion + `_tsid` series break at the rollover
   boundary (field names/values unchanged, dashboards unaffected).

Do NOT touch any other data stream, pipeline, or the kibana/ assets.

## Acceptance criteria

- `elastic-package check` passes from the package root.
- `git diff` shows only the three files above.
- Summary: 2 sentences + full `elastic-package check` output tail.

## STM contract

Before starting: `CHRONO_SESSION=2026-07-18-s2-spool bash /home/dev/coding/Workflow/scripts/stm.sh recall`.
Save non-obvious discoveries via `stm.sh save … --kind learning` (STM_AGENT=codex@nuc).
If STM is unreachable from your sandbox (network blocked), note it once and proceed.
