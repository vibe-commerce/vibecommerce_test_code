# Testing Strategy

## Levels

| Level | What | Tool | When |
|-------|------|------|------|
| Lint | Code style, errors | `ruff check` / `eslint` | Every change |
| Unit | Function logic | `pytest tests/` | Every change |
| Integration | Collectors + APIs (with mocks) | `pytest tests/ -m integration` | Before deploy |
| E2E | Full pipeline | `pytest tests/e2e/` | Before release |
| Smoke | HTTP check after deploy | `./scripts/smoke-test.sh` | After deploy |

## Commands

```bash
make lint          # Lint only
make test          # Unit tests
make test-e2e      # E2E tests
```

## Feedback Loop

After generating or modifying code — always run tests:
1. `make lint`
2. `make test`
3. If fails → fix → retry (max 3 attempts)
4. Only after green tests → task is done
