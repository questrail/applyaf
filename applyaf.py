#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
applyaf.py

Apply the antenna factor and cable loss data to spectrum
analyzer measurements.

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
import pandas as pd

def _is_valid_file(parser, arg):
    '''
    Determine if the argument is an existing file
    '''
    if not os.path.isfile(arg):
        parser.error("The file %s does not exist!"%arg)
    else:
        # File exists so return the filename
        return arg

def _read_csv_file(filename, freq_unit_multiplier):
    '''
    Read csv file into a numpy array
    '''
    # FIXME: Test a file with blank lines in the CSV file.
    with open(filename) as f:
        # Determine if the CSV file has a header row
        has_header = csv.Sniffer().has_header(f.read(1024))
        rows_to_skip = 1 if has_header else 0
        # Go back to the file's beginning and read it into np.array
        f.seek(0)
        # Comment out the previous usage and convert to structured arrays
        #array_to_return = np.loadtxt(f, delimiter=',',
                #skiprows=rows_to_skip).T
        #array_to_return[0,:] *= freq_unit_multiplier
        array_to_return = np.loadtxt(f, dtype={'names': ('frequency', 'amplitude_db'),
            'formats': ('f8', 'f8')}, delimiter=',', skiprows=rows_to_skip)
        array_to_return['frequency'] *= freq_unit_multiplier
        return array_to_return

def _remove_duplicate_frequencies(my_array, duplicates='Keep Max'):
    '''
    Input is a numpy array containing two columns, frequency and amplitude.
    Remove the duplicate frequencies.
    '''

    # Convert from a numpy array to a pandas DataFrame
    #my_dataframe = pd.DataFrame(my_array)
    # FIXME: Try to remove the duplicates without using pandas

    return
    # Sort the data based on the frequency and then the amplitude

def apply_antenna_factor(analyzer_readings, antenna_factors,
        cableloss=False, duplicates='Keep Max'):
    '''
    Applies the antenna factor to spectrum analyzer readings and
    optional 1) applies a cable loss and 2) removes duplicates
    from the data

    # Inputs
    `cableloss` = False or numpy.array to add to spectrum analyzer
    readings in order to calculate the incident electric field
    `duplices` = `Keep Max` removes duplicates and keeps the maximum
    value or `Keep Min` removes duplicates and keeps the minimum value
    '''

    # Remove duplicates and keep the maximum 

    return

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Apply antenna factor')
    parser.add_argument('-s', dest='spectrumanalyzer', required=True,
            help="CSV file containing spectrum analyzer reading.",
            metavar='FILE', type=lambda x: _is_valid_file(parser,x))
    parser.add_argument('-a', dest='antennafactor', required=True,
            help="CSV file containing antenna factor data.",
            metavar='FILE', type=lambda x: _is_valid_file(parser,x))
    parser.add_argument('-c', '--cableloss', dest='cableloss', required=False,
            help="CSV file containing cable loss data.",
            metavar='FILE', type=lambda x: _is_valid_file(parser,x))
    args = parser.parse_args()

    # Open the CSV files and read the data into np.array
    analyzer_readings = _read_csv_file(args.spectrumanalyzer, 1.0e0)
    antenna_factors = _read_csv_file(args.antennafactor, 1.0e6)

    # Print some info about the arrays
    print('Spectrum analyzer data contains {num_points} points'
            ' from {fstart:1.3e} Hz to {fstop:1.3e} Hz'.format(
            num_points = analyzer_readings.shape[1],
            fstart = analyzer_readings[0,0],
            fstop = analyzer_readings[0,-1]))
    print('Antenna factor data contains {num_points} points'
            ' from {fstart:1.3e} Hz to {fstop:1.3e} Hz'.format(
            num_points = antenna_factors.shape[1],
            fstart = antenna_factors[0,0],
            fstop = antenna_factors[0,-1]))

    # Determine if cable loss data was provided
    if args.cableloss:
        cable_losses = _read_csv_file(args.cableloss, 1e6)
        print('Cable loss data contains {num_points} points'
                ' from {fstart:1.3e} Hz to {fstop:1.3e} Hz'.format(
                num_points = cable_losses.shape[1],
                fstart = cable_losses[0,0],
                fstop = cable_losses[0,-1]))

        # Apply the antenna factor and cable loss to the spectrum analyzer
        # readings
        incident_field = apply_antenna_factor(analyzer_readings,
                antenna_factors, cable_losses)
    else:
        incident_field = apply_antenna_factor(analyzer_readings,
                antenna_factors)

