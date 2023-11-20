import pandas as pd
from src.database_connector import DatabaseConnector
from src.exceptions import EmptyCSVError


class DataManager(DatabaseConnector):
    """
        DataManager class for loading data into db table.

        This class inherits db connectivity from the DatabaseConnector class
        in order to load data from a CSV file into a specified table.

        Args:
            db_file (str): Path to db file.

        Methods:
            load_data_into_table(data_file_path, table_name):
                Load required data from a CSV file into a db table.
    """

    def __init__(self, db_file):
        """
            Initialize a DataManager instance with db connection.

            This constructor initializes a DataManager instance and creates db connection
            using the DatabaseConnector constructor.

            Args:
                db_file (str): Path to db file.

            Attributes:
                engine (sqlalchemy.engine.base.Engine): DB engine for data operations.
        """
        super().__init__(db_file)

    def load_data_into_table(self, data_file_path, table_name):
        """
            Load data from CSV file into db table.

            Args:
                data_file_path (str): Path to CSV file.
                table_name (str): Table name to be created in db.

            Returns:
                pd.DataFrame: Loaded csv data.
        Raises:
        EmptyCSVError: Custom Exception if CSV file is empty.
    """

        try:
            # Check if the CSV file is completely empty before attempting to read it
            with open(data_file_path, 'r') as file:
                header_line = file.readline()

            if not header_line.strip():
                raise EmptyCSVError(data_file_path)

            # Read the CSV data into a DataFrame
            csv_data = pd.read_csv(data_file_path)

            # Check if the DataFrame has headers but is empty
            if csv_data.empty:
                raise EmptyCSVError(data_file_path)

            # Save the data to the specified table in db
            csv_data.to_sql(table_name, self.engine, if_exists='replace', index=False)

            return csv_data
        except EmptyCSVError as e:
            # Handle Custom Exception for EmptyCSVError
            print(e)
        except Exception as e:
            # Handle other exceptions
            print(f"An error occurred during load_data_into_table(): {e}")
