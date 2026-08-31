# Copyright (c) 2013-2026 The applyaf developers. All rights reserved.
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

# Data analysis related imports
import numpy as np
import numpy.typing as npt


def _has_header(sample: str) -> bool:
    """Determine whether a CSV sample starts with a header row.

    csv.Sniffer decides by comparing the first row against the types of the
    rows below it, so it has nothing to compare against in a single row file
    and reports a header for what is actually data. Every file this module
    reads holds numeric frequency/amplitude pairs, so a first row that parses
    as numbers is data no matter what the sniffer concludes.

    Args:
        sample: The leading characters of a CSV file.

    Returns:
        True if the first row of the sample is a header row.
    """
    first_row = sample.split("\n", 1)[0]
    try:
        [float(field) for field in first_row.split(",")]
    except ValueError:
        # The first row isn't numeric, so let the sniffer weigh in.
        pass
    else:
        return False

    try:
        return csv.Sniffer().has_header(sample)
    except csv.Error:
        # The sniffer couldn't determine a dialect. The first row isn't
        # numeric, so treating it as a header is the better guess.
        return True


def read_csv_file(
    filename: str,
    freq_unit_multiplier: float,
    header: bool | None = None,
) -> npt.NDArray:
    """Read csv file into a numpy array

    Blank lines in the CSV file are ignored.

    Args:
        filename: Path to a two column CSV file of frequency and amplitude.
        freq_unit_multiplier: Scale factor applied to the frequency column,
            e.g. 1.0e6 for a file whose frequencies are given in MHz.
        header: An optional boolean stating whether the file starts with a
            header row. Detected automatically when None.

    Returns:
        A 1D numpy structured array with fields 'frequency' and
        'amplitude_db'.
    """
    with open(filename) as f:
        if header is None:
            header = _has_header(f.read(1024))
        rows_to_skip = 1 if header else 0
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
            # Keep a single row file 1D so it stays indexable by field.
            ndmin=1,
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


def _interpolate_at(
    frequencies: npt.NDArray,
    calibration: npt.NDArray,
    description: str,
    allow_extrapolation: bool,
) -> npt.NDArray:
    """Interpolate calibration data onto the given frequencies.

    np.interp() clamps anything outside the calibration range to the nearest
    endpoint rather than extrapolating, which silently substitutes an
    amplitude that was never measured. Refuse to do that unless asked.

    Args:
        frequencies: A 1D numpy array of frequencies to interpolate onto.
        calibration: A 1D numpy structured array with the fields 'frequency'
            and 'amplitude_db', already sorted and free of duplicates.
        description: What the calibration data represents, used in the error
            message.
        allow_extrapolation: A boolean determining whether frequencies outside
            the calibration range are permitted, in which case they take the
            nearest calibrated amplitude.

    Returns:
        A 1D numpy array of amplitudes at the given frequencies.

    Raises:
        ValueError: If any frequency falls outside the calibration range and
            allow_extrapolation is False.
    """
    if not allow_extrapolation:
        lowest = calibration["frequency"].min()
        highest = calibration["frequency"].max()
        outside = (frequencies < lowest) | (frequencies > highest)
        if outside.any():
            raise ValueError(
                f"{outside.sum()} of {frequencies.size} frequencies fall "
                f"outside the {description}, which span {lowest:.6g} Hz to "
                f"{highest:.6g} Hz. The frequencies in question run from "
                f"{frequencies[outside].min():.6g} Hz to "
                f"{frequencies[outside].max():.6g} Hz and would be clamped to "
                f"the nearest calibrated amplitude. Pass "
                f"allow_extrapolation=True to accept that."
            )

    return np.interp(frequencies, calibration["frequency"], calibration["amplitude_db"])


def apply_antenna_factor(
    analyzer_readings: npt.NDArray,
    antenna_factors: npt.NDArray,
    cable_losses: npt.NDArray | None = None,
    keep_max: bool = True,
    allow_extrapolation: bool = False,
) -> npt.NDArray:
    """Apply the antenna factor and cable losses to the input data.

    Applies the frequency dependent antenna factor and, optionally, the cable
    losses to a given input data (typically spectrum analyzer readings). Before
    interpolating the frequencies of the antenna factors and cable losses onto
    the dataset, any duplicate frequency entries are removed and either the
    minimum or maximum amplitude value is kept depending on the user's
    selection.

    This is used to calculate the incident electric field:

        E(dBuV/m) = Vsa(dBuV) + AF(dB/m) + cable_loss(dB)

    as given by Eqn 7.62 in *Introduction to Electromagnetic Compatibility* 2nd
    edition by Clayton Paul. The magnetic field form of that equation,

        H(dBuA/m) = Vsa(dBuV) - AF(dBohm/m) + cable_loss(dB)

    subtracts the antenna factor, which this function never does. Negate the
    antenna factors before passing them in to calculate H.

    Args:
        analyzer_readings: A 1D numpy structured array containing the fields
            'frequency' and 'amplitude_db'.
        antenna_factors: A 1D numpy structured array containing the fields
            'frequency' and 'amplitude_db'.
        cable_losses: An optional 1D numpy structured array containing the
            fields 'frequency' and 'amplitude_db'.
        keep_max: An optional boolean determining whether the max or min
            amplitudes are kept whenever duplicate frequency entries are
            found. This applies to analyzer_readings as well as to
            antenna_factors and cable_losses, so duplicate readings at one
            frequency are reduced to a single value and the returned array
            can be shorter than the input.
        allow_extrapolation: An optional boolean determining whether analyzer
            frequencies may fall outside the range covered by the antenna
            factors and cable losses. Those frequencies take the nearest
            calibrated amplitude, which was never measured, so this defaults
            to False and such frequencies raise instead.

    Returns:
        A 1D numpy structured array containing the incident field.

    Raises:
        ValueError: If any analyzer frequency falls outside the range covered
            by the antenna factors or cable losses and allow_extrapolation is
            False.
    """
    (
        incident_field,
        _,
        _,
    ) = apply_antenna_factor_show_af_cl(
        analyzer_readings, antenna_factors, cable_losses, keep_max, allow_extrapolation
    )
    return incident_field


def apply_antenna_factor_show_af_cl(
    analyzer_readings: npt.NDArray,
    antenna_factors: npt.NDArray,
    cable_losses: npt.NDArray | None = None,
    keep_max: bool = True,
    allow_extrapolation: bool = False,
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

    This is used to calculate the incident electric field:

        E(dBuV/m) = Vsa(dBuV) + AF(dB/m) + cable_loss(dB)

    as given by Eqn 7.62 in *Introduction to Electromagnetic Compatibility* 2nd
    edition by Clayton Paul. The magnetic field form of that equation,

        H(dBuA/m) = Vsa(dBuV) - AF(dBohm/m) + cable_loss(dB)

    subtracts the antenna factor, which this function never does. Negate the
    antenna factors before passing them in to calculate H.

    Args:
        analyzer_readings: A 1D numpy structured array containing the fields
            'frequency' and 'amplitude_db'.
        antenna_factors: A 1D numpy structured array containing the fields
            'frequency' and 'amplitude_db'.
        cable_losses: An optional 1D numpy structured array containing the
            fields 'frequency' and 'amplitude_db'.
        keep_max: An optional boolean determining whether the max or min
            amplitudes are kept whenever duplicate frequency entries are
            found. This applies to analyzer_readings as well as to
            antenna_factors and cable_losses, so duplicate readings at one
            frequency are reduced to a single value and the returned array
            can be shorter than the input.
        allow_extrapolation: An optional boolean determining whether analyzer
            frequencies may fall outside the range covered by the antenna
            factors and cable losses. Those frequencies take the nearest
            calibrated amplitude, which was never measured, so this defaults
            to False and such frequencies raise instead.

    Returns:
        A tuple containing:
            A 1D numpy structured array containing the incident field.
            A 1D numpy array containing the antenna factors at the analyzer
                frequencies.
            A 1D numpy array containing the cable losses at the analyzer
                frequencies, or zeros if no cable losses were provided.

    Raises:
        ValueError: If any analyzer frequency falls outside the range covered
            by the antenna factors or cable losses and allow_extrapolation is
            False.
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
    antenna_factors_at_analyzer_frequencies = _interpolate_at(
        analyzer_readings_no_duplicates["frequency"],
        antenna_factors_no_duplicates,
        "frequencies covered by the antenna factors",
        allow_extrapolation,
    )

    if isinstance(cable_losses, np.ndarray):
        # If a numpy.array was provided for the cable_losses then
        # remove the duplicates and interpolate so that its frequencies
        # align with the spectrum analyzer readings
        cable_losses_no_duplicates = _remove_duplicate_frequencies(
            cable_losses, keep_max
        )
        cable_losses_at_analyzer_frequencies = _interpolate_at(
            analyzer_readings_no_duplicates["frequency"],
            cable_losses_no_duplicates,
            "frequencies covered by the cable losses",
            allow_extrapolation,
        )
    else:
        # There were no cable losses provided, which is the same as 0 dB of
        # loss at every analyzer frequency.
        cable_losses_at_analyzer_frequencies = np.zeros_like(
            antenna_factors_at_analyzer_frequencies
        )

    incident_field = analyzer_readings_no_duplicates
    incident_field["amplitude_db"] += antenna_factors_at_analyzer_frequencies
    incident_field["amplitude_db"] += cable_losses_at_analyzer_frequencies

    return (
        incident_field,
        antenna_factors_at_analyzer_frequencies,
        cable_losses_at_analyzer_frequencies,
    )


def remove_antenna_factor(
    analyzer_readings: npt.NDArray,
    antenna_factors: npt.NDArray,
    cable_losses: npt.NDArray | None = None,
    keep_max: bool = True,
    allow_extrapolation: bool = False,
) -> npt.NDArray:
    """Remove the antenna factor and cable losses from the input data.

    The inverse of apply_antenna_factor(). Removes the frequency dependent
    antenna factor and, optionally, the cable losses from a given input data
    (typically an incident field), recovering the underlying analyzer
    readings. Before interpolating the frequencies of the antenna factors and
    cable losses onto the dataset, any duplicate frequency entries are removed
    and either the minimum or maximum amplitude value is kept depending on the
    user's selection.

    Args:
        analyzer_readings: A 1D numpy structured array containing the fields
            'frequency' and 'amplitude_db'. Despite the name this is the
            incident field, i.e. the output of apply_antenna_factor().
        antenna_factors: A 1D numpy structured array containing the fields
            'frequency' and 'amplitude_db'.
        cable_losses: An optional 1D numpy structured array containing the
            fields 'frequency' and 'amplitude_db'.
        keep_max: An optional boolean determining whether the max or min
            amplitudes are kept whenever duplicate frequency entries are
            found. This applies to analyzer_readings as well as to
            antenna_factors and cable_losses, so duplicate readings at one
            frequency are reduced to a single value and the returned array
            can be shorter than the input.
        allow_extrapolation: An optional boolean determining whether analyzer
            frequencies may fall outside the range covered by the antenna
            factors and cable losses. Those frequencies take the nearest
            calibrated amplitude, which was never measured, so this defaults
            to False and such frequencies raise instead.

    Returns:
        A 1D numpy structured array containing the analyzer readings.

    Raises:
        ValueError: If any analyzer frequency falls outside the range covered
            by the antenna factors or cable losses and allow_extrapolation is
            False.
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
    antenna_factors_at_analyzer_frequencies = _interpolate_at(
        analyzer_readings_no_duplicates["frequency"],
        antenna_factors_no_duplicates,
        "frequencies covered by the antenna factors",
        allow_extrapolation,
    )

    if isinstance(cable_losses, np.ndarray):
        # If a numpy.array was provided for the cable_losses then
        # remove the duplicates and interpolate so that its frequencies
        # align with the spectrum analyzer readings
        cable_losses_no_duplicates = _remove_duplicate_frequencies(
            cable_losses, keep_max
        )
        cable_losses_at_analyzer_frequencies = _interpolate_at(
            analyzer_readings_no_duplicates["frequency"],
            cable_losses_no_duplicates,
            "frequencies covered by the cable losses",
            allow_extrapolation,
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
