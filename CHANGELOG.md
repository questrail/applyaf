# CHANGELOG.md

This file contains all notable changes to the [applyaf][] project.

## Unreleased

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

## v1.1.0 - 2021-12-14

- Updated requirements
- Add newer versions of Python for testing.

## v1.0.1 - 2017-11-16

- Update setup.py

## v1.0.0 - 2017-11-16

- Remove Py2.6/2.7 from Travis-CI.
- Remove if main, since only run as library.

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

[#1]: https://github.com/questrail/applyaf/issues/1
[#2]: https://github.com/questrail/applyaf/issues/2
[applyaf]: https://github.com/questrail/applyaf
