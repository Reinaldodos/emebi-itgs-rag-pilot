# Repository Guidelines

## Project Structure & Module Organization

Implementation scripts live under `src/`, automated tests under `tests/`, and corpus documentation and metadata under `corpus/`. Keep downloaded documents, generated output, and local caches ignored. The numbered extraction and parsing scripts run directly from the checkout; this is not an installable Python package.

## Build, Test, and Development Commands

Use Python 3.11 or newer and uv. `pyproject.toml` declares minimum dependency versions; `uv.lock` pins the complete resolution. Python 3.13 is the verified interpreter for this environment.

- `make setup` (or `uv sync --locked`) — synchronize runtime and development dependencies into `.venv/`.
- `make test` (or `uv run --locked pytest`) — run the automated test suite.
- `uv run --locked pytest --collect-only` — check test discovery and imports without opening corpus documents.

When intentionally updating dependencies, run `uv lock --upgrade`, synchronize, and validate before committing the manifest and lockfile together. PDF validation needs the system `pdfinfo` and `pdftotext` executables; Excel validation needs `libreoffice`. See README for installation and scope. These tools are not Python dependencies.

## Coding Style & Naming Conventions

Use the formatter and linter standard to the chosen language, commit their configuration, and run both before opening a pull request. Prefer four spaces for Python and two spaces for JSON, YAML, and JavaScript/TypeScript unless an adopted formatter specifies otherwise. Use descriptive names: `snake_case` for Python files and functions, `PascalCase` for classes and UI components, and `kebab-case` for documentation and static assets. Keep modules focused and avoid committing generated files.

## Testing Guidelines

Every behavior change should include tests. Name tests after the behavior under test and keep fixtures close to the suite that uses them. Cover success paths, invalid inputs, and regressions. Run the unittest-based suite through `uv run --locked pytest`; no repository-wide coverage threshold is defined. Parsing tests currently require the local, Git-ignored PDF documented in README, so distinguish import/discovery success from full test execution when it is absent.

## Commit & Pull Request Guidelines

There is no usable Git history from which to infer an existing convention. Use concise, imperative commit subjects, optionally following Conventional Commits (for example, `feat: add prompt template loader`). Keep commits focused. Pull requests should explain the change and validation performed, link relevant issues, and include screenshots or sample output for user-visible changes. Call out configuration changes, migrations, and follow-up work explicitly.
