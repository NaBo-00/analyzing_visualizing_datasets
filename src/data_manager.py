import pandas as pd
from src.database_connector import DatabaseConnector
from src.exceptions import EmptyCSVError


class DataManager(DatabaseConnector):
    """
        DataManager class for loading data into a database table.

        This class inherits database connectivity features from the DatabaseConnector class and provides a method to load
        data from a CSV file into a specified table in the connected database.

        Args:
            db_file (str): The path to the database file required for establishing a database connection.

        Methods:
            load_data_into_table(data_file_path, table_name):
                Load required data from a CSV file into a table in the database.
    """

    def __init__(self, db_file):
        """
            Initialize a DataManager instance with database connectivity.

            This constructor initializes a DataManager instance and establishes a database connection
            by calling the constructor of the parent class, DatabaseConnector.

            Args:
                db_file (str): The path to the database file required for establishing a database connection.

            Attributes:
                engine (sqlalchemy.engine.base.Engine): The database engine provided by sqlalchemy for data operations.
        """
        super().__init__(db_file)

    def load_data_into_table(self, data_file_path, table_name):
        """
            Load data from a CSV file into a table in the database.

            Args:
                data_file_path (str): Path to the CSV data file.
                table_name (str): Name of the table to create in the database.

            Returns:
                pd.DataFrame: Loaded data.
        Raises:
        EmptyCSVError: If the CSV file is empty.

        Example:
            To load data from a CSV file into a database table:
            >>> data_manager.load_data_into_table('data.csv', 'my_table')
    """

        try:
            # Check if the CSV file is completely empty before attempting to read it
            with open(data_file_path, 'r') as file:
                first_line = file.readline()

            if not first_line.strip():
                raise EmptyCSVError(data_file_path)

            # Read the CSV data into a DataFrame
            data = pd.read_csv(data_file_path)

            # Check if the DataFrame has headers but is empty
            if data.empty:
                raise EmptyCSVError(data_file_path)

            # Save the data to the specified table in the database
            data.to_sql(table_name, self.engine, if_exists='replace', index=False)

            return data
        except EmptyCSVError as e:
            print(e) # Print the EmptyCSVError message
        except Exception as e:
            # Handle any exceptions that may occur during loading data
            print(f"An error occurred while loading data into the table: {e}") # Print other exceptions
