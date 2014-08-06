# applyaf

[![Build Status][travis image]][travis link]
[![PyPi Version][pypi ver image]][pypi ver link]
[![Coverage Status][coveralls image]][coveralls link]

applyaf is a Python module that applies frequency dependent antenna
factors and cable losses to spectrum analyzer readings in order to
calculate the incident field. Any duplicate frequency entries in the
antenna factors or cable losses data are removed before interpolating
the frequencies to match those of the spectrum analyzer readings.

## Inputs

Three csv files containing the following are required inputs:

1. Spectrum analyzer measurements
2. Antenna factor data
3. Cable loss data

Each CSV file should contain data in two columns:

1. Frequency
2. Amplitude

The amplitude is expected to be in dB.

## Requirements

- [numpy][]
- `csv` module from the [Python Standard Library][]
- `os` module from the [Python Standard Library][]

## Future Improvements

Some thoughts for future improvements include:

1. Allowing CSV data files that contain non-dB amplitudes and then
convert as needed. Should this be a per-file setting?
2. Generalize the code to handle a variable number (>3) of data to be
interpolated and applied to the given data set.
3. If the code is generalized, should this be wrapped into the
[siganalysis][] project or left on its own?

## Contributing

[applyaf][] is developed using [Scott Chacon][]'s [GitHub Flow][]. To
contribute, fork [applyaf][], create a feature branch, and then submit
a pull request.  [GitHub Flow][] is summarized as:

- Anything in the `master` branch is deployable
- To work on something new, create a descriptively named branch off of
  `master` (e.g., `new-oauth2-scopes`)
- Commit to that branch locally and regularly push your work to the same
  named branch on the server
- When you need feedback or help, or you think the brnach is ready for
  merging, open a [pull request][].
- After someone else has reviewed and signed off on the feature, you can
  merge it into master.
- Once it is merged and pushed to `master`, you can and *should* deploy
  immediately.

# License

[applyaf] is released under the MIT license. Please see the
[LICENSE.txt] file for more information.

[applyaf]: https://github.com/questrail/applyaf
[coveralls image]: https://coveralls.io/repos/questrail/applyaf/badge.png
[coveralls link]: https://coveralls.io/r/questrail/applyaf
[github flow]: http://scottchacon.com/2011/08/31/github-flow.html
[LICENSE.txt]: https://github.com/questrail/applyaf/blob/develop/LICENSE.txt
[numpy]: http://www.numpy.org
[pull request]: https://help.github.com/articles/using-pull-requests
[pypi ver image]: https://badge.fury.io/py/applyaf.png
[pypi ver link]: http://badge.fury.io/py/applyaf
[python standard library]: https://docs.python.org/2/library/
[scott chacon]: http://scottchacon.com/about.html
[siganalysis]: https://github.com/questrail/siganalysis
[travis image]: https://travis-ci.org/questrail/applyaf.png
[travis link]: https://travis-ci.org/questrail/applyaf
