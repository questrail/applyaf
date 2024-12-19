# -*- coding: utf-8 -*-
# Copyright (c) 2013-2024 The applyaf developers. All rights reserved.
# Project site: https://github.com/questrail/applyaf
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Apply the antenna factor and cable loss to freq dependent data.

Apply the antenna factor and cable loss data to spectrum analyzer
measurements or other data. The antenna factor and cable loss arrays will
be interpolated onto the same frequencies as found in the given analyzer
data.
"""

# Standard module imports
import csv
from typing import Optional

# Data analysis related imports
import numpy as np
import numpy.typing as npt


def read_csv_file(filename: str, freq_unit_multiplier: float) -> npt.NDArray:
    """Read csv file into a numpy array"""
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
            dtype={
                "names": ("frequency", "amplitude_db"),
                "formats": ("f8", "f8"),
            },
            delimiter=",",
            skiprows=rows_to_skip,
        )
        array_to_return["frequency"] *= freq_unit_multiplier
        return array_to_return


def _remove_duplicate_frequencies(
    unsorted_array: npt.NDArray, keep_max: bool = True
) -> npt.NDArray:
    """Remove duplicates and sort by frequency

    Given a structured numpy array with 'frequency' and 'amplitude_db' fields,
    sort that array first by frequency and then by amplitude. Depending on
    whether the user wants to keep the max or min value, return the sorted
    array containing no duplicate frequency entries.
    Remove the duplicate frequencies.

    Args:
        unsorted_array: A 1D numpy structured array with fields 'frequency' and
            'amplitude_db'.
        keep_max: An optional boolean determining if the max or min amplitude
            values will be kept when duplicate frequencies are found.

    Returns:
        A sorted 1D numpy structured array with fields 'frequency' and
        'amplitude_db' with no duplicate frequencies.
    """

    # Sort the data based on the frequency and then the amplitude
    sorted_array = np.sort(unsorted_array, order=["frequency", "amplitude_db"])
    if keep_max:
        # Reverse the sort order, so that we end up keeping the max value
        sorted_array = sorted_array[::-1]

    # Determine the unique indices and only return those
    unique_indices = np.unique(sorted_array["frequency"], return_index=True)[1]
    return sorted_array[unique_indices]


def apply_antenna_factor(
    analyzer_readings: npt.NDArray,
    antenna_factors: npt.NDArray,
    cable_losses: Optional[npt.NDArray] = None,
    keep_max: bool = True,
) -> npt.NDArray:
    """Apply the antenna factor and cable losses to the input data.

    Applies the frequency dependent antenna factor and, optionally, the cable
    losses to a given input data (typically spectrum analyzer readings). Before
    interpolating the frequencies of the antenna factors and cable losses onto
    the dataset, any duplicate frequency entries are removed and either the
    minimum or maximum amplitude value is kept depending on the user's
    selection.

    This is used to calculate the incident field which is defined as either:

        E(dBuV/m) = Vsa(dBuV) + AF(dB/m) + cable_loss(dB)
        or
        H(dBuA/m) = Vsa(dBuV) - AF(dBohm/m) + cable_loss(dB)


    as given by Eqn 7.62 in *Introduction to Electromagnetic Compatibility* 2nd
    edition by Clayton Paul.

    Args:
        analyzer_readings: A 1D numpy structured array containing the fields
            'frequency' and 'amplitude_db'.
        antenna_factors: A 1D numpy structured array containing the fields
            'frequency' and 'amplitude_db'.
        cables_losses: An optional 1D numpy structured array containing the
            fields 'frequency' and 'amplitude_db'.
        keep_max: An optional boolean determining whether the max or min
            amplitudes are kept whenever duplicate frequency entries are found
            in the antenna_factors or cable_losses arrays.

    Returns:
        A 1D numpy structured array containing the incident field.
    """
    (
        incident_field,
        _,
        _,
    ) = apply_antenna_factor_show_af_cl(
        analyzer_readings, antenna_factors, cable_losses, keep_max
    )
    return incident_field


def apply_antenna_factor_show_af_cl(
    analyzer_readings: npt.NDArray,
    antenna_factors: npt.NDArray,
    cable_losses: Optional[npt.NDArray] = None,
    keep_max: bool = True,
) -> tuple[npt.NDArray, npt.NDArray, npt.NDArray]:
    """Apply the antenna factor and cable losses to the input data and show the
    antenna factors and cable losses at the analyzer frequencies in addition to
    returning the incident field.

    Applies the frequency dependent antenna factor and, optionally, the cable
    losses to a given input data (typically spectrum analyzer readings). Before
    interpolating the frequencies of the antenna factors and cable losses onto
    the dataset, any duplicate frequency entries are removed and either the
    minimum or maximum amplitude value is kept depending on the user's
    selection.

    This is used to calculate the incident field which is defined as either:

        E(dBuV/m) = Vsa(dBuV) + AF(dB/m) + cable_loss(dB)
        or
        H(dBuA/m) = Vsa(dBuV) - AF(dBohm/m) + cable_loss(dB)


    as given by Eqn 7.62 in *Introduction to Electromagnetic Compatibility* 2nd
    edition by Clayton Paul.

    Args:
        analyzer_readings: A 1D numpy structured array containing the fields
            'frequency' and 'amplitude_db'.
        antenna_factors: A 1D numpy structured array containing the fields
            'frequency' and 'amplitude_db'.
        cables_losses: An optional 1D numpy structured array containing the
            fields 'frequency' and 'amplitude_db'.
        keep_max: An optional boolean determining whether the max or min
            amplitudes are kept whenever duplicate frequency entries are found
            in the antenna_factors or cable_losses arrays.

    Returns:
        A tuple containing:
            A 1D numpy structured array containing the incident field.
            A 1D numpy array containing the antenna factors at the analyzer
                frequencies.
            A 1D numpy array containing the cable losses at the analyzer
                frequencies.
    """

    # Remove duplicates and keep the max or min
    analyzer_readings_no_duplicates = _remove_duplicate_frequencies(
        analyzer_readings, keep_max
    )
    antenna_factors_no_duplicates = _remove_duplicate_frequencies(
        antenna_factors, keep_max
    )

    # Interpolate the antenna factors so that they align
    # with the frequencies found in the spectrum analyzer readings
    antenna_factors_at_analyzer_frequencies = np.interp(
        analyzer_readings_no_duplicates["frequency"],
        antenna_factors_no_duplicates["frequency"],
        antenna_factors_no_duplicates["amplitude_db"],
    )

    if isinstance(cable_losses, np.ndarray):
        # If a numpy.array was provided for the cables_losses then
        # remove the duplicates and interpolate so that its frequencies
        # align with the spectrum analyzer readings
        cable_losses_no_duplicates = _remove_duplicate_frequencies(
            cable_losses, keep_max
        )
        cable_losses_at_analyzer_frequencies = np.interp(
            analyzer_readings_no_duplicates["frequency"],
            cable_losses_no_duplicates["frequency"],
            cable_losses_no_duplicates["amplitude_db"],
        )
        incident_field = analyzer_readings_no_duplicates
        incident_field["amplitude_db"] += antenna_factors_at_analyzer_frequencies
        incident_field["amplitude_db"] += cable_losses_at_analyzer_frequencies
    else:
        # There were no cable losses provided, so just apply the
        # antenna factors.
        incident_field = analyzer_readings_no_duplicates
        incident_field["amplitude_db"] += antenna_factors_at_analyzer_frequencies
        cable_losses_at_analyzer_frequencies = np.empty([1, 1])

    return (
        incident_field,
        antenna_factors_at_analyzer_frequencies,
        cable_losses_at_analyzer_frequencies,
    )


def remove_antenna_factor(
    analyzer_readings: npt.NDArray,
    antenna_factors: npt.NDArray,
    cable_losses: Optional[npt.NDArray] = None,
    keep_max: bool = True,
) -> npt.NDArray:
    """Remove the antenna factor and cable losses to the input data.

    Removes the frequency dependent antenna factor and, optionally, the cable
    losses to a given input data (typically spectrum analyzer readings). Before
    interpolating the frequencies of the antenna factors and cable losses onto
    the dataset, any duplicate frequency entries are removed and either the
    minimum or maximum amplitude value is kept depending on the user's
    selection.

    Args:
        analyzer_readings: A 1D numpy structured array containing the fields
            'frequency' and 'amplitude_db'.
        antenna_factors: A 1D numpy structured array containing the fields
            'frequency' and 'amplitude_db'.
        cables_losses: An optional 1D numpy structured array containing the
            fields 'frequency' and 'amplitude_db'.
        keep_max: An optional boolean determining whether the max or min
            amplitudes are kept whenever duplicate frequency entries are found
            in the antenna_factors or cable_losses arrays.

    Returns:
        A 1D numpy structured array containing the incident field.
    """

    # Remove duplicates and keep the max or min
    analyzer_readings_no_duplicates = _remove_duplicate_frequencies(
        analyzer_readings, keep_max
    )
    antenna_factors_no_duplicates = _remove_duplicate_frequencies(
        antenna_factors, keep_max
    )

    # Interpolate the antenna factors so that they align
    # with the frequencies found in the spectrum analyzer readings
    antenna_factors_at_analyzer_frequencies = np.interp(
        analyzer_readings_no_duplicates["frequency"],
        antenna_factors_no_duplicates["frequency"],
        antenna_factors_no_duplicates["amplitude_db"],
    )

    if isinstance(cable_losses, np.ndarray):
        # If a numpy.array was provided for the cables_losses then
        # remove the duplicates and interpolate so that its frequencies
        # align with the spectrum analyzer readings
        cable_losses_no_duplicates = _remove_duplicate_frequencies(
            cable_losses, keep_max
        )
        cable_losses_at_analyzer_frequencies = np.interp(
            analyzer_readings_no_duplicates["frequency"],
            cable_losses_no_duplicates["frequency"],
            cable_losses_no_duplicates["amplitude_db"],
        )
        incident_field = analyzer_readings_no_duplicates
        incident_field["amplitude_db"] -= antenna_factors_at_analyzer_frequencies
        incident_field["amplitude_db"] -= cable_losses_at_analyzer_frequencies
    else:
        # There were no cable losses provided, so just apply the
        # antenna factors.
        incident_field = analyzer_readings_no_duplicates
        incident_field["amplitude_db"] -= antenna_factors_at_analyzer_frequencies

    return incident_field
