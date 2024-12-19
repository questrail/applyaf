# -*- coding: utf-8 -*-
# Copyright (c) 2013-2024 The applyaf developers. All rights reserved.
# Project site: https://github.com/questrail/applyaf
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Unit tests for applyaf.py."""

import os.path

import numpy as np
import pytest

import applyaf


@pytest.fixture
def my_data_type():
    return [("frequency", np.float64), ("amplitude_db", np.float64)]


@pytest.fixture
def known_analyzer_readings(my_data_type):
    return np.array(
        [
            (3.20238e8, 30.05846),
            (3.12879e8, 30.33228),
            (3.14719e8, 29.76266),
            (3.18398e8, 30.33228),
            (3.20238e8, 30.04746),
            (3.22078e8, 29.47784),
            (3.25758e8, 29.19304),
        ],
        dtype=my_data_type,
    )


@pytest.fixture
def known_antenna_factors(my_data_type):
    return np.array(
        [
            (290e6, 13.0),
            (300e6, 13.0),
            (325e6, 14.0),
            (350e6, 14.2),
            (375e6, 15.2),
            (400e6, 15.9),
        ],
        dtype=my_data_type,
    )


@pytest.fixture
def known_cable_losses(my_data_type):
    return np.array(
        [
            (100e6, 0.20),
            (200e6, 0.30),
            (500e6, 0.44),
            (1000e6, 0.61),
        ],
        dtype=my_data_type,
    )


@pytest.fixture
def known_incident_field(my_data_type):
    return np.array(
        [
            (3.12879e8, 44.200116867),
            (3.14719e8, 43.704955533),
            (3.18398e8, 44.4234524),
            (3.20238e8, 44.224091067),
            (3.22078e8, 43.717929733),
            (3.25758e8, 43.557791067),
        ],
        dtype=my_data_type,
    )


@pytest.fixture
def given_analyzer_readings(my_data_type):
    return np.array(
        [
            (3.12879e8, 43.84744),
            (3.14719e8, 43.35142),
            (3.18398e8, 44.0682),
            (3.20238e8, 43.86798),
            (3.22078e8, 43.36096),
            (3.25758e8, 43.199104),
        ],
        dtype=my_data_type,
    )


@pytest.fixture
def test_applyaf_dir():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample_data")


@pytest.fixture
def analyzer_readings(test_applyaf_dir):
    analyzer_readings_filename = os.path.join(
        test_applyaf_dir, "spectrum_analyzer_readings.csv"
    )
    return applyaf.read_csv_file(analyzer_readings_filename, 1.0e0)


@pytest.fixture
def antenna_factors(test_applyaf_dir):
    antenna_factor_file = os.path.join(test_applyaf_dir, "antenna_factor.csv")
    return applyaf.read_csv_file(antenna_factor_file, 1.0e6)


@pytest.fixture
def cable_losses(test_applyaf_dir):
    cable_loss_filename = os.path.join(test_applyaf_dir, "cable_loss.csv")
    return applyaf.read_csv_file(cable_loss_filename, 1.0e6)


class TestReadingCSVFiles:
    def test_reading_spectrum_analyzer_readings(
        self, analyzer_readings, known_analyzer_readings
    ):
        np.testing.assert_array_equal(analyzer_readings, known_analyzer_readings)

    def test_reading_antenna_factors(self, antenna_factors, known_antenna_factors):
        np.testing.assert_array_equal(antenna_factors, known_antenna_factors)

    def test_reading_cable_losses(self, cable_losses, known_cable_losses):
        np.testing.assert_array_equal(cable_losses, known_cable_losses)


class TestApplyAntennaFactors:
    def test_applying_antenna_factor(
        self, analyzer_readings, antenna_factors, cable_losses, known_incident_field
    ):
        # FIXME: Why did I drop one data point?
        calculated_incident_field = applyaf.apply_antenna_factor(
            analyzer_readings, antenna_factors, cable_losses
        )
        np.testing.assert_array_equal(
            calculated_incident_field["frequency"], known_incident_field["frequency"]
        )
        np.testing.assert_array_almost_equal(
            calculated_incident_field["amplitude_db"],
            known_incident_field["amplitude_db"],
        )

    def test_applying_then_removing_antenna_factor(
        self, given_analyzer_readings, antenna_factors, cable_losses
    ):
        calculated_incident_field = applyaf.apply_antenna_factor(
            given_analyzer_readings, antenna_factors, cable_losses
        )
        calculated_analyzer_readings = applyaf.remove_antenna_factor(
            calculated_incident_field, antenna_factors, cable_losses
        )
        np.testing.assert_array_equal(
            calculated_analyzer_readings["frequency"],
            given_analyzer_readings["frequency"],
        )
        np.testing.assert_array_almost_equal(
            calculated_analyzer_readings["amplitude_db"],
            given_analyzer_readings["amplitude_db"],
        )

    def test_applying_antenna_factor_without_cable_loss(
        self, my_data_type, analyzer_readings, antenna_factors
    ):
        known_incident_field = np.array(
            [
                (3.12879e8, 43.84744),
                (3.14719e8, 43.35142),
                (3.18398e8, 44.0682),
                (3.20238e8, 43.86798),
                (3.22078e8, 43.36096),
                (3.25758e8, 43.199104),
            ],
            dtype=my_data_type,
        )
        calculated_incident_field = applyaf.apply_antenna_factor(
            analyzer_readings, antenna_factors
        )
        np.testing.assert_array_equal(
            calculated_incident_field["frequency"], known_incident_field["frequency"]
        )
        np.testing.assert_array_almost_equal(
            calculated_incident_field["amplitude_db"],
            known_incident_field["amplitude_db"],
        )


# class TestRemoveDuplicates():
#     def setUp(self):
#         self.my_data_type = [("frequency", np.float64), ("amplitude_db", np.float64)]
#         self.given_array_with_duplicates = np.array(
#             [
#                 (3.20238e8, 30.05846),
#                 (3.12879e8, 30.33228),
#                 (3.18398e8, 30.33228),
#                 (3.20238e8, 30.04746),
#                 (3.25758e8, 29.19304),
#             ],
#             dtype=self.my_data_type,
#         )
#         self.given_array_without_duplicates_kept_max = np.array(
#             [
#                 (3.12879e8, 30.33228),
#                 (3.18398e8, 30.33228),
#                 (3.20238e8, 30.05846),
#                 (3.25758e8, 29.19304),
#             ],
#             dtype=self.my_data_type,
#         )
#         self.given_array_without_duplicates_kept_min = np.array(
#             [
#                 (3.12879e8, 30.33228),
#                 (3.18398e8, 30.33228),
#                 (3.20238e8, 30.04746),
#                 (3.25758e8, 29.19304),
#             ],
#             dtype=self.my_data_type,
#         )
#
#     def test_remove_duplicates_keep_max(self):
#         array_without_dups_kept_max = applyaf._remove_duplicate_frequencies(
#             self.given_array_with_duplicates, True
#         )
#         np.testing.assert_array_equal(
#             array_without_dups_kept_max, self.given_array_without_duplicates_kept_max
#         )
#
#     def test_remove_duplicates_keep_min(self):
#         array_without_dups_kept_min = applyaf._remove_duplicate_frequencies(
#             self.given_array_with_duplicates, keep_max=False
#         )
#         np.testing.assert_array_equal(
#             array_without_dups_kept_min, self.given_array_without_duplicates_kept_min
#         )
