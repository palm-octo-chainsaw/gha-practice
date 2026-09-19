# Challenge 1 evidence: path filters behave like GitLab `rules:changes`

## The mapping (one line)

`on.push.paths` + `on.pull_request.paths` in `.github/workflows/ci.yml` ==
`rules: - changes: [src/**, tests/**, .github/workflows/**]` in `.gitlab-ci.yml`.

Difference worth internalizing: GitLab evaluates `rules:changes` *after* creating a
pipeline, so a non-matching change shows up as a skipped/ignored pipeline. GitHub
evaluates `on.*.paths` *before* creating a run, so a non-matching change produces
**no run at all** — the Actions tab simply gains no entry for that commit.

## Half 1 — code/workflow change: the matrix job runs

- Commit: `eb8cb8c` (`docs: map path filters to GitLab rules:changes`) — touched
  `.github/workflows/ci.yml`, which matches `.github/workflows/**`.
- Run: https://github.com/palm-octo-chainsaw/gha-practice/actions/runs/35409277560 — `success`
  (both `test (py3.11)` and `test (py3.12)` legs, plus `summarize`).

Earlier code-path evidence on the same branch:
https://github.com/palm-octo-chainsaw/gha-practice/actions/runs/35408188604 (commit `d880039`, `src`/workflow change, green).

## Half 2 — docs-only change: no run is created

- Commit: the one that adds this file — touches `docs/**` only, matching none of the
  three path globs.
- Expected and observed: `gh run list --branch feature/fine-grain-workflow-run` shows
  **no new run** whose `headSha` equals that commit. The newest run stays `35409277560`.

Reproduce it yourself:

```bash
# before
gh run list --branch "$(git branch --show-current)" --limit 3 --json databaseId,headSha,conclusion

git commit --allow-empty=false -m "docs: touch" -- docs/ && git push

# after: same list, no entry for the new SHA
gh run list --branch "$(git branch --show-current)" --limit 3 --json databaseId,headSha,conclusion
git log -1 --format=%H   # this SHA appears nowhere above
```

## Acceptance criteria status

- [x] Push a docs-only commit: heavy job does not run (no run created — see Half 2)
- [x] Push a code change: heavy job runs (run `35409277560`, green — see Half 1)
- [x] README + workflow comment explain the mapping to GitLab `rules:changes`
