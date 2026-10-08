.PHONY: typecheck

typecheck:
	uv run --locked pyright --project . --warnings
	bash -o pipefail -c 'rg --files --hidden --no-ignore --glob "*.py" --glob "*.pyi" --null tools | xargs -0 uv run --locked ruff check --config pyproject.toml --select TID251,ANN401 --ignore-noqa --no-force-exclude --'
