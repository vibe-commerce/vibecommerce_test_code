# Troubleshooting

## Common Issues

### Deploy fails
1. Check branch: `git rev-parse --abbrev-ref HEAD`
2. Check remote sync: `git fetch origin && git status`
3. Check logs: `/logs`

### Tests fail after changes
1. Run `make lint` — check for syntax errors
2. Run `make test` — see specific failures
3. Check error-log: `.claude/data/error-log.md`

## Error Registry
See [80-ERROR-REGISTRY.md](80-ERROR-REGISTRY.md) for documented errors with root causes.
