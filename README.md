# applyaf

[![PyPi Version][pypi ver image]][pypi ver link]
[![Build Status][travis image]][travis link]
[![Coverage Status][coveralls image]][coveralls link]
[![License Badge][license image]][LICENSE.txt]

[applyaf][] is a Python 3.9+ module that applies frequency dependent
antenna factors and cable losses to spectrum analyzer readings in order
to calculate the incident field. Any duplicate frequency entries in the
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

### Development Setup Using pyenv

Use the following commands to create a virtualenv using [pyenv][] and
[pyenv-virtualenv][], install the requirements in the virtualenv named
`applyaf`, and list the available [Invoke][] tasks.

```bash
$ pyenv install 3.13
$ pyenv virtualenv 3.13 applyaf
$ pyenv activate applyaf
$ pip install -r requirements.txt
$ inv -l
```

## License

[applyaf][] is released under the MIT license. Please see the
[LICENSE.txt][] file for more information.

[applyaf]: https://github.com/questrail/applyaf
[coveralls image]: http://img.shields.io/coveralls/questrail/applyaf/master.svg
[coveralls link]: https://coveralls.io/r/questrail/applyaf
[invoke]: https://www.pyinvoke.org/
[LICENSE.txt]: https://github.com/questrail/applyaf/blob/develop/LICENSE.txt
[license image]: http://img.shields.io/pypi/l/applyaf.svg
[numpy]: http://www.numpy.org
[pull request]: https://help.github.com/articles/using-pull-requests
[pyenv]: https://github.com/pyenv/pyenv
[pyenv-virtualenv]: https://github.com/pyenv/pyenv-virtualenv
[pypi ver image]: http://img.shields.io/pypi/v/applyaf.svg
[pypi ver link]: https://pypi.python.org/pypi/applyaf
[siganalysis]: https://github.com/questrail/siganalysis
[travis image]: http://img.shields.io/travis/questrail/applyaf/master.svg
[travis link]: https://travis-ci.org/questrail/applyaf
