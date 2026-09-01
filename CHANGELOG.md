# CHANGELOG.md

This file contains all notable changes to the [applyaf][] project.

## Unreleased

### Added

- Put the Python dependencies under Dependabot. The actions in `ci.yml`
  and `release.yml` had been pinned to commit SHAs and updated monthly
  since they were pinned, while numpy and the dev tools sat in `uv.lock`
  with nothing moving them at all: `just up-all` was a manual act of
  memory. Dependabot's uv ecosystem reads `pyproject.toml` and `uv.lock`
  together, so an update arrives as a lock file change that CI checks
  with `uv sync --locked`. The dev tools are grouped into one pull
  request; numpy is left out of the group, since it is the one runtime
  dependency and both `requires-python` and the floor job make claims
  about it.

### Changed

- Stop persisting the GitHub credential in the checkouts. `actions/checkout`
  writes the `GITHUB_TOKEN` into `.git/config` by default, where every
  later step, and every action those steps call, can read it. In the
  release job that token carries `contents: write` and sits beside the
  step that mints a PyPI credential. No step in either workflow talks to
  the remote over git: the tag check reads refs the checkout already
  fetched, and `gh release create` authenticates through `GH_TOKEN`.

### Added

- Put the Python dependencies under Dependabot. The actions in `ci.yml`
  and `release.yml` had been pinned to commit SHAs and updated monthly
  since they were pinned, while numpy and the dev tools sat in `uv.lock`
  with nothing moving them at all: `just up-all` was a manual act of
  memory. Dependabot's uv ecosystem reads `pyproject.toml` and `uv.lock`
  together, so an update arrives as a lock file change that CI checks
  with `uv sync --locked`. The dev tools are grouped into one pull
  request; numpy is left out of the group, since it is the one runtime
  dependency and both `requires-python` and the floor job make claims
  about it.

## v3.0.2 - 2026-09-01

### Added

- Create a GitHub release for each tag from the release workflow, with
  the CHANGELOG section for that version as the notes and the built
  distributions as the assets. Ten tags had been pushed without one, so
  the Releases page was empty and the version history was only readable
  from this file. The notes are collected before the upload rather than
  after, so that a CHANGELOG with no section for the version being
  released stops the release while stopping it is still possible.
- Smoke test the built wheel before publishing it. Every other check
  runs against the source tree with `src/` on the path, so a packaging
  mistake that left a module or `py.typed` out of the distribution
  passed ruff, pyright, and the whole suite and shipped anyway. The new
  step installs the wheel where `src/` cannot be reached, imports it
  there, checks the installed version against the tag, resolves every
  name in `__all__`, and confirms `py.typed` came along.
- Test on Python 3.14 in CI and declare it in the classifiers. The code
  and the type checking were already clean on 3.14; what was missing was
  anything that would notice if they stopped being clean, since
  `requires-python = ">=3.12"` had let 3.14 install all along without a
  matrix entry standing behind it.
- Test the dependency floors in CI with a `--resolution lowest-direct`
  job. The matrix installs what `uv.lock` pins, which is the newest numpy
  rather than the oldest that `numpy>=2.2.0` promises to anyone
  installing applyaf alongside something that holds numpy back, so the
  floor was a claim with nothing standing behind it. The job installs
  numpy 2.2.0 and runs the suite against it. It runs on 3.12, since numpy
  ships no cp314 wheels below 2.3.2 and resolving to the floor on 3.14
  would compile numpy from source. Only the suite runs there, because
  lowest-direct pins the dev tools to their floors too and an older ruff
  formats differently.

### Changed

- Give the dependency floor job its own `cache-suffix`. It runs on 3.12,
  as does a leg of the matrix, which put both on the same default cache key
  on the same runner: they raced to save it and every CI run carried a
  "Failed to save: Unable to reserve cache" warning. The two install
  deliberately different numpy versions, so they want separate keys rather
  than one they take turns overwriting.

- Upgrade `astral-sh/setup-uv` from v7.6.0 to v10.0.1, across three major
  releases. v8 dropped the `manifest-file` format this project never used
  and stopped publishing major and minor tags altogether, which is the same
  supply chain reasoning the SHA pins here already follow. v9 changed the
  `prune-cache` default to `false` to ease the load on PyPI; the caches
  that grows are small enough here to take the new default as it comes.
  v10 stops caching by default on the events where a poisoned cache does
  the most damage.
- Stop caching in the release job. `enable-cache` was `true`, which
  overrode the protection v10 added: setup-uv's own `auto` mode declines to
  cache on a tag push, which is exactly what triggers this workflow, and
  this is the job that can mint a PyPI credential. It is set to `false`
  rather than left on `auto` so the answer does not change if that
  heuristic does. Little is lost, since the lint and test steps moved to
  the CI job and nothing in the release syncs the dev environment any more.
  `ci.yml` keeps its cache: those jobs install numpy and the dev tools four
  times over, and none of them can publish anything.

- Pin every GitHub action to a commit SHA rather than a tag, with the
  version it stood for in a comment beside it. A tag is mutable, and the
  release job can mint a PyPI credential, so a moved tag on
  `actions/checkout` or `astral-sh/setup-uv` was a path to the package.
  `ci.yml` is pinned on the same terms: it is not privileged itself, but
  the release now publishes on its verdict, so an action that could turn a
  red run green sits inside the same boundary. The SHAs are the ones the
  tags in use already resolved to, so nothing about the runs changes.
- Add `.github/dependabot.yml` for the actions, without which pinning
  would amount to staying on one commit forever: a fix published upstream
  no longer arrives on its own once the tag stops moving. Minor and patch
  updates are grouped into one monthly pull request; majors are left out
  of the group so they are reviewed on their own.

- Run the wheel smoke test from `scripts/smoke_test_wheel.py`, which both
  `just build` and the release workflow now call. It had lived as a
  heredoc inside `release.yml`, so the README's claim that `just build`
  runs the same checks was not quite true: the local build was the one
  place a packaging mistake could slip through.
- Set `UV_NO_SYNC` for `ci.yml`. Each job installs its environment once,
  in the step that says so, and every `uv run` after it was re-resolving
  and reinstalling the project on top of that. In the floor job that was
  more than wasted time: a re-sync resolves at the default resolution and
  would have undone the `lowest-direct` install the job exists to test.
  The explicit `--no-sync` flags there are gone, since the variable now
  says it once for the whole file.
- Select the `PT` and `RUF` ruff rules. `PT` caught a
  `pytest.raises(ValueError)` with no `match`, which any other `ValueError`
  from that call would have satisfied. `C4`, `RET`, `ARG`, and `TID` were
  tried and found nothing, so they are left out rather than added dormant.
- Require 100% coverage with `fail_under`, which the suite now reaches.
  Two branches had never been exercised: `remove_antenna_factor()` with
  no cable losses, which is a public path a caller can take, and the
  `csv.Error` fallback in `_has_header()` that a single column file
  reaches. Both have tests now. Also set `relative_files`, since Coveralls
  cannot map the absolute paths of a runner's checkout onto the
  repository.
- Track `.python-version` rather than ignoring it, so a contributor's
  `uv sync` builds against the interpreter the release is built on
  instead of whatever uv finds. The CI matrix is unaffected: setup-uv's
  `python-version` input sets `UV_PYTHON`, which takes precedence over the
  file.
- Drop `ruff` from the `brew install` line in the README. It is a dev
  dependency pinned in `uv.lock` and reached through `uv run`, so a brewed
  copy only added a second, unpinned ruff for an editor to find, and
  formatting changes between ruff releases: the editor could reformat code
  that `ruff format --check` then rejected.
- Gate the release on CI. `release.yml` now calls `ci.yml` as a reusable
  workflow and publishes only once the whole 3.12/3.13/3.14 matrix and
  the dependency floor job are green. It had rechecked only what it could
  reach itself, on 3.13 alone, while `git push --follow-tags` started the
  release and CI at the same time, so nothing stopped an upload that went
  out while 3.14 was still running or already red. The lint, format, type
  check, and test steps are gone from `release.yml` as a result, and with
  them the third copy of a block that already lived in the `Justfile` and
  in `ci.yml`. `uv sync --locked` went too: reading the version needs no
  environment, the build makes its own, and the wheel smoke test installs
  into an isolated one.
- Verify that the tagged commit is on `master` before publishing. `just
  release` refuses to cut from anywhere else, but that is a local
  courtesy and the workflow trusted any `v*` tag that reached it; a tag
  is only a pointer, and one placed on a branch or on a commit that never
  landed would have published whatever it pointed at. The check needs
  real history, so the release checkout is no longer shallow.
- Pass `--check-url` to `uv publish`, making the upload resumable. A run
  that uploaded the sdist and then lost the wheel could not be retried:
  the second attempt failed on the file PyPI already had, and a version
  number can never be reused. Files already uploaded are now skipped and
  the rest goes out.
- Give `release.yml` a concurrency group and a 15 minute timeout, so that
  a second push of the same tag queues behind the first rather than
  racing it. A publish is not something to cancel part way through, so
  `cancel-in-progress` is off. The group in `ci.yml` is now the literal
  `ci-` rather than `${{ github.workflow }}-`, which resolves to the
  calling workflow's name when `ci.yml` is reused and would have left the
  called run waiting on a slot the release job was holding.
- Skip the Coveralls report when `ci.yml` runs as part of a release,
  where it would only re-report the coverage that same commit already
  reported when it landed on `master`.

- Upgrade numpy in the lock file from 2.2.0 to 2.5.2. 2.2.0 predates
  Python 3.14 and ships no cp314 wheels, so a 3.14 job would have had to
  compile numpy from source on every run; cp314 wheels start at numpy
  2.3.2. The `numpy>=2.2.0` floor in `pyproject.toml` is unchanged, since
  a resolver installing on 3.14 picks the newest compatible numpy anyway
  and only the lock had pinned the old one.
- Check the release preconditions in `just release` before linting and
  testing rather than after. `release` had depended on `lint` and
  `test`, so a dirty tree, the wrong branch, or an empty Unreleased
  section was only reported once the full suite had run.
- Ask for no more than `contents: read` in `ci.yml`, which had inherited
  the repository default of write while only reading the code it checks.
  `release.yml` asks for the `contents: write` that creating a release
  needs, alongside the `id-token: write` that trusted publishing needs.
- List `369937+matthewrankin@users.noreply.github.com` as the author
  address in `pyproject.toml`, replacing a work address. It is what
  `Author-email` carries in the built metadata and what PyPI shows on the
  project page, so it changes there from the next release onward.

## v3.0.1 - 2026-08-31

### Added

- Restore the `_remove_duplicate_frequencies()` tests, which had been
  commented out, as pytest classes.

### Changed

- Declare the license as a PEP 639 `license = "MIT"` expression with
  `license-files`, replacing the `License :: OSI Approved` classifier
  that PEP 639 deprecates. Built distributions now carry
  `License-Expression: MIT` under metadata version 2.5 and ship
  `LICENSE.txt` in `dist-info/licenses`.
- Configure pytest in `pyproject.toml`, which had none of its own
  despite `just test` and `just cov` driving it. `testpaths` aims
  collection at the suite, and `--strict-markers` and `--strict-config`
  turn a mistyped marker or an unknown config key into a failure rather
  than a silent no-op.
- Type check `tests/` with pyright, which had covered only `src/` while
  ruff checked both.
- Publish to PyPI from a `release.yml` workflow that a `vX.Y.Z` tag
  triggers, authenticating with trusted publishing rather than a
  `UV_PUBLISH_TOKEN` API token, so no long lived credential exists for
  the project. The workflow refuses a tag that disagrees with the
  version in `pyproject.toml`. `just deploy` becomes `just build`, which
  runs the same checks and produces the same distributions locally
  without publishing them.
- Cut releases with `just release`, which lints, tests, shows the
  entries waiting under Unreleased beside the version each bump would
  produce, and asks which to cut, then bumps, closes out the CHANGELOG,
  locks, commits, and tags, leaving only `git push --follow-tags` to
  publish. It refuses a dirty tree, a branch other than `master`, a
  `master` behind its upstream, an empty Unreleased section, and a tag
  that already exists. Cancelling or refusing leaves the version, the
  CHANGELOG, and the tags untouched.

## v3.0.0 - 2026-08-31

### Changed

- **Breaking.** Analyzer frequencies falling outside the range covered by
  the antenna factors or cable losses now raise a `ValueError` naming the
  calibrated span. `np.interp()` had been silently clamping them to the
  nearest calibrated amplitude, substituting a value that was never
  measured. Pass the new `allow_extrapolation=True` to restore the
  previous behaviour.

### Fixed

- `read_csv_file()` returned a 0-d array for a CSV file holding a single
  data row, which raised an `AxisError` once it reached `np.sort()`.
- `read_csv_file()` silently discarded the only row of a headerless
  single row CSV file. `csv.Sniffer` reports a header for such a file
  because it has no other rows to compare against, so a first row that
  parses as numbers is now treated as data.
- `apply_antenna_factor_show_af_cl()` returned the cable losses as
  `np.empty([1, 1])` when no cable losses were given, which is
  uninitialized memory in a shape that doesn't match the antenna
  factors. It now returns zeros, which is also the correct 0 dB of loss.

- Correct the docstrings, which advertised a magnetic field equation the
  code cannot produce, understated the scope of `keep_max`, described
  `remove_antenna_factor()` as if it were the forward operation, and
  misspelled the `cable_losses` argument.

### Added

- `header` argument to `read_csv_file()` to override header detection.
- `py.typed` marker so the inline annotations reach consumers.
- GitHub Actions CI running lint, formatting, pyright, and the tests on
  Python 3.12 and 3.13, with coverage reported to Coveralls.
- `just lint` and `just cov` recipes.

### Changed

- Pin the ruff rule selection in `pyproject.toml` so lint results don't
  drift with the installed ruff, and pin ruff and pyright as development
  dependencies.
- `just deploy` now depends on `just lint`, which only checks, rather
  than on `just fix`, which rewrites files.
- Replace `Optional[X]` with `X | None` and declare the public API with
  `__all__`.

## v2.1.1 - 2024-12-19

- Remove the Travis CI configuration and update the README.
- Add `ruff format` to the Justfile and format the code with it.

## v2.1.0 - 2024-12-18

- Expose `apply_antenna_factor_show_af_cl()` from the package root.

## v2.0.1 - 2024-12-18

- Bump the version to correct the v2.0.0 release.

## v2.0.0 - 2024-12-18

- Rename `_read_csv_file()` to `read_csv_file()` and expose it as part of
  the public API.
- Remove the unused `_is_valid_file()` helper.
- Raise the minimum supported Python from 3.9 to 3.12, and require
  numpy 2.2.0 or newer.
- Move the package under `src/` and switch the tests from unittest to
  pytest.
- Replace the invoke tasks with uv and Just.

## v1.6.6 - 2024-12-05

- Fix the hatch build so the module, rather than a package, is built.

## v1.6.5 - 2024-12-05

- Further fixes to the hatch deployment.

## v1.6.3 - 2024-12-05

- Fix the deployment with hatch.

## v1.6.2 - 2024-12-05

- Fix the deployment.

## v1.6.1 - 2024-12-05

- Release to correct the v1.6.0 deployment.

## v1.6.0 - 2024-12-05

- Raise the minimum supported Python to 3.9.
- Refactor `tasks.py` and remove a superfluous executable file
  attribute.

## v1.5.2 - 2024-12-04

- Release to correct the v1.5.1 deployment.

## v1.5.1 - 2024-12-04

- Release to correct the v1.5.0 build.

## v1.5.0 - 2024-12-04

- Build with hatchling.
- Raise the minimum supported Python to 3.8 and update the tested
  versions.
- Bump tqdm from 4.64.0 to 4.66.3.
- Remove superfluous executable permissions.

## v1.4.0 - 2023-11-03

- Change suppoted Python to 3.6–3.10.
- Add mypy to lint.
- Add type hints to function definitions.
- Return emptry array if cable loss is not provided.

## v1.3.1 - 2022-04-21

- Fixed error in apply antenna factors frequency.

## v1.3.0 - 2022-04-21

- Add function to apply the antenna factors and cable losses and return the
  antenna factors at the analyzer frequencies and the cable losses at the
  analyzer frequencies in addition to the returning the incident field.

## v1.2.2 - 2021-12-21

- Fix package directory structure.

## v1.2.1 - 2021-12-21

- Fix the directory structure for the module.

## v1.2.0 - 2021-12-21

- Fix the project directory structure and update the location of
  `setup.py`.
- Restore the version in `__init__.py`.
- Use build to deploy.

## v1.1.0 - 2021-12-14

- Updated requirements
- Add newer versions of Python for testing.

## v1.0.1 - 2017-11-16

- Update setup.py

## v1.0.0 - 2017-11-16

- Remove Py2.6/2.7 from Travis-CI.
- Remove if main, since only run as library.

## v0.4.2 - 2017-07-25

- Remove the unicode literal import.

## v0.4.1 - 2017-07-25

- Bump the revision.

## v0.4.0 - 2017-03-24

### Added

- Ability to remove antenna factors and cable losses

## v0.3.0 - 2015-08-20

### Changed

- Migrated Travis-CI from legacy to container-based
  infrastructure
- Added coverage to requirements.txt and updated `inv test` task to
  run coverage as well.

## v0.2.3 - 2015-08-20

### Changed

- Updated pip requirements including numpy from 1.8.1 to 1.9.2

## v0.2.2 - 2014-08-08

### Changed

- Moved AUTHORS.txt to AUTHORS.md
- Moved CHANGES.md to CHANGELOG.md
- Switched badges to shields.io
- Updated README.md

## v0.2.1 - 2014-08-07

### Added

- Create release script [#2][]

## v0.2 - 2014-08-07

- Initial release, reading the CSV files and removing duplicate
  frequency entries.

[#1]: https://github.com/questrail/applyaf/issues/1
[#2]: https://github.com/questrail/applyaf/issues/2
[applyaf]: https://github.com/questrail/applyaf
