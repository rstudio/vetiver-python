# Simplifying the vetiver ↔ Connect integration-testing relationship

**Date:** 2026-06-30
**Status:** Approved design, pending implementation plan
**Repos affected:** `vetiver-python`, `rsconnect-python`

## Problem

The integration-testing relationship between `vetiver-python` and
`rsconnect-python` is both inverted and duplicated:

- The real dependency is one-way: `vetiver-python` declares
  `rsconnect-python>=1.11.0` as a production dependency and calls
  `rsconnect.actions.deploy_python_fastapi` / `rsconnect.api.RSConnectServer` /
  `RSConnectClient` directly.
- Despite not depending on vetiver, `rsconnect-python` carries vetiver-specific
  test baggage: a `vetiver-testing/` harness, `tests/test_vetiver_pins.py`, a
  `--vetiver` pytest marker, and a nightly `test-dev-connect` CI job that installs
  vetiver and deploys a model.
- Both repos independently maintain a near-identical bespoke Connect-in-Docker
  harness (`docker-compose.yml`, `setup-rsconnect/` with `dump_api_keys.py`,
  `add-users.sh`, `users.txt`, `rstudio-connect.gcfg`).

## Goal

vetiver owns and runs all vetiver↔Connect integration tests in its own repo;
`rsconnect-python` carries no vetiver-specific test code. Both repos use
[`with-connect`](https://github.com/posit-dev/with-connect) — the preferred
shared tool for running Connect in Docker during tests — instead of a hand-rolled
harness.

## Target architecture

```
rsconnect-python                          vetiver-python
  ├ tests/test_main_system_caches.py        ├ vetiver/tests/test_rsconnect.py
  │   (own integration test; kept)          │   (reads env creds, single admin user)
  ├ CI: own with-connect job;               ├ CI: posit-dev/with-connect Action (pinned)
  │   creates publisher user via admin API  ├ local: `make test-rsc` → uvx with-connect
  └ actions.py compatibility shim           └ deletes docker-compose.yml,
      (deploy_python_fastapi for vetiver)       script/setup-rsconnect/, dump_api_keys.py

Deleted from rsconnect-python: vetiver-testing/, tests/test_vetiver_pins.py,
the --vetiver marker, the nightly test-dev-connect job, root docker-compose.yml,
and the dev/dev-stop Justfile recipes.
```

The reverse-dependency canary ("does new rsconnect break vetiver?") lives in
vetiver's weekly CI matrix, which already installs `rsconnect` from `main` and
runs the integration tests. rsconnect PRs do not get that signal directly; a
failure notification on the weekly canary is recommended so rsconnect maintainers
learn of breakage without watching the schedule.

### `with-connect` behavior the design relies on

Verified against `posit-dev/with-connect@main`:

- Exports exactly two env vars to the wrapped command: `CONNECT_SERVER` and
  `CONNECT_API_KEY`.
- Bootstraps a single admin-privileged API key via JWT; it does **not** create
  named PAM users. The bootstrapped username is assigned by Connect — derive it
  at runtime, never hardcode it.
- CLI `--license` takes a file path (default `./rstudio-connect.lic`). The
  Action's `license` input takes license *contents* and writes the file itself.
- Does nothing with `requirements.txt` / manifests.
- Default `version` is `release`; supports `--config`/`config-file`, `-e`/`env`,
  `--port`.
- Tool runtime needs Python 3.13 / `uv`, satisfied via `uvx` or the Action. This
  is independent of the test matrix: the wrapped `pytest` runs in the CI job's
  own Python (3.9/3.10), so there is no Python-version regression.

## vetiver-python changes

### Test fixture — `vetiver/tests/test_rsconnect.py`

- Read `CONNECT_SERVER` and `CONNECT_API_KEY` from `os.environ` instead of the
  hardcoded `http://localhost:3939` and the `rsconnect_api_keys.json` file.
- Use the single `with-connect` admin key. Remove `get_key`, `rsc_from_key`,
  `rsc_fs_from_key`, and the JSON helpers; the `rsc_short` fixture builds its
  `BoardRsConnect` from the one env-provided key. The current test already uses
  only one user (`susan`), so a single user covers everything it verifies.
- Do not hardcode a username. Derive it at runtime via
  `rsc.get_user()["username"]` and build the pin name as `f"{username}/model"`;
  update the corresponding `pin_read`, `deploy_connect(pin_name=...)`, and
  `content_search` title lookup.
- The `Authorization: Key ...` header and prediction assertions
  (`response.iloc[0, 0] == 44.47`, `len(response) == 100`) are unchanged.

### Local dev — `Makefile`

- Remove `dev-start`, `dev`, the `RSC_API_KEYS` variable, and the `dump_api_keys`
  invocation.
- `make test-rsc` runs the `with-connect` CLI, e.g.
  `uvx --from git+https://github.com/posit-dev/with-connect@<pinned-ref> with-connect -- pytest vetiver -m 'rsc_test'`.
  License resolves from `./rstudio-connect.lic` per the CLI default.
- `make test` (the `not rsc_test and not docker` run) is unchanged.

### CI — `.github/workflows/tests.yml` and `weekly.yml`

- In each Connect job, replace the `docker compose up --build -d` + `make dev`
  block with the Action, pinned to a release tag or commit SHA:

  ```yaml
  - uses: posit-dev/with-connect@<pinned-tag-or-sha>
    with:
      version: <connect-version>          # release, or a pinned version in the weekly matrix
      license: ${{ secrets.RSC_LICENSE }} # existing secret = license CONTENTS
      command: |
        pip freeze > requirements.txt
        pytest vetiver -m 'rsc_test'
  ```

  The `pip freeze > requirements.txt` step stays because the test deploys with
  `extra_files=["requirements.txt"]` so Connect can rebuild the model env; this is
  unrelated to `with-connect`.
- The weekly matrix keeps its version combinations: vetiver `pypi` × rsconnect
  `main`, and vetiver `main` × rsconnect `main`. Only the harness invocation
  changes; the rsconnect-version install steps stay. These jobs are the canary.
- Add a failure notification (issue/Slack) on the weekly canary.

### Deletions

- `docker-compose.yml`
- `script/setup-rsconnect/` (`dump_api_keys.py`, `add-users.sh`, `users.txt`,
  `rstudio-connect.gcfg`)
- `vetiver/tests/rsconnect_api_keys.json`

## rsconnect-python changes

### Keep and re-home `tests/test_main_system_caches.py`

This is rsconnect's own integration test for the `system caches` CLI, unrelated
to vetiver, that currently freeloads on the vetiver harness (it reads
`vetiver-testing/rsconnect_api_keys.json` and runs inside the `test-dev-connect`
job). It must survive the harness removal:

- It needs two privilege levels — an admin (can list/delete caches) and a
  non-admin publisher (must be denied) — so it cannot use only the `with-connect`
  admin key.
- Refactor it to read `CONNECT_SERVER`/`CONNECT_API_KEY` from env, and add a
  fixture that uses the admin key to create a publisher user via the Connect API
  and mint that user's key at runtime (replacing static `get_key("susan")`).
- Give rsconnect its own `with-connect`-based CI job (Action, pinned) that runs
  `pytest tests/test_main_system_caches.py`. Confirm during implementation that
  the cache add/remove host commands (`ADD_CACHE_COMMAND`/`RM_CACHE_COMMAND`) can
  still target the `with-connect`-managed container.

### Relabel the `actions.py` compatibility shim

`actions.py` lines 281–442 (`validate_extra_files`, `validate_entry_point`,
`deploy_app`) are kept and reframed as a supported compatibility entry point used
by vetiver:

- `deploy_python_fastapi` (line 446, called by vetiver's `deploy_connect`) does
  `return deploy_app(...)`, and `deploy_app` calls the two `validate_*` functions
  — all within this block. `deploy_app` has no other caller. These functions are
  load-bearing for vetiver and have no `DeprecationWarning` or changelog notice,
  so they are treated as a maintained shim, not dead code.
- Rewrite the block-marker comments (lines 281–285, 441–443) to describe this as
  a supported compatibility entry point for `vetiver-python`, dropping the
  "deprecated … will be removed in the future" language.
- Optional cleanup: have `deploy_app` call the `bundle.py` `validate_*` functions
  instead of the local copies, so vetiver deploys stop emitting spurious "This
  method has been moved and will be deprecated" warnings on every call.

The identically-named `validate_extra_files` / `validate_entry_point` in
`bundle.py` (lines ~1774, ~1845) are the active versions used by the `main.py`
CLI and must not be altered. The `actions.py` copies are reachable only through
`deploy_app`.

### Deletions

- `vetiver-testing/` (entire directory).
- `tests/test_vetiver_pins.py`.
- `conftest.py`: the `--vetiver` option and `pytest.mark.vetiver` skip logic.
- `pyproject.toml`: the `vetiver` marker definition and the `vetiver-testing/`
  ruff exclude.
- `.github/workflows/main.yml`: the `test-dev-connect` job (replaced by the
  rsconnect-own `system caches` job above, which no longer installs vetiver).
- Root `docker-compose.yml` and the `dev` / `dev-stop` recipes in `Justfile`
  (lines ~62–71). Their only consumers are the vetiver dev/test path and the
  `test-dev-connect` job. The separate `integration-testing/docker-compose.yml`
  is unrelated and stays.

## Sequencing

The two repos' changes are independent and may land in either order; vetiver
keeps working against rsconnect `main` throughout. Suggested intra-repo order for
rsconnect to keep CI green at every commit:

1. Update `conftest.py` to drop the `--vetiver` option/marker logic.
2. Refactor and re-home `test_main_system_caches.py` onto the new `with-connect`
   job (create publisher user via admin API; env-var creds).
3. Delete `tests/test_vetiver_pins.py`.
4. Update `pyproject.toml` (drop `vetiver` marker + ruff exclude).
5. Replace the `test-dev-connect` job in `main.yml`.
6. Delete the `dev`/`dev-stop` Justfile recipes and root `docker-compose.yml`.
7. Delete `vetiver-testing/`.
8. Relabel the `actions.py` shim comments.

## Verification items

- Confirm `with-connect`'s default Connect image/config enables Python content
  execution (vetiver's test deploys a FastAPI app). If not, enable via the
  Action's `config-file` or `-e`.
- Confirm the bootstrapped admin user can write pins to its own namespace and that
  `rsc.get_user()["username"]` returns the expected value.
- Confirm creating a non-admin publisher user via the Connect API with the
  bootstrap admin key works, for `test_main_system_caches.py`.
- Confirm the `system caches` host commands can still add/remove caches in the
  `with-connect`-managed container.
- Pin a specific `with-connect` Action ref (tag or SHA) and CLI ref; record an
  update strategy.

## Risks / accepted tradeoffs

- rsconnect PRs lose direct vetiver-breakage signal; it moves to vetiver's weekly
  CI, with a failure notification to compensate.
- New external dependency on `posit-dev/with-connect`, mitigated by pinning to a
  tag/SHA. Both repos rely on Docker either way.
- vetiver remains coupled to rsconnect's internal `deploy_python_fastapi` shim.
  Removing that coupling is out of scope and would require a real deprecation
  cycle plus migrating vetiver to the `rsconnect` CLI.
