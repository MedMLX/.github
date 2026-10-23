.DEFAULT_GOAL := qa
.PHONY: lint typecheck qa

typecheck:
	uv run --locked --no-sync --offline pyright --project . --warnings
	bash -o pipefail -c 'rg --files --hidden --no-ignore --glob "*.py" --glob "*.pyi" --null tools typings | xargs -0 uv run --locked --no-sync --offline ruff check --config pyproject.toml --select TID251,ANN401 --ignore-noqa --no-force-exclude --'

lint:
	uv run --locked --no-sync --offline ruff check tools typings

qa: lint typecheck
