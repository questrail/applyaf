import os.path
import unittest

import numpy as np

import applyaf

class TestReadingCSVFiles(unittest.TestCase):

    def setUp(self):
        self.test_applyaf_directory = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'sample_data')

        # Setup the three filenames
        spectrum_analyzer_readings_filename = os.path.join(
                self.test_applyaf_directory, 'spectrum_analyzer_readings.csv')
        antenna_factor_file = os.path.join(
                self.test_applyaf_directory, 'antenna_factor.csv')
        cable_loss_filename = os.path.join(
                self.test_applyaf_directory, 'cable_loss.csv')

        # Read the thre CSV files
        self.spectrum_analyzer_readings = applyaf._read_csv_file(
                spectrum_analyzer_readings_filename, 1.0e0)
        self.antenna_factors = applyaf._read_csv_file(
                antenna_factor_file, 1.0e6)
        self.cable_losses = applyaf._read_csv_file(
                cable_loss_filename, 1.0e6)

        # Setup the known data arrays
        self.my_data_type = [('frequency', np.float64), ('amplitude_db', np.float64)]
        self.known_spectrum_analyzer_readings = np.array([(3.20238e8, 30.05846),
            (3.12879e8, 30.33228), (3.14719e8, 29.76266),
            (3.18398e8, 30.33228), (3.20238e8, 30.04746),
            (3.22078e8, 29.47784), (3.25758e8, 29.19304)], dtype=self.my_data_type)
        self.known_antenna_factors = np.array([(290e6, 13.0), (300e6, 13.0),
            (325e6, 14.0), (350e6, 14.2), (375e6, 15.2), (400e6, 15.9)],
            dtype=self.my_data_type)
        self.known_cable_losses = np.array([(100e6, 0.20), (200e6, 0.30),
            (500e6, 0.44), (1000e6, 0.61)], dtype=self.my_data_type)

    def test_reading_spectrum_analyzer_readings(self):
        np.testing.assert_array_equal(self.spectrum_analyzer_readings,
                self.known_spectrum_analyzer_readings)

    def test_reading_antenna_factors(self):
        np.testing.assert_array_equal(self.antenna_factors,
                self.known_antenna_factors)

    def test_reading_cable_losses(self):
        np.testing.assert_array_equal(self.cable_losses,
                self.known_cable_losses)

if __name__ == '__main__':
    unittest.main()

