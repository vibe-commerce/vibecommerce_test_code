# Deploy Procedures

> ⚠️ **Не применимо в базовом шаблоне.** `vibecommerce_test_code` работает только
> на ветках `local` + `main`, без DEV/PROD-деплоя (см. CLAUDE.md). Скрипты
> `deploy-dev.sh` / `deploy-prod.sh`, окружения и `_status/{DEV,PROD}.md` ниже —
> образец для форка, если студент добавит боевой деплой.

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
