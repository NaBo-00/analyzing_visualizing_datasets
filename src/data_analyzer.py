import math
import numpy as np
import pandas as pd
from src.database_connector import DatabaseConnector


class DataAnalyzer(DatabaseConnector):
    """
        DataAnalyzer class for analyzing test data and calculating close and remaining data points.

        This class inherits database connectivity features from the DatabaseConnector class
        and provides methods to analyze test data by finding close data points and remaining data points.

        Args:
            db_file (str): The path to the database file for establishing a database connection.

        Methods:
            analyze_data(test_data, ideal_data, best_fit_results): Analyze the test data and calculate close and remaining data points.
            find_close_data_points(test_data, ideal_data, best_fit_results, engine): Find close data points in the test data.
            find_remaining_data_points(test_data, close_datapoints): Find remaining data points in the test data.
    """

    def __init__(self, db_file):
        """
            Initialize a DataAnalyzer instance with database connectivity.

            This constructor initializes a DataAnalyzer instance and establishes a database connection
            by calling the constructor of the parent class, DatabaseConnector.

            Args:
                db_file (str): The path to the database file for establishing a database connection.

            Attributes:
                engine (sqlalchemy.engine.base.Engine): The database engine for data operations.

        """
        super().__init__(db_file)
    @staticmethod
    def analyze_data(test_data, ideal_data, best_fit_results, engine):
        """
            Analyze the test data and calculate close data points and remaining data points.

            Args:
                test_data (pd.DataFrame): Test data.
                ideal_data (pd.DataFrame): Ideal data.
                best_fit_results (pd.DataFrame): Best fit results.

            Returns:
                Tuple (close_datapoints, remaining_data_points): Close data points and remaining data points.
        """

        try:
            # Call the static methods to find close data points and remaining data points
            close_datapoints = DataAnalyzer.find_close_data_points(test_data, ideal_data, best_fit_results, engine)
            remaining_data_points = DataAnalyzer.find_remaining_data_points(test_data, close_datapoints)

            return close_datapoints, remaining_data_points
        except Exception as e:
            # Handle any exceptions that may occur during data analysis
            print(f"An error occurred during data analysis: {e}")

    @staticmethod
    def find_close_data_points(test_data, ideal_data, best_fit_results, engine):
        """
            Find close data points in the test data.

            Args:
                test_data (pd.DataFrame): Test data.
                ideal_data (pd.DataFrame): Ideal data.
                best_fit_results (pd.DataFrame): Best fit results.
                engine: Inherit engine from DatabaseConnector.

            Returns:
                Dict: Close data points.
        """

        try:
            # Create a dictionary to store close data points for each ideal function
            close_datapoints = {}

            # Calculate the maximum deviation (square root of 2)
            max_deviation = math.sqrt(2)

            # Iterate through the test data and check each point against each ideal function
            for index, row in test_data.iterrows():
                x_test = row['x']
                y_test = row['y']
                closest_ideal_function = None
                min_deviation = float('inf')

                for ideal_function_name in best_fit_results["Best Ideal Function"]:
                    if not ideal_data[ideal_function_name][ideal_data['x'] == x_test].values:
                        print(f"error: value {x_test} missing")
                        continue

                    # Calculate the deviation between the test point and the current ideal function
                    deviation = abs(y_test - ideal_data[ideal_function_name][ideal_data['x'] == x_test].values[0])

                    # save deviation according to y test and y test and add ideal_function name
                    if deviation <= max_deviation and deviation < min_deviation:
                        min_deviation = deviation
                        closest_ideal_function = ideal_function_name

                if closest_ideal_function is not None:
                    # Append the closest data point to the list
                    close_data_points = [x_test, y_test, min_deviation]

                    # If this ideal function has not been added to the dictionary, create a new entry
                    if closest_ideal_function not in close_datapoints:
                        close_datapoints[closest_ideal_function] = [close_data_points]
                    else:
                        close_datapoints[closest_ideal_function].append(close_data_points)
            # Convert the lists of close data points to NumPy arrays
            for key, value in close_datapoints.items():
                close_datapoints[key] = np.array(value)

            # Store close datapoints into db
            # Create an empty list to store rows of data
            data_rows = []

            # Iterate through the dictionary and flatten the arrays
            for ideal_function, data_array in close_datapoints.items():
                for data_point in data_array:
                    x_value, y_value, deviation = data_point
                    data_rows.append([x_value, y_value, deviation, ideal_function])

            # Create a DataFrame from the list of rows
            close_datapoints_results = pd.DataFrame(data_rows, columns=['x', 'y', 'Deviation', 'Ideal Function'])

            # Create a table in the database to store close data points
            close_datapoints_results.to_sql("close_datapoints_results", engine, if_exists='replace', index=False)

            return close_datapoints
        except Exception as e:
            # Handle any exceptions that may occur during finding close datapoints
            print(f"An error occurred while finding close data points: {e}")

    @staticmethod
    def find_remaining_data_points(test_data, close_datapoints):
        """
            Find remaining data points in the test data.

            Args:
                test_data (pd.DataFrame): Test data.
                close_datapoints (Dict): Close data points.

            Returns:
                np.ndarray: Remaining data points.
        """

        try:
            remaining_data_points = []

            # Iterate through the test data to find data points not in the close data points
            for index, row in test_data.iterrows():
                x_test = row['x']
                y_test = row['y']

                is_in_close_datapoints = False

                # Check if the data point is in the close data points
                for data_points in close_datapoints.values():
                    if any((x_test == x and y_test == y) for (x, y, _) in data_points):
                        is_in_close_datapoints = True
                        break

                if not is_in_close_datapoints:
                    remaining_data_points.append([x_test, y_test])

            remaining_data_points = np.array(remaining_data_points)

            return remaining_data_points
        except Exception as e:
            # Handle any exceptions that may occur during finding remaining datapoints
            print(f"An error occurred while finding remaining data points: {e}")
