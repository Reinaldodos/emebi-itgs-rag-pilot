# Repository Guidelines

## Project Structure & Module Organization

This repository is currently an empty scaffold; no application code, tests, or build configuration have been committed. Keep the root uncluttered as the project develops. Place implementation code under `src/`, automated tests under `tests/`, documentation under `docs/`, and non-code resources under `assets/`. Mirror source paths in the test tree—for example, test `src/services/generator.py` with `tests/services/test_generator.py`. Store only small, necessary assets in Git; keep generated output and local caches ignored.

## Build, Test, and Development Commands

No build or test commands are defined yet. When introducing a language or framework, add its standard manifest and expose a small, documented command set through a `Makefile` or package scripts. Contributors should be able to discover and run common tasks consistently, such as:

- `make setup` — install or synchronize development dependencies.
- `make test` — run the complete automated test suite.
- `make lint` — run formatting and static-analysis checks.
- `make run` — start the project locally.

Update this guide and the project README when these commands become available. Do not document commands that have not been implemented.

## Coding Style & Naming Conventions

Use the formatter and linter standard to the chosen language, commit their configuration, and run both before opening a pull request. Prefer four spaces for Python and two spaces for JSON, YAML, and JavaScript/TypeScript unless an adopted formatter specifies otherwise. Use descriptive names: `snake_case` for Python files and functions, `PascalCase` for classes and UI components, and `kebab-case` for documentation and static assets. Keep modules focused and avoid committing generated files.

## Testing Guidelines

Every behavior change should include tests. Name tests after the behavior under test and keep fixtures close to the suite that uses them. Cover success paths, invalid inputs, and regressions. Once a framework is selected, document its exact invocation and any coverage threshold here; until then, do not claim a repository-wide coverage target.

## Commit & Pull Request Guidelines

There is no usable Git history from which to infer an existing convention. Use concise, imperative commit subjects, optionally following Conventional Commits (for example, `feat: add prompt template loader`). Keep commits focused. Pull requests should explain the change and validation performed, link relevant issues, and include screenshots or sample output for user-visible changes. Call out configuration changes, migrations, and follow-up work explicitly.
