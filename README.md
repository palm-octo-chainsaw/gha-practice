# gha-practice

**Goal:** get fluent in GitHub Actions if you already know GitLab CI / Jenkins / Cloud Build.

This is a **drill yard**, not a tutorial dump. The app under test is deliberately tiny so the pipeline is the product.

## How to use this repo

1. Clone (or work on GitHub.dev / Codespaces).
2. Push to `main` or open a PR — CI will run.
3. **First run is meant to fail.** Open the Actions run, read the logs, fix the deliberate mismatch (see below), push again until green.
4. Work through [`CHALLENGES.md`](./CHALLENGES.md) in order. Each challenge has acceptance criteria. Do not skip to the "answer" — the point is the muscle memory of editing YAML and reading logs.
5. Prefer small commits per challenge so the Actions history stays readable.

### Mental model: GitLab CI → Actions

| GitLab CI | GitHub Actions |
|-----------|----------------|
| `.gitlab-ci.yml` | `.github/workflows/*.yml` |
| `stages` + jobs | jobs + `needs` / job order |
| `rules:` / `only:` / `changes:` | `on:` + `paths` / `if:` |
| `artifacts:` | `actions/upload-artifact` / `download-artifact` |
| `cache:` | `actions/cache` or setup-action cache |
| `include:` / templates | reusable workflows / composite actions |
| protected environments | Environments + protection rules (UI) |

## What's already here

- `.github/workflows/ci.yml` — push/PR workflow with a **job matrix** (two Python versions) and a deliberate fail path.
- `src/hello.py` + `tests/test_hello.py` — minimal pytest target.
- `CHALLENGES.md` — progressive drills with acceptance criteria.

### The intentional failure

`hello()` currently returns `"Hello, World!"` but the test expects `"Hello, Actions!"`.
Your first drill: make CI green (change the code **or** the test — either is fine; note which you chose and why).

## Local check (optional)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Topics

`github-actions` · `ci` · `devops` · `practice` · `gitlab-ci-migration`
