import numpy as np
import pandas as pd
from src.database_connector import DatabaseConnector


class DataProcessor(DatabaseConnector):
    """
        DataProcessor class for processing data and inheriting database connectivity.

        This class inherits the database connectivity features from the DatabaseConnector class
        to perform data processing tasks, including calculating least squares errors and finding the best fit.

        Args:
            db_file (str): The path to the database file for establishing a database connection.

        Attributes:
            engine (sqlalchemy.engine.base.Engine): The database engine for data operations.

        Methods:
            calc_least_squares(y_train, y_ideal): Calculate the least squares error.
            find_best_fit(train_data, ideal_data): Find the best fit between training and ideal data.
    """

    def __init__(self, db_file):
        """
            Initialize a DataProcessor instance with database connectivity.

            This constructor initializes a DataProcessor instance and establishes a database connection
            by calling the constructor of the parent class, DatabaseConnector.

            Args:
                db_file (str): The path to the database file for establishing a database connection.

            Attributes:
                engine (sqlalchemy.engine.base.Engine): The database engine for data operations.
        """

        super().__init__(db_file)

    @staticmethod
    def calc_least_squares(y_train, y_ideal):
        """
            Calculate the least squares error.

            Args:
                y_train (pd.Series): Training data.
                y_ideal (pd.Series): Ideal data.

            Returns:
                float: Least squares error.
        """

        try:
            # Calculate the least squares error by summing the squared differences between corresponding data points
            return np.sum((y_train - y_ideal) ** 2)
        except Exception as e:
            # Handle any exceptions that may occur during least square calculation
            print(f"An error occurred during least squares calculation: {e}")

    @staticmethod
    def find_best_fit(train_data, ideal_data, engine):
        """
            Find the best fit between training data and ideal data.

            Args:
                train_data (pd.DataFrame): Training data.
                ideal_data (pd.DataFrame): Ideal data.
                engine: Inherit engine from DatabaseConnector.

            Returns:
                pd.DataFrame: Best fit results including Training Data Function, Best Ideal Function, and Best Least Square Value.
        """

        try:
            # Initialize a dictionary to store the best fit results
            best_fit = {"Training Data Function": [], "Best Ideal Function": [], "Best Least Square Value": []}

            # Iterate through the columns of the training data
            for i in range(1, len(train_data.columns)):
                train_column = f'y{i}'
                best_ls = float('inf')
                best_ideal_function = None

                # Iterate through the columns of the ideal data
                for j in range(1, len(ideal_data.columns)):
                    ideal_column = f'y{j}'
                    ls = DataProcessor.calc_least_squares(train_data[train_column], ideal_data[ideal_column])

                    # Update the best fit information if a lower least squares error is found
                    if ls < best_ls:
                        best_ls = ls
                        best_ideal_function = ideal_column

                # Append the best fit information to the results dictionary
                best_fit["Training Data Function"].append(train_column)
                best_fit["Best Ideal Function"].append(best_ideal_function)
                best_fit["Best Least Square Value"].append(best_ls)

            # Create a DataFrame from the results dictionary
            best_fit_results = pd.DataFrame(best_fit)

            # Create a database table for the best fit results
            best_fit_results.to_sql("best_fit_results", engine, if_exists='replace', index=False)

            return best_fit_results
        except Exception as e:
            # Handle any exceptions that may occur during finding best fits
            print(f"An error occurred while finding the best fit: {e}")