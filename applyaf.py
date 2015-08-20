#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 The applyaf developers. All rights reserved.
# Project site: https://github.com/questrail/applyaf
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Apply the antenna factor and cable loss to freq dependent data.

Apply the antenna factor and cable loss data to spectrum analyzer
measurements or other data. The antenna factor and cable loss arrays will
be interpolated onto the same frequencies as found in the given analyzer
data.
"""

# Try to future proof code so that it's Python 3.x ready
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

# Standard module imports
import csv
import os.path

# Data analysis related imports
import numpy as np

__version__ = '0.3.0'


def _is_valid_file(parser, arg):
    """Determine if the argument is an existing file
    """
    if not os.path.isfile(arg):
        parser.error("The file {} does not exist!".format(arg))
    else:
        # File exists so return the filename
        return arg


def _read_csv_file(filename, freq_unit_multiplier):
    """Read csv file into a numpy array
    """
    # FIXME: Test a file with blank lines in the CSV file.
    with open(filename) as f:
        # Determine if the CSV file has a header row
        has_header = csv.Sniffer().has_header(f.read(1024))
        # print('Header') if has_header else print('No header')
        rows_to_skip = 1 if has_header else 0
        # Go back to the file's beginning and read it into np.array
        f.seek(0)
        array_to_return = np.loadtxt(
            f,
            dtype={'names': ('frequency', 'amplitude_db'),
                   'formats': ('f8', 'f8')},
            delimiter=',',
            skiprows=rows_to_skip)
        array_to_return['frequency'] *= freq_unit_multiplier
        return array_to_return


def _remove_duplicate_frequencies(unsorted_array, keep_max=True):
    """Remove duplicates and sort by frequency

    Given a structured numpy array with 'frequency' and 'amplitude_db' fields,
    sort that array first by frequency and then by amplitude. Depending on
    whether the user wants to keep the max or min value, return the sorted
    array containing no duplicate frequency entries.
    Remove the duplicate frequencies.

    Args:
        unsorted_array: A 1D numpy structured array with fields 'frequency' and
            'amplitude_db'.
        keep_max: A boolean determing if the max or min amplitude values will
            be kept when duplicate frequencies are found.

    Returns:
        A sorted 1D numpy structured array with fields 'frequency' and
        'amplitude_db' with no duplicate frequencies.
    """

    # Sort the data based on the frequency and then the amplitude
    sorted_array = np.sort(unsorted_array, order=['frequency', 'amplitude_db'])
    if keep_max:
        # Reverse the sort order, so that we end up keeping the max value
        sorted_array = sorted_array[::-1]

    # Determine the unique indices and only return those
    unique_indices = np.unique(sorted_array['frequency'], return_index=True)[1]
    return sorted_array[unique_indices]


def apply_antenna_factor(analyzer_readings, antenna_factors,
                         cable_losses=False, keep_max=True):
    """Apply the antenna factor and cable losses to the input data.

    Applies the frequency dependent antenna factor and, optionally, the cable
    losses to a given input data (typically spectrum analyzer readings). Before
    interpolating the frequencies of the antenna factors and cable losses onto
    the dataset, any duplicate frequency entries are removed and either the
    minimum or maximum amplitude value is kept depending on the user's
    selection.

    This is used to calculate the incident field which is defined as:

        E(dBuV/m) = AF(dB) + Vsa(dBuV) + cable_loss(dB)

    as given by Eqn 7.62 in *Introduction to Electromagnetic Compatibility* 2nd
    edition by Clayton Paul.

    Args:
        analyzer_readings: A 1D numpy structured array containing the fields
            'frequency' and 'amplitude_db'.
        antenna_factors: A 1D numpy structured array containing the fields
            'frequency' and 'amplitude_db'.
        cables_losses: A 1D numpy structured array containing the fields
            'frequency' and 'amplitude_db'.
        keep_max: A boolean determining whether the max or min amplitudes are
            kept whenever duplicate frequency entries are found in the
            antenna_factors or cable_losses arrays.

    Returns:
        A 1D numpy structured array containing the incident field.
    """

    # Remove duplicates and keep the max or min
    analyzer_readings_no_duplicates = _remove_duplicate_frequencies(
        analyzer_readings, keep_max)
    antenna_factors_no_duplicates = _remove_duplicate_frequencies(
        antenna_factors, keep_max)

    # Interpolate the antenna factors so that they align
    # with the frequencies found in the spectrum analyzer readings
    antenna_factors_at_analyzer_frequencies = np.interp(
        analyzer_readings_no_duplicates['frequency'],
        antenna_factors_no_duplicates['frequency'],
        antenna_factors_no_duplicates['amplitude_db'])

    if isinstance(cable_losses, np.ndarray):
        # If a numpy.array was provided for the cables_losses then
        # remove the duplicates and interpolate so that its frequencies
        # align with the spectrum analyzer readings
        cable_losses_no_duplicates = _remove_duplicate_frequencies(
            cable_losses, keep_max)
        cable_losses_at_analyzer_frequencies = np.interp(
            analyzer_readings_no_duplicates['frequency'],
            cable_losses_no_duplicates['frequency'],
            cable_losses_no_duplicates['amplitude_db'])
        incident_field = analyzer_readings_no_duplicates
        incident_field['amplitude_db'] += \
            antenna_factors_at_analyzer_frequencies
        incident_field['amplitude_db'] += \
            cable_losses_at_analyzer_frequencies
    else:
        # There were no cable losses provided, so just apply the
        # antenna factors.
        incident_field = analyzer_readings_no_duplicates
        incident_field['amplitude_db'] += \
            antenna_factors_at_analyzer_frequencies

    return incident_field

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Apply antenna factor')
    parser.add_argument(
        '-s', dest='spectrumanalyzer', required=True,
        help="CSV file containing spectrum analyzer reading.",
        metavar='FILE', type=lambda x: _is_valid_file(parser, x))
    parser.add_argument(
        '-a', dest='antennafactor', required=True,
        help="CSV file containing antenna factor data.",
        metavar='FILE', type=lambda x: _is_valid_file(parser, x))
    parser.add_argument(
        '-c', '--cableloss', dest='cableloss', required=False,
        help="CSV file containing cable loss data.",
        metavar='FILE', type=lambda x: _is_valid_file(parser, x))
    args = parser.parse_args()

    # Open the CSV files and read the data into np.array
    analyzer_readings = _read_csv_file(args.spectrumanalyzer, 1.0e0)
    antenna_factors = _read_csv_file(args.antennafactor, 1.0e6)

    # Print some info about the arrays
    print(
        'Spectrum analyzer data contains {num_points} points'
        ' from {fstart:1.3e} Hz to {fstop:1.3e} Hz'.format(
            num_points=analyzer_readings.shape[1],
            fstart=analyzer_readings[0, 0],
            fstop=analyzer_readings[0, -1]))
    print(
        'Antenna factor data contains {num_points} points'
        ' from {fstart:1.3e} Hz to {fstop:1.3e} Hz'.format(
            num_points=antenna_factors.shape[1],
            fstart=antenna_factors[0, 0],
            fstop=antenna_factors[0, -1]))

    # Determine if cable loss data was provided
    if args.cableloss:
        cable_losses = _read_csv_file(args.cableloss, 1e6)
        print(
            'Cable loss data contains {num_points} points'
            ' from {fstart:1.3e} Hz to {fstop:1.3e} Hz'.format(
                num_points=cable_losses.shape[1],
                fstart=cable_losses[0, 0],
                fstop=cable_losses[0, -1]))

        # Apply the antenna factor and cable loss to the spectrum analyzer
        # readings
        incident_field = apply_antenna_factor(
            analyzer_readings, antenna_factors, cable_losses)
    else:
        incident_field = apply_antenna_factor(
            analyzer_readings, antenna_factors)
