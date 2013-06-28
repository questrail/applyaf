# applyaf

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

* [numpy][]

## Future Improvements

Some thoughts for future improvements include:

1. Allowing CSV data files that contain non-dB amplitudes and then
convert as needed. Should this be a per-file setting?
2. Generalize the code to handle a variable number (>3) of data to be
interpolated and applied to the given data set.
3. If the code is generalized, should this be wrapped into the
[siganalysis] project or left on its own?

## Contributing

[applyaf] is developed using [git-flow], which are "git extensions to
provide high-level repository operations for [Vincent Driessen's
branching model][nvie-git]." To contirbute, [install git-flow], fork
[applyaf], and then run:

```bash
$ git clone git@github.com:<username>/applyaf.git
$ cd applyaf
$ git branch master origin/master
$ git flow init -d
$ git flow feature start <your_feature>
```

When you're done coding and committing the changes for `your_feature`,
issue:

```bash
$ git flow feature publish <your_feature>
```

Then open a pull request to `your_feature` branch.


# License

[applyaf] is released under the MIT license. Please see the
[LICENSE.txt] file for more information.

[applyaf]: https://github.com/questrail/applyaf
[numpy]: http://www.numpy.org
[siganalysis]: https://github.com/questrail/siganalysis
[git workflow]: http://nvie.com/posts/a-successful-git-branching-model/
[LICENSE.txt]: https://github.com/questrail/applyaf/blob/develop/LICENSE.txt
[git-flow]: https://github.com/nvie/gitflow
[nvie-git]: http://nvie.com/posts/a-successful-git-branching-model/
[install git-flow]: https://github.com/nvie/gitflow/wiki/Installation
