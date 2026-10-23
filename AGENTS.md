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
