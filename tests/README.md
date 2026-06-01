# `tests/` — регрессионный контур шаблона

Last Updated: 2026-06-02

## Что здесь

Минимальный набор тестов целостности шаблона (`make test` → `pytest tests/ -v`):

- `test_template_integrity.py` — валидность install-конфига (PEP 508 имя),
  синхрон версий (VERSION ↔ pyproject), отсутствие личных путей `/Users/...`,
  парсимость всех JSON/YAML/TOML, резолв локальных Markdown-ссылок.
- `test_module_05_pipeline.py` — smoke pipeline модуля 05
  (generate-sales → generate-ads → ABCDX → funnel) в копии модуля, без правки
  tracked `data-demo/`.
- `test_cli_tools.py` — smoke CLI-утилит из `scripts/` (xlsx → markdown).

## Зачем

Появился в 0.3.1 (план `backlog/plans/2026-06-01-fix-template-integrity.md`):
до этого `make test` давал ложноположительный результат (0 собранных тестов
маскировались через `|| echo`). Эти тесты ловят дефекты QA-прогона, чтобы они
не вернулись.

## Как пользоваться

```bash
make install          # ставит pytest + зависимости модулей
make test             # pytest tests/ -v
pytest tests/ -m "not slow"   # без тяжёлого funnel-теста (matplotlib)
```

Маркеры (`slow`, `e2e`) объявлены в `pyproject.toml` → `[tool.pytest.ini_options]`.

## Связанные

- Родитель: [`../README.md`](../README.md)
- План-источник: [`../backlog/plans/2026-06-01-fix-template-integrity.md`](../backlog/plans/2026-06-01-fix-template-integrity.md)
- Конфиг pytest: [`../pyproject.toml`](../pyproject.toml)
