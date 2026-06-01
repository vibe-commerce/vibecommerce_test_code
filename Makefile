.PHONY: install run test lint format clean sync-agents verify-agents

install:
	@if command -v uv >/dev/null 2>&1; then \
		uv pip install -e ".[dev]"; \
	else \
		pip install -e ".[dev]"; \
	fi

run:
	@echo "Stub: модули — read-only. Запускай скрипты из _modules/<NN>/scripts/ напрямую"
	@echo "  python _modules/05-ads-optimization/scripts/abcdx_analysis.py"

test:
	pytest tests/ -v

lint:
	ruff check _modules/ scripts/ tests/

format:
	ruff format _modules/ scripts/ tests/

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name .pytest_cache -prune -exec rm -rf {} +
	find . -type d -name .ruff_cache -prune -exec rm -rf {} +

# Cross-agent compatibility (Claude Code + OpenAI Codex)
sync-agents:
	bash scripts/sync-agents-config.sh

verify-agents:
	bash scripts/verify-cross-compat.sh
