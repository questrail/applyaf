# -*- coding: utf-8 -*-
# Copyright (c) 2013-2024 The applyaf developers. All rights reserved.
# Project site: https://github.com/questrail/applyaf
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Unit tests for applyaf.py."""

import os.path
import unittest

import numpy as np

import applyaf


class TestReadingCSVFiles(unittest.TestCase):
    def setUp(self):
        self.test_applyaf_directory = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "sample_data"
        )

        # Setup the three filenames
        spectrum_analyzer_readings_filename = os.path.join(
            self.test_applyaf_directory, "spectrum_analyzer_readings.csv"
        )
        antenna_factor_file = os.path.join(
            self.test_applyaf_directory, "antenna_factor.csv"
        )
        cable_loss_filename = os.path.join(
            self.test_applyaf_directory, "cable_loss.csv"
        )

        # Read the thre CSV files
        self.spectrum_analyzer_readings = applyaf._read_csv_file(
            spectrum_analyzer_readings_filename, 1.0e0
        )
        self.antenna_factors = applyaf._read_csv_file(antenna_factor_file, 1.0e6)
        self.cable_losses = applyaf._read_csv_file(cable_loss_filename, 1.0e6)

        # Setup the known data arrays
        self.my_data_type = [("frequency", np.float64), ("amplitude_db", np.float64)]
        self.known_spectrum_analyzer_readings = np.array(
            [
                (3.20238e8, 30.05846),
                (3.12879e8, 30.33228),
                (3.14719e8, 29.76266),
                (3.18398e8, 30.33228),
                (3.20238e8, 30.04746),
                (3.22078e8, 29.47784),
                (3.25758e8, 29.19304),
            ],
            dtype=self.my_data_type,
        )
        self.known_antenna_factors = np.array(
            [
                (290e6, 13.0),
                (300e6, 13.0),
                (325e6, 14.0),
                (350e6, 14.2),
                (375e6, 15.2),
                (400e6, 15.9),
            ],
            dtype=self.my_data_type,
        )
        self.known_cable_losses = np.array(
            [(100e6, 0.20), (200e6, 0.30), (500e6, 0.44), (1000e6, 0.61)],
            dtype=self.my_data_type,
        )

    def test_reading_spectrum_analyzer_readings(self):
        np.testing.assert_array_equal(
            self.spectrum_analyzer_readings, self.known_spectrum_analyzer_readings
        )

    def test_reading_antenna_factors(self):
        np.testing.assert_array_equal(self.antenna_factors, self.known_antenna_factors)

    def test_reading_cable_losses(self):
        np.testing.assert_array_equal(self.cable_losses, self.known_cable_losses)

    def test_applying_antenna_factor(self):
        # FIXME: Why did I drop one data point?
        known_incident_field = np.array(
            [
                (3.12879e8, 44.200116867),
                (3.14719e8, 43.704955533),
                (3.18398e8, 44.4234524),
                (3.20238e8, 44.224091067),
                (3.22078e8, 43.717929733),
                (3.25758e8, 43.557791067),
            ],
            dtype=self.my_data_type,
        )
        calculated_incident_field = applyaf.apply_antenna_factor(
            self.spectrum_analyzer_readings, self.antenna_factors, self.cable_losses
        )
        np.testing.assert_array_equal(
            calculated_incident_field["frequency"], known_incident_field["frequency"]
        )
        np.testing.assert_array_almost_equal(
            calculated_incident_field["amplitude_db"],
            known_incident_field["amplitude_db"],
        )

    def test_applying_then_removing_antenna_factor(self):
        given_analyzer_readings = np.array(
            [
                (3.12879e8, 43.84744),
                (3.14719e8, 43.35142),
                (3.18398e8, 44.0682),
                (3.20238e8, 43.86798),
                (3.22078e8, 43.36096),
                (3.25758e8, 43.199104),
            ],
            dtype=self.my_data_type,
        )
        calculated_incident_field = applyaf.apply_antenna_factor(
            given_analyzer_readings, self.antenna_factors, self.cable_losses
        )
        calculated_analyzer_readings = applyaf.remove_antenna_factor(
            calculated_incident_field, self.antenna_factors, self.cable_losses
        )
        np.testing.assert_array_equal(
            calculated_analyzer_readings["frequency"],
            given_analyzer_readings["frequency"],
        )
        np.testing.assert_array_almost_equal(
            calculated_analyzer_readings["amplitude_db"],
            given_analyzer_readings["amplitude_db"],
        )

    def test_applying_antenna_factor_without_cable_loss(self):
        known_incident_field = np.array(
            [
                (3.12879e8, 43.84744),
                (3.14719e8, 43.35142),
                (3.18398e8, 44.0682),
                (3.20238e8, 43.86798),
                (3.22078e8, 43.36096),
                (3.25758e8, 43.199104),
            ],
            dtype=self.my_data_type,
        )
        calculated_incident_field = applyaf.apply_antenna_factor(
            self.spectrum_analyzer_readings, self.antenna_factors
        )
        np.testing.assert_array_equal(
            calculated_incident_field["frequency"], known_incident_field["frequency"]
        )
        np.testing.assert_array_almost_equal(
            calculated_incident_field["amplitude_db"],
            known_incident_field["amplitude_db"],
        )


class TestingRemoveDuplicates(unittest.TestCase):
    def setUp(self):
        self.my_data_type = [("frequency", np.float64), ("amplitude_db", np.float64)]
        self.given_array_with_duplicates = np.array(
            [
                (3.20238e8, 30.05846),
                (3.12879e8, 30.33228),
                (3.18398e8, 30.33228),
                (3.20238e8, 30.04746),
                (3.25758e8, 29.19304),
            ],
            dtype=self.my_data_type,
        )
        self.given_array_without_duplicates_kept_max = np.array(
            [
                (3.12879e8, 30.33228),
                (3.18398e8, 30.33228),
                (3.20238e8, 30.05846),
                (3.25758e8, 29.19304),
            ],
            dtype=self.my_data_type,
        )
        self.given_array_without_duplicates_kept_min = np.array(
            [
                (3.12879e8, 30.33228),
                (3.18398e8, 30.33228),
                (3.20238e8, 30.04746),
                (3.25758e8, 29.19304),
            ],
            dtype=self.my_data_type,
        )

    def test_remove_duplicates_keep_max(self):
        array_without_dups_kept_max = applyaf._remove_duplicate_frequencies(
            self.given_array_with_duplicates, True
        )
        np.testing.assert_array_equal(
            array_without_dups_kept_max, self.given_array_without_duplicates_kept_max
        )

    def test_remove_duplicates_keep_min(self):
        array_without_dups_kept_min = applyaf._remove_duplicate_frequencies(
            self.given_array_with_duplicates, keep_max=False
        )
        np.testing.assert_array_equal(
            array_without_dups_kept_min, self.given_array_without_duplicates_kept_min
        )


if __name__ == "__main__":
    unittest.main()
