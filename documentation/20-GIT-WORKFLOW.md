# Git Workflow

```
local (development) → cherry-pick → dev (testing) → merge → prod (production)
```

| Branch | Purpose | What to commit |
|--------|---------|----------------|
| local | Developer workspace | Everything: code, specs, plans |
| dev | Test environment | Only working code (completed features) |
| prod | Production | Only tested code |
| main | Frozen (archive) | Nothing |

## Commands

| Action | Command |
|--------|---------|
| Commit | `/commit` |
| Push | `/push` |
| Cherry-pick to dev | `/cherry-pick` |
| Merge to prod | `/merge-to-prod` |
| Status | `/git-status` |
