# .github

## Source documentation

For new or changed owned source code, document actual behavior and non-obvious
rationale in docstrings and inline comments, including scientific/data contracts;
verify claims against the implementation, and preserve native documentation
conventions. Avoid boilerplate and unrelated, upstream, or generated
documentation rewrites.

## Node runtime for development

- Use a patched host Node for Pyright. The `pyright[nodejs]` extra was rejected
  because its wheel currently installs an older Node and can undo runtime
  security updates during environment synchronization.

## Validation scope

Choose the smallest check that covers the changed behavior. `make qa` runs
static checks in the existing environment; it does not run model tests or builds.
For behavior changes, exercise the affected tool against a small local input.
Full suites, numerical parity, model
exports, benchmarks, live checks and package builds are explicit tasks, used
when the change or the user requires them. Documentation, file moves and metadata
edits do not require full QA. Do not synchronize environments, run sibling gates,
or repeat passed checks without a new relevant change. Mandatory full QA after
every edit was rejected because it adds unrelated work and delays feedback.

## Typing policy

Use Pyright strict mode over the maintained source, tests, scripts and local
stubs declared in `pyproject.toml`. Type-ignore comments stay disabled and
unnecessary ignores are errors. Use the maintained host Node with the pinned
Pyright dependency; do not install the `pyright[nodejs]` extra.

Explicit dynamic types remain prohibited. Use Pyright and Ruff for static
checks; custom AST typing scanners add duplicate code and maintenance.
Fix source contracts rather than adding suppressions or weakening diagnostics.

Validation calls the provisioned project Python directly. Using `uv run --no-sync`
as an environment guard was rejected because it can create an empty environment
and select development tools from the host PATH.
