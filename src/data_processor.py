import numpy as np
import pandas as pd
from src.database_connector import DatabaseConnector


class DataProcessor(DatabaseConnector):
    """
        DataProcessor class for processing data and inheriting database connectivity.

        This class inherits db connectivity from the DatabaseConnector class
        in order to calculate least squares and finding best fit.

        Args:
            db_file (str): Path to db file.

        Attributes:
            engine (sqlalchemy.engine.base.Engine): DB engine for data operations.

        Methods:
            calc_least_squares(y_train, y_ideal): Calculate least squares.
            find_best_fit(train_data, ideal_data): Find best fit between training and ideal data.
    """

    def __init__(self, db_file):
        """
            Initialize a DataProcessor instance including db connection.

            This constructor initializes a DataProcessor instance and creates db connection
            using the DatabaseConnector constructor.

            Args:
                db_file (str): Path to db file.

            Attributes:
                engine (sqlalchemy.engine.base.Engine): DB engine for data operations.
        """

        super().__init__(db_file)

    @staticmethod
    def calc_least_squares(y_train, y_ideal):
        """
            Calculate the least squares.

            Args:
                y_train (pd.Series): Training data.
                y_ideal (pd.Series): Ideal data.

            Returns:
                float: Least squares.
        """

        try:
            # Calculate the least squares
            return np.sum((y_train - y_ideal) ** 2)
        except Exception as e:
            # Handle exceptions
            print(f"An error occurred during calc_least_squares(): {e}")

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
            # Define dictionary to store the best fit results
            best_fit = {"Training Data Function": [], "Best Ideal Function": [], "Best Least Square Value": []}

            # Iterate through the columns of the training data
            for i in range(1, len(train_data.columns)):
                train_column = f'y{i}'
                best_ls = float('inf')
                best_ideal_function = None

                # Iterate through the columns of the ideal data
                for j in range(1, len(ideal_data.columns)):
                    ideal_column = f'y{j}'
                    least_square = DataProcessor.calc_least_squares(train_data[train_column], ideal_data[ideal_column])

                    # Update best fit result if a lower least squares is found
                    if least_square < best_ls:
                        best_ls = least_square
                        best_ideal_function = ideal_column

                # Add best fit result to the results dictionary
                best_fit["Training Data Function"].append(train_column)
                best_fit["Best Ideal Function"].append(best_ideal_function)
                best_fit["Best Least Square Value"].append(best_ls)

            # Create DataFrame from results dictionary
            best_fit_results = pd.DataFrame(best_fit)

            # Create db table for best fit results
            best_fit_results.to_sql("best_fit_results", engine, if_exists='replace', index=False)

            return best_fit_results
        except Exception as e:
            # Handle exceptions
            print(f"An error occurred during find_best_fit(): {e}")