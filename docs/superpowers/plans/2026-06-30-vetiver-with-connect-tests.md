# vetiver-python: adopt with-connect for Connect tests — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace vetiver's bespoke Connect-in-Docker test harness with `posit-dev/with-connect`, so the Connect integration test reads credentials from the environment and the repo no longer carries its own docker-compose/user-bootstrap scripts.

**Architecture:** `with-connect` boots a licensed Connect container, bootstraps a single admin API key, and exports `CONNECT_SERVER` + `CONNECT_API_KEY` to the wrapped command. The test fixture reads those env vars and derives the pin namespace from the authenticated user. CI uses the `with-connect` GitHub Action; local dev uses the `with-connect` CLI via `uvx`.

**Tech Stack:** Python, pytest, pins, rsconnect-python, Docker, `uv`/`uvx`, GitHub Actions.

## Global Constraints

- vetiver supports Python 3.9+; the Connect test job runs on Python 3.9. (`with-connect`'s own 3.13 requirement is satisfied by `uvx`/the Action and does not affect the test interpreter.)
- `with-connect` exposes **only** `CONNECT_SERVER` and `CONNECT_API_KEY` to a wrapped command. Do not rely on any other injected env var, on named users (`susan`/`derek`/`admin`), or on a JSON keys file.
- Never hardcode a Connect username; derive it at runtime via the pins API.
- Pin `with-connect` to commit `0783dabdd24e360e985a4588ce1239c3dc31c542` (no release tags exist yet). Verify this is still the desired ref at execution time with `gh api repos/posit-dev/with-connect/commits/main -q .sha`.
- A valid `rstudio-connect.lic` must be present in the repo root for local runs (gitignored). CI passes the license via the `RSC_LICENSE` secret.
- The Connect test deploys with `extra_files=["requirements.txt"]`, so a `requirements.txt` snapshot of the test env must exist in the working directory before the test runs.

---

### Task 1: Refactor `test_rsconnect.py` to env-var credentials + single user

**Files:**
- Modify: `vetiver/tests/test_rsconnect.py` (full rewrite of fixtures/helpers)

**Interfaces:**
- Consumes: `CONNECT_SERVER`, `CONNECT_API_KEY` from the environment (provided by `with-connect`).
- Produces: a single `rsc_admin` board fixture and a `username` fixture; no JSON-key helpers remain.

- [ ] **Step 1: Replace the module so credentials are read lazily and the user is derived at runtime**

Rationale for lazy reads: pytest imports every test module during collection even for `make test` (which deselects `rsc_test` by marker). Module-level `os.environ["CONNECT_SERVER"]` would raise `KeyError` during that collection. Use `os.environ.get(...)` at module scope and `pytest.skip(...)` inside the fixtures.

Replace the entire contents of `vetiver/tests/test_rsconnect.py` with:

```python
import os

import numpy as np
import pandas as pd
import pytest
import sklearn

import pins
from pins.boards import BoardRsConnect
from pins.rsconnect.api import RsConnectApi
from pins.rsconnect.fs import RsConnectFs
from rsconnect.api import RSConnectClient, RSConnectServer

import vetiver

RSC_SERVER_URL = os.environ.get("CONNECT_SERVER")
RSC_API_KEY = os.environ.get("CONNECT_API_KEY")

pytestmark = pytest.mark.rsc_test  # noqa


def _require_connect():
    if not RSC_SERVER_URL or not RSC_API_KEY:
        pytest.skip("CONNECT_SERVER and CONNECT_API_KEY must be set (run via with-connect)")


def _api():
    return RsConnectApi(RSC_SERVER_URL, RSC_API_KEY)


def rsc_delete_user_content(rsc):
    guid = rsc.get_user()["guid"]
    content = rsc.get_content(owner_guid=guid)
    for entry in content:
        rsc.delete_content_item(entry["guid"])


@pytest.fixture(scope="function")
def username():
    _require_connect()
    return _api().get_user()["username"]


@pytest.fixture(scope="function")
def rsc_admin():
    # tears down content after each test
    _require_connect()
    fs = RsConnectFs(_api())
    rsc_delete_user_content(fs.api)
    yield BoardRsConnect("", fs, allow_pickle_read=True)
    rsc_delete_user_content(fs.api)


def test_deploy(rsc_admin, username):
    np.random.seed(500)

    # Load data, model
    X_df, y = vetiver.mock.get_mock_data()
    model = vetiver.mock.get_mock_model().fit(X_df, y)

    pin_name = f"{username}/model"
    v = vetiver.VetiverModel(model=model, prototype_data=X_df, model_name=pin_name)

    board = pins.board_connect(
        server_url=RSC_SERVER_URL, api_key=RSC_API_KEY, allow_pickle_read=True
    )

    vetiver.vetiver_pin_write(board=board, model=v)
    connect_server = RSConnectServer(url=RSC_SERVER_URL, api_key=RSC_API_KEY)
    assert isinstance(board.pin_read(pin_name), sklearn.dummy.DummyRegressor)

    vetiver.deploy_connect(
        connect_server=connect_server,
        board=board,
        pin_name=pin_name,
        title="testapi",
        extra_files=["requirements.txt"],
    )

    # get url of where content lives
    client = RSConnectClient(connect_server)
    dicts = client.content_search()
    rsc_api = list(filter(lambda x: x["title"] == "testapi", dicts))
    content_url = rsc_api[0].get("content_url")

    h = {"Authorization": f"Key {RSC_API_KEY}"}

    endpoint = vetiver.vetiver_endpoint(content_url + "/predict")
    response = vetiver.predict(endpoint, X_df, headers=h)

    assert isinstance(response, pd.DataFrame), response
    assert response.iloc[0, 0] == 44.47
    assert len(response) == 100
```

- [ ] **Step 2: Verify the normal (non-Connect) test suite still collects and runs**

This confirms the lazy env reads didn't break collection of the module for the default run.

Run: `pytest -m 'not rsc_test and not docker' -q`
Expected: PASS (no `KeyError` during collection; `test_rsconnect.py::test_deploy` is deselected by the marker).

- [ ] **Step 3: Verify the Connect test passes under with-connect**

Requires Docker + `rstudio-connect.lic` in the repo root.

Run:
```bash
pip freeze > requirements.txt
uvx --from git+https://github.com/posit-dev/with-connect@0783dabdd24e360e985a4588ce1239c3dc31c542 \
  with-connect -- pytest vetiver/tests/test_rsconnect.py -m 'rsc_test' -v
```
Expected: PASS — `test_deploy` deploys the model and asserts `response.iloc[0, 0] == 44.47`.

- [ ] **Step 4: Commit**

```bash
git add vetiver/tests/test_rsconnect.py
git commit -m "test: read Connect creds from env, derive pin user at runtime"
```

---

### Task 2: Point `make test-rsc` at with-connect and remove the dev harness targets

**Files:**
- Modify: `Makefile`

**Interfaces:**
- Consumes: nothing new.
- Produces: a `test-rsc` target that no longer depends on `dev`/`dev-start`/`dev-stop` or `RSC_API_KEYS`.

- [ ] **Step 1: Remove the `RSC_API_KEYS` variable**

Delete this line near the top of `Makefile`:

```make
RSC_API_KEYS=vetiver/tests/rsconnect_api_keys.json
```

- [ ] **Step 2: Replace the `test-rsc` target**

Change:

```make
test-rsc: clean-test
	pytest
```

to:

```make
test-rsc: clean-test
	pip freeze > requirements.txt
	uvx --from git+https://github.com/posit-dev/with-connect@0783dabdd24e360e985a4588ce1239c3dc31c542 \
		with-connect -- pytest vetiver -m 'rsc_test'
```

- [ ] **Step 3: Remove the `dev`, `dev-start`, `dev-stop`, and `$(RSC_API_KEYS)` targets**

Delete these blocks from `Makefile`:

```make
dev: vetiver/tests/rsconnect_api_keys.json

dev-start:
	docker compose up -d
	docker compose exec -T rsconnect bash < script/setup-rsconnect/add-users.sh
	# curl fails with error 52 without a short sleep....
	sleep 5
	curl -s --retry 10 --retry-connrefused http://localhost:3939

dev-stop:
	docker compose down
	rm -f $(RSC_API_KEYS)
```

and

```make
$(RSC_API_KEYS): dev-start
	python script/setup-rsconnect/dump_api_keys.py $@
```

- [ ] **Step 4: Update the `help` target text**

Delete these three lines from the `help` recipe:

```make
	@echo "dev - generate Connect API keys"
	@echo "dev-start - start up development Connect in Docker"
	@echo "dev-stop - stop Connect dev container"
```

- [ ] **Step 5: Verify the Makefile is well-formed and `test-rsc` runs**

Run: `make -n test-rsc`
Expected: prints the `pip freeze` + `uvx ... with-connect -- pytest` commands with no `make` errors.

Run (Docker + license present): `make test-rsc`
Expected: PASS (same green result as Task 1, Step 3).

- [ ] **Step 6: Commit**

```bash
git add Makefile
git commit -m "build: run rsc tests via with-connect, drop bespoke dev targets"
```

---

### Task 3: Convert the `test-connect` CI job to the with-connect Action

**Files:**
- Modify: `.github/workflows/tests.yml` (the `test-connect` job)

**Interfaces:**
- Consumes: `secrets.RSC_LICENSE` (license contents).
- Produces: a `test-connect` job that needs no `docker-compose.yml` or `make dev`.

- [ ] **Step 1: Replace the `run Connect` + `Run tests` steps**

In the `test-connect` job, replace these two steps:

```yaml
      - name: run Connect
        run: |
          docker compose up --build -d
          pip freeze > requirements.txt
          make dev
          cat requirements.txt
        env:
          RSC_LICENSE: ${{ secrets.RSC_LICENSE }}
          GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}

      # NOTE: edited to run checks for python package
      - name: Run tests
        run: |
          pytest vetiver -m 'rsc_test'
```

with:

```yaml
      - name: Run Connect integration tests
        uses: posit-dev/with-connect@0783dabdd24e360e985a4588ce1239c3dc31c542
        with:
          license: ${{ secrets.RSC_LICENSE }}
          command: |
            pip freeze > requirements.txt
            pytest vetiver -m 'rsc_test'
```

Note: keep the existing `Install dependencies` step (it still installs `.[dev]` and the vetiver build) so `pip freeze` captures the deployable environment.

- [ ] **Step 2: Lint the workflow YAML**

Run: `python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/tests.yml'))"`
Expected: no output (valid YAML).

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/tests.yml
git commit -m "ci: run Connect tests via with-connect action"
```

---

### Task 4: Convert the weekly workflow jobs

**Files:**
- Modify: `.github/workflows/weekly.yml`

**Interfaces:**
- Consumes: `secrets.RSC_LICENSE`.
- Produces: the two rsconnect jobs run via the Action; the two pins jobs no longer start Connect.

- [ ] **Step 1: Remove Connect setup from the two `*_pins_main` jobs**

`vetiver_main_pins_main` and `vetiver_pypi_pins_main` run `make test` (which is `-m 'not rsc_test and not docker'`), so they do not need Connect. In **both** jobs, delete the `run Connect` step:

```yaml
      - name: run Connect
        run: |
          docker compose up --build -d
          make dev
        env:
          RSC_LICENSE: ${{ secrets.RSC_LICENSE }}
          GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

Leave their final `make test` step intact.

- [ ] **Step 2: Convert the two `*_rsconnect_latest` jobs to the Action**

In `vetiver_pypi_rsconnect_latest` and `vetiver_latest_rsconnect_latest`, replace the `run Connect` + `Run Tests` steps:

```yaml
      - name: run Connect
        run: |
          docker compose up --build -d
          make dev
        env:
          RSC_LICENSE: ${{ secrets.RSC_LICENSE }}
          GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}

      - name: Run Tests
        run: |
          pytest -m 'rsc_test'
```

with:

```yaml
      - name: Run Connect integration tests
        uses: posit-dev/with-connect@0783dabdd24e360e985a4588ce1239c3dc31c542
        with:
          license: ${{ secrets.RSC_LICENSE }}
          command: |
            pip freeze > requirements.txt
            pytest vetiver -m 'rsc_test'
```

These jobs already run `pip freeze > requirements.txt` in their `Install dependencies` step; the line inside `command:` re-snapshots after all installs and is harmless. The rsconnect-from-`main` install steps stay unchanged — these jobs remain the reverse-dependency canary.

- [ ] **Step 3: Add a failure notification to the canary jobs**

Append this step to **both** `*_rsconnect_latest` jobs so rsconnect breakage is surfaced:

```yaml
      - name: Open issue on failure
        if: failure() && github.event_name == 'schedule'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: `Weekly canary failed: ${context.job}`,
              body: `The weekly Connect canary failed on run ${context.runId}. This often means a change in rsconnect-python \`main\` broke vetiver. See https://github.com/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId}`,
              labels: ["ci-failure"]
            })
```

- [ ] **Step 4: Lint the workflow YAML**

Run: `python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/weekly.yml'))"`
Expected: no output (valid YAML).

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/weekly.yml
git commit -m "ci: weekly Connect jobs via with-connect; drop Connect from pins-only jobs"
```

---

### Task 5: Delete the bespoke harness files

**Files:**
- Delete: `docker-compose.yml`
- Delete: `script/setup-rsconnect/dump_api_keys.py`, `add-users.sh`, `users.txt`, `rstudio-connect.gcfg` (the whole `script/setup-rsconnect/` directory)
- Delete: `vetiver/tests/rsconnect_api_keys.json` (if present / untracked)

- [ ] **Step 1: Confirm nothing else references the harness paths**

Run:
```bash
grep -rn "setup-rsconnect\|rsconnect_api_keys\|docker-compose\|docker compose" \
  --include='*.py' --include='*.yml' --include='*.yaml' --include='Makefile' . \
  | grep -v 'docs/superpowers'
```
Expected: no hits outside `docs/superpowers/` (the design/plan docs). If `script/setup-docker/` appears, that is the *Docker* test path (`test-docker` job) and is unrelated — leave it.

- [ ] **Step 2: Delete the files**

Run:
```bash
git rm docker-compose.yml
git rm -r script/setup-rsconnect
rm -f vetiver/tests/rsconnect_api_keys.json
```

- [ ] **Step 3: Verify the default test suite still passes**

Run: `pytest -m 'not rsc_test and not docker' -q`
Expected: PASS.

- [ ] **Step 4: Verify the Connect test still passes end-to-end**

Run: `make test-rsc`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "chore: remove bespoke Connect test harness (replaced by with-connect)"
```

---

## Self-Review notes

- Spec "vetiver-python changes" → Tasks 1–5 cover the fixture, Makefile, `tests.yml`, `weekly.yml`, and all deletions.
- The spec's `requirements.txt` requirement is honored in Task 1 Step 3, Task 2 Step 2, and the `command:` blocks in Tasks 3–4.
- `with-connect` ref is pinned to one SHA used identically in Tasks 1–4 (`0783dabdd24e360e985a4588ce1239c3dc31c542`).
- The lazy-env-read detail (Task 1) prevents a collection-time regression in the default `pytest` run.
