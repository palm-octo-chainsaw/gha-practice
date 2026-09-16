# Secrets & OIDC patterns (notes lab)

No real credentials live in this repo. Fill the gaps below as you study.

## GitLab → Actions map

| GitLab | Actions |
|--------|---------|
| CI/CD Variables (masked/protected) | Repository / Environment / Organization secrets |
| `CI_JOB_TOKEN` / project access tokens | `GITHUB_TOKEN` (scoped) or a PAT in secrets |
| OIDC to cloud (e.g. GCP WIF) | `permissions: id-token: write` + cloud OIDC role |

## Dry-run staging job (intentional gap)

Challenge: add a job `deploy-staging-dry-run` that:
1. `needs: [test]` (or your reusable setup)
2. Uses `environment: staging` (create it in the UI; no real deploy)
3. Prints what *would* deploy (echo image tag / commit SHA)
4. Never calls a real cloud API

Optional stretch: sketch (do not implement live) an OIDC trust to GCP/AWS in comments:
- which `permissions` block
- which secret names you would *not* need anymore
- how that compares to a long-lived service-account key in GitLab variables

## Done when

- [ ] Dry-run job appears in Actions and only runs after tests
- [ ] Environment `staging` exists (even with no reviewers)
- [ ] This doc has your OIDC sketch filled in
