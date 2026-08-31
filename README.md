# applyaf

[![PyPI Version][pypi ver image]][pypi ver link]
[![Python Versions][pyversions image]][pypi ver link]
[![CI Status][ci image]][ci link]
[![Coverage Status][coveralls image]][coveralls link]
[![License Badge][license image]][LICENSE.txt]

[applyaf][] is a Python 3.12+ module that applies frequency dependent antenna
factors and cable losses to spectrum analyzer readings in order to calculate the
incident field. Any duplicate frequency entries in the antenna factors or cable
losses data are removed before interpolating the frequencies to match those of
the spectrum analyzer readings.

## Inputs

Three csv files containing the following are required inputs:

1. Spectrum analyzer measurements
2. Antenna factor data
3. Cable loss data

Each CSV file should contain data in two columns:

1. Frequency
2. Amplitude

The amplitude is expected to be in dB.

## Dependencies

See the `pyproject.toml` and `uv.lock` files for the dependency requirements.

## Future Improvements

Some thoughts for future improvements include:

1. Allowing CSV data files that contain non-dB amplitudes and then
   convert as needed. Should this be a per-file setting?
2. Generalize the code to handle a variable number (>3) of data to be
   interpolated and applied to the given data set.
3. If the code is generalized, should this be wrapped into the
   [siganalysis][] project or left on its own?

## Contributing

Contributions are welcome! To contribute please:

1. Fork the repository
2. Create a feature branch
3. Add code and tests
4. Pass lint and tests
5. Submit a [pull request][]

## Development Setup

### Development Setup Using uv

#### Development Setup on macOS

```bash
$ brew install uv ruff just
```

With [uv][], [ruff][] and [Just][] installed, development has been simplified to
simply running [Just][] to see the available commands.

```bash
$ just
```

#### Releasing to PyPI

Pushing a `vX.Y.Z` tag runs the [release workflow][], which rechecks the tag
against the version in `pyproject.toml`, lints, type checks, tests, builds, and
publishes. There is no PyPI API token anywhere: the workflow authenticates with
[trusted publishing][], which mints a short lived credential from the GitHub
OIDC identity of that run.

`just build` runs the same checks and produces the same distributions locally,
so the artifacts can be inspected before the tag goes out. It refuses to run
against a dirty working tree, which means the version bump and the CHANGELOG
have to be committed first.

```bash
$ uv version --bump minor        # or major / patch
$ # in CHANGELOG.md, insert a "## vX.Y.Z - YYYY-MM-DD" heading directly
$ # below "## Unreleased" so the accumulated entries sit under the new version
$ uv lock
$ git commit -am "Release vX.Y.Z"
$ just build                     # optional: verify what CI will publish
$ git tag -a vX.Y.Z -m "vX.Y.Z"
$ git push --follow-tags         # this is the release
```

The tag is what publishes, so it is the point of no return: PyPI never lets a
version number be reused. Everything before the push can be amended freely.

This depends on one piece of configuration that lives outside the repository. A
[trusted publisher][trusted publishing] has to be registered for `applyaf` on
PyPI, pointing at the `questrail/applyaf` repository, the `release.yml`
workflow, and the `pypi` environment. It is a one time setup per project.

## License

[applyaf][] is released under the MIT license. Please see the
[LICENSE.txt][] file for more information.

[applyaf]: https://github.com/questrail/applyaf
[ci image]: https://github.com/questrail/applyaf/actions/workflows/ci.yml/badge.svg?branch=master
[ci link]: https://github.com/questrail/applyaf/actions/workflows/ci.yml
[coveralls image]: https://coveralls.io/repos/github/questrail/applyaf/badge.svg?branch=master
[coveralls link]: https://coveralls.io/github/questrail/applyaf?branch=master
[just]: https://just.systems/
[LICENSE.txt]: https://github.com/questrail/applyaf/blob/master/LICENSE.txt
[license image]: https://img.shields.io/pypi/l/applyaf.svg
[pull request]: https://help.github.com/articles/using-pull-requests
[pypi ver image]: https://img.shields.io/pypi/v/applyaf.svg
[pypi ver link]: https://pypi.python.org/pypi/applyaf
[pyversions image]: https://img.shields.io/pypi/pyversions/applyaf.svg
[release workflow]: https://github.com/questrail/applyaf/blob/master/.github/workflows/release.yml
[ruff]: https://docs.astral.sh/ruff/
[siganalysis]: https://github.com/questrail/siganalysis
[trusted publishing]: https://docs.pypi.org/trusted-publishers/
[uv]: https://docs.astral.sh/uv/
