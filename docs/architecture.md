# contextscore Architecture

## Scaffolding Decisions

| Concern | Choice | Rationale |
| :--- | :--- | :--- |
| **Dependencies (Python)** | `uv` | Modern, fast dependency management and environment creation |
| **Frontend Framework** | Streamlit | Python-native interactive UI with minimal boilerplate |
| **Backend Processing** | Python (pandas, sentence-transformers) | Semantic scoring engine |
| **Linting & Formatting** | `pre-commit` (ruff) | Automated code quality and consistency checks |
| **Type Checking** | `pre-commit` (mypy) | Catch type errors early |
| **Testing** | `pytest` | Standard Python testing framework |
| **Code Coverage** | `pytest-cov` + CodeCov | Visibility into test efficacy, automated tracking in CI |
| **CI/CD** | GitHub Actions | Automated build, test, lint, and typecheck on push/PR |
| **Deployment** | Posit Connect Cloud | Managed hosting for Streamlit applications |

## Project Scaffolding Sequence

1. Configure dependency management with uv.
2. Build simple scoring module with an `embed()` function that returns an embedding generated with sentence-transformers.
3. Add simple pytest to test testing functionality.
4. Create boilerplate Streamlit app with a button to test integration with scoring module.
5. Deploy Streamlit app to Posit Connect Cloud.
6. Add pre-commit hooks for `ruff` and `mypy`.
7. Set up GitHub Actions workflow that runs tests on push/PR.
8. Add CodeCov with `pytest-cov`.
9. Write `README.md`.

> Design decisions are documented in [`design.md`](./design.md).
