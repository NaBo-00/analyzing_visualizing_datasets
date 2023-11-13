import unittest
import pandas as pd
import os
from src.data_manager import DataManager
from sqlalchemy import create_engine
import time


class TestDataManager(unittest.TestCase):
    def setUp(self):
        # Create temp db file for testing
        self.db_file = '../db/test.db'
        self.engine = create_engine(f"sqlite:///{self.db_file}")

        # Create SQLite db file if it doesn't exist
        if not os.path.exists(self.db_file):
            open(self.db_file, 'w').close()

        # Create temp CSV file for testing
        csv_data = "x,y\n1,4\n2,5\n3,6"
        unittest_data_path = "unittest_data.csv"
        with open(unittest_data_path, 'w') as csv_file:
            csv_file.write(csv_data)

    def tearDown(self):
        # Close db engine
        self.engine.dispose()
        time.sleep(2)

        # Delete test.db
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

        # Delete temp CSV file
        unittest_data_path = "unittest_data.csv"
        if os.path.exists(unittest_data_path):
            os.remove(unittest_data_path)

    def test_load_data_into_table(self):
        # Initialize DataManager with temp db file
        data_manager = DataManager(self.db_file)

        # Define table name for test.db
        table_name = 'test_table'

        # Define unittest_data.csv path
        unittest_data_path = "unittest_data.csv"

        # Create representative DataFrame
        testing_data = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})

        # Load data into db
        loaded_data = data_manager.load_data_into_table(unittest_data_path, table_name)

        # Check if loaded data is equal to the original data
        self.assertTrue(testing_data.equals(loaded_data), "Loaded data is not equal to the original data.")

        # Check if table exists in the db
        with data_manager.engine.connect() as connection:
            table_exists = connection.dialect.has_table(connection, table_name)
        self.assertTrue(table_exists, "Table does not exists in db.")

        # Close the database engine to release the file
        data_manager.engine.dispose()
