from src.data_manager import DataManager
from src.data_analyzer import DataAnalyzer
from src.data_processor import DataProcessor
from src.data_visualizer import DataVisualizer


def main():
    """
        Main function to process and visualize data.
    """
    try:
        # Define the path to the database file
        db_file = "db/data.db"

        # Initialize data manager, processor, and analyzer
        data_manager = DataManager(db_file)
        data_processor = DataProcessor(db_file)
        data_analyzer = DataAnalyzer(db_file)

        # Load training, ideal, and test data into database tables
        train_data = data_manager.load_data_into_table('data/training_data/train.csv', 'train_data')
        ideal_data = data_manager.load_data_into_table('data/ideal_data/ideal.csv', 'ideal_data')
        test_data = data_manager.load_data_into_table('data/test_data/test.csv', 'test_data')

        # Find the best fit between training and ideal data
        best_fit_results = DataProcessor.find_best_fit(train_data, ideal_data, data_processor.engine)

        # Visualize the best fit functions
        DataVisualizer.visualize_best_fit(train_data, ideal_data, best_fit_results)

        # Analyze the test data and calculate close and remaining data points
        close_datapoints, remaining_data_points = DataAnalyzer.analyze_data(test_data, ideal_data, best_fit_results, data_analyzer.engine)

        # Visualize the mapping between training and ideal functions
        DataVisualizer.visualize_mapping(train_data, ideal_data, best_fit_results, close_datapoints, remaining_data_points)

        # Print a message to indicate the program has ended
        print("Program Ended")
    except Exception as e:
        # Handle any exceptions that may occur during program execution
        print(f"During the execution of main(), an error occurred: {e}")


if __name__ == "__main__":
    # Whenever this script runs, execute the main function.
    main()
