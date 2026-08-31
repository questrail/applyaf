# CHANGELOG.md

This file contains all notable changes to the [applyaf][] project.

## Unreleased

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
