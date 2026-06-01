# Task Decomposition: {feature}

Source spec: `_specs/{feature}/tech-spec.md`
Created: {date}

## Rules
- Each task = 1 atomic change (can be done in 1 Claude Code session)
- Each task has clear input, output, and acceptance criteria
- Tasks in same wave can run in parallel (no dependencies between them)
- Task in wave N depends only on tasks from wave N-1 or earlier

## Tasks

| # | Task | Wave | Depends On | Status | Files | Acceptance Criteria |
|---|------|------|------------|--------|-------|---------------------|
| 1 | {описание} | 1 | — | TODO | {файлы} | {что значит "готово"} |
| 2 | {описание} | 1 | — | TODO | {файлы} | {критерии} |
| 3 | {описание} | 2 | 1, 2 | TODO | {файлы} | {критерии} |

Statuses: TODO / WIP / DONE / BLOCKED

## Notes
- Max 3 review iterations per task
- If blocked after 3 attempts → escalate to user
