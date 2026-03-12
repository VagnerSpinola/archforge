# Contributing

## Development Environment

1. Install Python 3.12 or newer.
2. Create and activate a virtual environment.
3. Install dependencies with `make install`.
4. Install the git hooks with `pre-commit install`.

## Workflow

1. Create a focused branch for the change.
2. Keep architectural boundaries explicit and avoid leaking framework details into domain code.
3. Add or update tests alongside the implementation.
4. Run `make lint`, `make typecheck`, and `make test` before opening a pull request.

## Pull Requests

Pull requests should describe the problem, the chosen implementation, and any tradeoffs. If a change affects generated output, include the generated files or test coverage that demonstrates the new behavior.

## Coding Standards

- Use Python 3.12 features where they improve clarity.
- Prefer `pathlib` for filesystem work.
- Keep template changes aligned with the architectural boundaries documented in `docs/architecture.md`.
- Introduce patterns only where they clarify the design.