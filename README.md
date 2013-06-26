# applyaf

applyaf is a Python module that applies frequency dependent antenna
 factors and cable losses to spectrum analyzer readings. The antenna
factors and cable losses are interpolated onto the spectrum analyzer
readings.

# Inputs

Three csv files containing the following are required inputs:

1. Spectrum analyzer measurements
2. Antenna factor data
3. Cable loss data

Each CSV file should contain data in two columns:

1. Frequency
2. Amplitude

The amplitude is expected to be in dB.
 
# Requirements

* [numpy][]

# Future Improvements

Some thoughts for future improvements include:

1. Allowing CSV data files that contain non-dB amplitudes and then
convert as needed. Should this be a per-file setting?
2. Generalize the code to handle a variable number (>3) of data to be
interpolated and applied to the given data set.
3. If the code is generalized, should this be wrapped into the
[siganalysis] project or left on its own?

# Contributing

applyaf is developed using the [git workflow], so feel free to fork,
branch, and contribute.

# License

applyaf is released under the MIT license. Please see the `LICENSE.txt`
file for more information.

[numpy]: http://www.numpy.org
[siganalysis]: https://github.com/questrail/siganalysis
[git workflow]: http://nvie.com/posts/a-successful-git-branching-model/
