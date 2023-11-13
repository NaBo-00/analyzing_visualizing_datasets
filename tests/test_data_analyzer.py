import os
import time
import unittest
import pandas as pd
import numpy as np
import numpy.testing as npt
from sqlalchemy import create_engine
from src.data_analyzer import DataAnalyzer


class TestDataAnalyzer(unittest.TestCase):
    def setUp(self):
        # Create temp db file for testing
        self.db_file = '../db/test.db'
        self.engine = create_engine(f"sqlite:///{self.db_file}")

        # Create SQLite db file if it doesn't exist
        if not os.path.exists(self.db_file):
            open(self.db_file, 'w').close()

    def tearDown(self):
        # Close db engine
        self.engine.dispose()
        time.sleep(2)

        # Delete temp test.db
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def test_find_close_data_points(self):
        test_data = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        ideal_data = pd.DataFrame({'x': [1, 2, 3], 'y1': [4, 5, 6], 'y2': [3, 6, 9]})
        best_fit_results = pd.DataFrame(
            {'Training Data Function': ['y1'], 'Best Ideal Function': ['y1'], 'Best Least Square Value': [0]})

        close_datapoints = DataAnalyzer.find_close_data_points(test_data, ideal_data, best_fit_results, self.engine)
        expected_result = {'y1': np.array([[1, 4, 0], [2, 5, 0], [3, 6, 0]])}

        for key, value in close_datapoints.items():
            npt.assert_array_almost_equal(value, expected_result[key])

    def test_find_remaining_data_points(self):
        test_data = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        close_datapoints = {'y1': np.array([[1, 4, 0], [2, 5, 0]])}

        remaining_data_points = DataAnalyzer.find_remaining_data_points(test_data, close_datapoints)
        expected_result = np.array([[3, 6]])

        np.testing.assert_array_equal(remaining_data_points, expected_result)
