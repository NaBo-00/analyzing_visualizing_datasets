import os
import unittest
import time
import pandas as pd
from sqlalchemy import create_engine
from src.data_processor import DataProcessor


class TestDataProcessor(unittest.TestCase):
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

        # Delete test.db
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def test_calc_least_squares(self):
        y_train = pd.Series([1, 2, 3])
        y_ideal = pd.Series([1, 3, 3])

        least_squares = DataProcessor.calc_least_squares(y_train, y_ideal)
        expected_result = 1

        self.assertEqual(least_squares, expected_result)

    def test_find_best_fit(self):
        train_data = pd.DataFrame({'x': [-5, 0, 5], 'y1': [1, 2, 3], 'y2': [4, 5, 6]})
        ideal_data = pd.DataFrame({'x': [-5, 0, 5], 'y1': [4.3, 5, 6], 'y2': [8, 9, 10], 'y3': [1.2, 2, 3]})

        best_fit_results = DataProcessor.find_best_fit(train_data, ideal_data, self.engine)
        expected_result = pd.DataFrame({'Training Data Function': ['y1', 'y2'],
                                        'Best Ideal Function': ['y3', 'y1'],
                                        'Best Least Square Value': [0.04, 0.09]})

        pd.testing.assert_frame_equal(best_fit_results, expected_result)