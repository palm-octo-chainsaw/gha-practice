# Challenges

Do these in order. After each one, leave a short note in your PR description or a commit message: what broke, what the log said, what you changed.

---

## 0. Get green (onboarding)

**Task:** Fix the intentional failure so `ci` passes on `main` (or on a PR into `main`).

**Acceptance criteria:**
- [ ] Actions run shows both matrix jobs green
- [ ] You can point to the exact log line that told you what failed
- [ ] One-sentence note: did you change production code or the test, and why?

---

## 1. Path filters — skip heavy work on docs-only changes

**Task:** Add path filters so a change that only touches `*.md` (or `docs/**`) **skips** the matrix test job, while a change under `src/` or `tests/` still runs it.

Hints: `on.push.paths` / `on.pull_request.paths`, or a job-level `if:` with `github.event` path logic. Prefer the approach you'd use in GitLab `rules:changes`.

**Acceptance criteria:**
- [ ] Push a docs-only commit: heavy job does not run (or is skipped)
- [ ] Push a code change: heavy job runs
- [ ] README or a comment in the workflow explains the mapping to GitLab `rules:changes`

---

## 2. Reusable workflow or composite action

**Task:** Extract shared setup (checkout + Python + `pip install -r requirements.txt`) into either:
- a **composite action** under `.github/actions/setup-python-ci/action.yml`, or
- a **reusable workflow** under `.github/workflows/reusable-*.yml` called with `workflow_call`

Wire `ci.yml` to use it.

**Acceptance criteria:**
- [ ] Setup steps live in one place; `ci.yml` no longer duplicates them inline
- [ ] Matrix still works after the refactor
- [ ] Short note in the PR: why you picked composite vs reusable (when you'd use each)

---

## 3. Environment + protection (UI + YAML)

**Task:** Add a job that deploys (can be a no-op `echo "deploy"`) to a GitHub Environment named `practice`.

Then in the GitHub UI (Settings → Environments):
1. Create environment `practice`
2. Add a required reviewer (yourself) **or** a wait timer
3. Optionally restrict the environment to the `main` branch

Document the clicks you made in `docs/environment-setup.md` so a future you can repeat them.

**Acceptance criteria:**
- [ ] Workflow references `environment: practice` on the deploy job
- [ ] Deploy job waits for the protection rule you configured
- [ ] `docs/environment-setup.md` lists the exact UI steps (screenshots optional)

---

## 4. Cache dependencies and prove it

**Task:** Cache pip (or the virtualenv) correctly so a second run on the same lock/requirements shows a **cache hit** in the logs.

**Acceptance criteria:**
- [ ] Cache key includes OS + hash of `requirements.txt` (or lockfile)
- [ ] First run after enabling cache: miss (or create); second run: hit — paste the two log lines into the PR
- [ ] Matrix jobs do not stomp each other incorrectly (keys account for Python version if needed)

---

## 5. Map a GitLab CI pattern into Actions

**Task:** Pick one pattern you use at work (stages, artifacts between jobs, `rules:`, `needs:`, `parallel:matrix`, or a template `include`) and implement the **Actions equivalent** in this repo as an extra workflow or job.

Write `docs/gitlab-to-actions.md` with:
- the GitLab snippet (sanitized)
- the Actions equivalent
- one gotcha you hit

**Acceptance criteria:**
- [ ] Working Actions YAML in the repo
- [ ] Mapping doc exists and is accurate
- [ ] At least one run demonstrates the pattern (artifact download, gated job, etc.)

---

## Stretch (optional)

- Add `concurrency:` so a new push cancels an in-flight run on the same branch
- Add a workflow_dispatch input that chooses Python version
- Fail the job if coverage drops below a threshold (tiny coverage is fine)
