from src.data_manager import DataManager
from src.data_analyzer import DataAnalyzer
from src.data_processor import DataProcessor
from src.data_visualizer import DataVisualizer


def main():
    """
        Main function to process and visualize data.
    """
    try:
        # Define db file path
        db_file = "db/data.db"

        # Create data manager, processor, and analyzer Object
        data_manager = DataManager(db_file)
        data_processor = DataProcessor(db_file)
        data_analyzer = DataAnalyzer(db_file)

        # Load training, ideal, and test data into db tables
        train_data = data_manager.load_data_into_table('data/training_data/train.csv', 'train_data')
        ideal_data = data_manager.load_data_into_table('data/ideal_data/ideal.csv', 'ideal_data')
        test_data = data_manager.load_data_into_table('data/test_data/test.csv', 'test_data')

        # Find the best fit between training and ideal functions
        best_fit_results = DataProcessor.find_best_fit(train_data, ideal_data, data_processor.engine)

        # Visualize best fit functions
        DataVisualizer.visualize_best_fit(train_data, ideal_data, best_fit_results)

        # Analyze test data points and calculate close and remaining data points
        close_datapoints, remaining_data_points = DataAnalyzer.analyze_data(test_data, ideal_data, best_fit_results, data_analyzer.engine)

        # Visualize mapping
        DataVisualizer.visualize_mapping(train_data, ideal_data, best_fit_results, close_datapoints, remaining_data_points)

        # Indication of Program End
        print("Program Ended")
    except Exception as e:
        # Handle any exceptions that may occur during program execution
        print(f"During the execution of main(), an error occurred: {e}")


if __name__ == "__main__":
    # Whenever this script runs, execute the main function.
    main()
