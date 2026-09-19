# Challenge 1 evidence: path filters == GitLab `rules:changes`

## The mapping (one line)

`on.push.paths` + `on.pull_request.paths` in `.github/workflows/ci.yml` ==
`rules: - changes: [src/**, tests/**, .github/workflows/**]` in `.gitlab-ci.yml`.

Two differences worth internalizing, both learned the hard way while producing the
evidence below:

1. **Skipped vs. never created.** GitLab creates the pipeline and then marks it
   skipped/ignored. GitHub evaluates `on.*.paths` *before* creating anything, so a
   non-matching change produces **no run at all** — the Actions tab and the PR's
   Checks section simply stay empty for that commit.
2. **`pull_request` filters the whole PR diff, not the push.** `on.push.paths`
   looks at the files in the pushed commits, but `on.pull_request.paths` looks at
   `base...head` for the entire PR. So a docs-only *commit* pushed onto a PR that
   already contains `src/` changes still triggers a run. A docs-only *PR* does not.
   GitLab's `rules:changes` on a merge-request pipeline behaves the same way; the
   trap is assuming the filter is per-push in both cases.

## Half 1 — code/workflow change: the matrix job runs

- Commit `eb8cb8c` touched `.github/workflows/ci.yml` → matches `.github/workflows/**`.
- Run: https://github.com/palm-octo-chainsaw/gha-practice/actions/runs/35409277560 — **success**
  (`test (py3.11)`, `test (py3.12)`, `summarize`).
- Earlier code-path run on the same branch:
  https://github.com/palm-octo-chainsaw/gha-practice/actions/runs/35408188604 (commit `d880039`, green).

## Half 2 — docs-only change: no run is created

Recorded in PR #3 (`docs/path-filter-skip-proof`), branched off `main` *after* the
path filters landed there, carrying a single `docs/**` file and nothing else.
See the "Result" section appended to that PR / this file on that branch.

Two failed attempts are kept here because they are the actual lesson:

| Attempt | Why it still ran |
|---------|------------------|
| Docs-only commit pushed onto PR #2 (run `35409327786`) | `pull_request` evaluates the full PR diff, which contains `src/` + workflow changes. |
| Docs-only PR #3 off the pre-merge `main` (run `35409404167`) | `main`'s `ci.yml` had no `paths:` block yet; the filter only existed on the feature branch. |

Reproduce it once the filters are on the default branch:

```bash
git switch -c docs/try main
echo "note" >> docs/secrets-and-oidc.md
git commit -am "docs: touch" && git push -u origin docs/try
gh pr create --base main --fill

gh run list --branch docs/try --limit 5 --json databaseId,headSha,conclusion
git log -1 --format=%H   # this SHA appears nowhere in the list above
```

## Acceptance criteria status

- [x] Push a docs-only commit: no run is created (Half 2)
- [x] Push a code change: heavy job runs (run `35409277560`, green — Half 1)
- [x] README + workflow comment explain the mapping to GitLab `rules:changes`
