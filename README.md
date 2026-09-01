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

`just release` cuts the release. It first checks that a release is possible at
all, then lints, type checks, and tests, then shows the entries waiting under
Unreleased and the version each kind of bump would produce, and asks which to
cut. Once answered it bumps the version, closes out the CHANGELOG, updates the
lock file, commits, and tags. Pushing the tag is what publishes.

```bash
$ just release

Releasing from 3.0.1, with these entries under Unreleased:

    ### Fixed

    - `read_csv_file()` returned a 0-d array for a single row file.

    1) patch   3.0.1 -> 3.0.2
    2) minor   3.0.1 -> 3.1.0
    3) major   3.0.1 -> 4.0.0
    q) cancel

Which release? [1] 2

Tagged v3.1.0. Publish it with:

    git push --follow-tags
```

The entries decide the bump, so the prompt puts them next to the versions they
would produce rather than leaving the choice to memory. Answering `q`, or
anything unrecognized, changes nothing.

The tag push runs the [release workflow][], which rechecks the tag against the
version in `pyproject.toml`, repeats the checks, and builds. Every check to that
point runs against the source tree, so the workflow then installs the wheel it
just built somewhere `src/` is not on the path and imports it there, which is
the only step that can catch a packaging mistake that left something out of the
distribution. It uploads once that passes. There is no PyPI API token anywhere:
the workflow authenticates with [trusted publishing][], which mints a short
lived credential from the GitHub OIDC identity of that run.

Uploading is followed by a [GitHub release][releases] for the tag, carrying the
CHANGELOG section for that version as its notes and the built distributions as
its assets. The notes are collected before the upload rather than after, so that
a CHANGELOG with no section for the version being released stops the release
while stopping it is still possible.

Pushing the tag is the point of no return, since PyPI never lets a version
number be reused. Everything `just release` does is local and amendable until
then, and it refuses to start against a dirty working tree, off `master`, on a
`master` behind its upstream, with a CHANGELOG whose Unreleased section is
empty, or when the tag it would create already exists. Those refusals come
before the lint and test run, so a release that cannot happen is turned away at
once rather than after the suite. A refusal leaves the version and the CHANGELOG
untouched.

`just build` runs the same checks and produces the same distributions without
releasing anything, which is the way to inspect what CI would upload.

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
[releases]: https://github.com/questrail/applyaf/releases
[ruff]: https://docs.astral.sh/ruff/
[siganalysis]: https://github.com/questrail/siganalysis
[trusted publishing]: https://docs.pypi.org/trusted-publishers/
[uv]: https://docs.astral.sh/uv/
