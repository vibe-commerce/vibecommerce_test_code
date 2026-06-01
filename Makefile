.PHONY: install install-claude-tools run test test-e2e lint format clean sync-agents verify-agents

install:
	uv pip install -e ".[dev]" 2>/dev/null || pip install -e ".[dev]"

install-claude-tools:
	./scripts/install-claude-tools.sh

run:
	@echo "Stub: модули — read-only. Запускай скрипты из _modules/<NN>/scripts/ напрямую"
	@echo "  python _modules/05-ads-optimization/scripts/abcdx_analysis.py"

test:
	pytest _modules/ -v 2>/dev/null || echo "Нет тестов — запускай скрипты модулей напрямую"

lint:
	ruff check _modules/ scripts/ 2>/dev/null || echo "Установи ruff: pip install ruff"

format:
	ruff format _modules/ scripts/ 2>/dev/null || echo "Установи ruff: pip install ruff"

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name .pytest_cache -prune -exec rm -rf {} +
	find . -type d -name .ruff_cache -prune -exec rm -rf {} +

# Cross-agent compatibility (Claude Code + OpenAI Codex)
sync-agents:
	bash scripts/sync-agents-config.sh

verify-agents:
	bash scripts/verify-cross-compat.sh
