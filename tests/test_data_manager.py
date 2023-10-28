import unittest
import pandas as pd
import os
from src.data_manager import DataManager
from sqlalchemy import create_engine
import time


class TestDataManager(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file for testing
        self.db_file = '../db/test.db'
        self.engine = create_engine(f"sqlite:///{self.db_file}")

        # Create the SQLite database file if it doesn't exist
        if not os.path.exists(self.db_file):
            open(self.db_file, 'w').close()

        # Create temporary a CSV file for testing
        csv_data = "x,y\n1,4\n2,5\n3,6"
        unittest_data_path = "unittest_data.csv"
        with open(unittest_data_path, 'w') as csv_file:
            csv_file.write(csv_data)

    def tearDown(self):
        # Give the database connection time to release the file
        time.sleep(2)

        # Delete test.db
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

        # Delete the CSV file created in setUp
        unittest_data_path = "unittest_data.csv"
        if os.path.exists(unittest_data_path):
            os.remove(unittest_data_path)

    def test_load_data_into_table(self):
        # Initialize the DataManager with the temporary database file
        data_manager = DataManager(self.db_file)

        # Define the table name for testing
        table_name = 'test_table'

        #Define path for unittest_data.csv
        unittest_data_path = "unittest_data.csv"

        # Create a sample DataFrame to be loaded
        testing_data = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})

        # Load data into the table and get the loaded data
        loaded_data = data_manager.load_data_into_table(unittest_data_path, table_name)

        # Check if the loaded data matches the original data
        self.assertTrue(testing_data.equals(loaded_data), "Loaded data does not match the original data.")

        # Check if the table was created in the database
        with data_manager.engine.connect() as connection:
            table_exists = connection.dialect.has_table(connection, table_name)
        self.assertTrue(table_exists, "Table was not created in the database.")

        # Close the database engine to release the file
        data_manager.engine.dispose()
