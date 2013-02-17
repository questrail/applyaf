import os.path
import unittest

import numpy as np

import applyaf

class TestReadingSpectrumAnalyzerData(unittest.TestCase):

    def setUp(self):
        self.test_applyaf_directory = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'sample_data')

        spectrum_analyzer_readings_filename = os.path.join(
                self.test_applyaf_directory,
                'spectrum_analyzer_readings.csv')

        self.spectrum_analyzer_readings = applyaf._read_csv_file(
                spectrum_analyzer_readings_filename, 1.0e0)

    def test_spectrum_analyzer_readings(self):
        my_data_type = [('frequency', np.float64), ('amplitude_db', np.float64)]
        known_first_three_points = np.array([(3.0184e8, 30.04746),
            (3.05519e8, 30.90190), (3.07359e8, 31.75632)], dtype=my_data_type)
        known_last_three_points = np.array([(1.99264e9, 34.31961),
            (1.99632e9, 34.31961), (1.99632e9, 34.03481)], dtype=my_data_type)
        np.testing.assert_array_equal(self.spectrum_analyzer_readings[0:3],
                known_first_three_points)
        np.testing.assert_array_equal(self.spectrum_analyzer_readings[-3:],
                known_last_three_points)

class TestReadingAntennaFactorData(unittest.TestCase):

    def setUp(self):
        self.test_applyaf_directory = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'sample_data')

        antenna_factors_filename = os.path.join(
                self.test_applyaf_directory,
                'antenna_factor.csv')

        self.antenna_factors = applyaf._read_csv_file(
                antenna_factors_filename, 1.0e6)

    def test_antenna_factors_readings(self):
        my_data_type = [('frequency', np.float64), ('amplitude_db', np.float64)]
        known_first_three_points = np.array([(290e6, 13.0),
            (300e6, 13.0), (325e6, 14.0)], dtype=my_data_type)
        known_last_three_points = np.array([(1.800e9, 29.7),
            (1.9000e9, 30.7), (2.00e9, 31.3)], dtype=my_data_type)
        np.testing.assert_array_equal(self.antenna_factors[0:3],
                known_first_three_points)
        np.testing.assert_array_equal(self.antenna_factors[-3:],
                known_last_three_points)

class TestReadingCableLossData(unittest.TestCase):

    def setUp(self):
        self.test_applyaf_directory = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'sample_data')

        cable_loss_filename = os.path.join(
                self.test_applyaf_directory,
                'cable_loss.csv')

        self.cable_loss = applyaf._read_csv_file(
                cable_loss_filename, 1.0e6)

    def test_cable_loss_readings(self):
        my_data_type = [('frequency', np.float64), ('amplitude_db', np.float64)]
        known_first_three_points = np.array([(20e6, 0.17),
            (50e6, 0.20), (100e6, 0.20)], dtype=my_data_type)
        known_last_three_points = np.array([(17.0e9, 2.54),
            (17.5e9, 2.57), (18.0e9, 2.58)], dtype=my_data_type)
        np.testing.assert_array_equal(self.cable_loss[0:3],
                known_first_three_points)
        np.testing.assert_array_equal(self.cable_loss[-3:],
                known_last_three_points)

if __name__ == '__main__':
    unittest.main()

