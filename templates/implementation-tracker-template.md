# 06 · Implementation tracker: [Business name]

Source of truth: `06-tracker.csv` (columns below). This Markdown view is regenerated for status updates and reports.

> `implemented` = deployed. `validated` = QA evidence accepted at G5. Never mark validated because code was written or a deploy finished.

## Columns

| Column | Content |
|---|---|
| task_id | `T-###`, never reused |
| description | Concrete: template / URLs / files |
| category | On-page / Off-page / Technical / Local / Analytics / Content / International / AI-search |
| finding_ids | e.g. `TEC-004, ONP-012` |
| horizon | quick-win / high-priority / short-term / medium-term / long-term |
| priority | P0-P3 |
| expected_impact | Mechanism and direction, no numeric promise |
| effort | 1-5 |
| owner_role | Accountable party for the task, e.g. frontend dev, Arabic content writer, client marketing |
| executor | Party that actually performs the change: `claude`, `owner`, or a named role (e.g. `client-developer`), as recorded in the change log. Executor doesn't bypass approval: the B3 rules in SKILL.md (Approval gates) still decide whether the full G4 proposal or the owner-executed path applies |
| dependencies | Task IDs, access, decisions, inputs |
| acceptance_criteria | Observable conditions defining done |
| validation_method | QA method and timing (immediate / after recrawl) |
| change_id | `CHG-###` from 07-changes/change-log.md |
| status | open → proposed → approved → in-progress → implemented → validated → monitoring, plus blocked and won't-fix. Meanings are in SKILL.md (Status lifecycle). Owner actions are `implemented` only after the owner confirms them with evidence; `monitoring` = validated, effect still being measured |
| implemented_date / validated_date | YYYY-MM-DD |
| evidence | Path in 08-qa/ |
| notes | |

## Status summary ([YYYY-MM-DD])

| Status | Count | Tasks |
|---|---|---|
| validated | | |
| implemented (QA pending) | | |
| in-progress | | |
| approved | | |
| proposed (awaiting G4) | | |
| blocked | | |
| open | | |
| monitoring | | |
| won't-fix | | |

## Blocked items

| Task | Blocked by | Needed from | Since |
|---|---|---|---|
