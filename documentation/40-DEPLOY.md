# Deploy Procedures

## Environments

| Env | Branch | Script | Status |
|-----|--------|--------|--------|
| DEV | dev | `./scripts/deploy-dev.sh` | `_status/DEV.md` |
| PROD | prod | `./scripts/deploy-prod.sh` | `_status/PROD.md` |

## Workflow

```
local → /cherry-pick → dev → /deploy-dev → test → /merge-to-prod → /deploy-prod
```

## After Every Deploy

1. Test that deploy works
2. Run `/docs` to update documentation
3. Update VERSION for significant changes (semver)
4. Update changelog (`_changelogs/`)
5. Check branch sync
