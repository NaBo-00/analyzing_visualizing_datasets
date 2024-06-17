# Data Processing, Analysis and Visualization

## Project Description
The purpose of this project is to analyze and visualize data. Its objectives are to process different datasets, determine which training and ideal data sets fit together the best, map test data points to the best fit functions, and visualize the results. The project primarily utilizes Python for interactive visualization and data processing, including SQLAlchemy, Pandas, Numpy, and the Bokeh library.

## Project Structure
The project structure consists of the following directories and files:

- `data/`: Contains directories for training (train.csv), ideal (ideal.csv), and test (test.csv) data in CSV format.
- `db/`: Stores the SQLite database file (`data.db`) for data storage.
- `src/`: Holds Python source code for different components:
  - `database_connector.py`: Establishes a database connection using SQLAlchemy.
  - `data_analyzer.py`: Analyzes test data, calculates close and remaining data points.
  - `data_manager.py`: Loads data from CSV files into the database.
  - `data_processor.py`: Processes data, calculates the best fit between training and ideal data.
  - `data_visualizer.py`: Visualizes data using the Bokeh library.
- `graphs/`: Stores HTML files for visualizations, including best fit functions and data mapping.
- `.gitignore`: Contains ignored files and directories for version control.
- `requirements.txt`: Lists the project's Python dependencies.
- `main.py`: The main Python script to run the project.
- `additionalTaskGit_VCS.txt`: Includes the solution to the Additional Task (Task 1.3) from the written assignment paper. 
- `README.md`: This documentation file.

## Installation and Setup
1. Clone the project repository to your local machine.
2. Install the project dependencies by running `pip install -r requirements.txt`.
3. Run `main.py` to execute the project.

## Usage
- Ensure that the CSV files in the `data/` directory contain the necessary data.
- Run `main.py` to process and visualize the data.
- Generated visualizations will be saved in the `graphs/` directory.

## Data Analysis Process
The program follows these steps:
1. **Database Setup**: It establishes a database connection using SQLAlchemy to store and manage data.

2. **Data Loading**: It loads training data, ideal functions, and test data into the database tables.

3. **Best Fit Functions**: It calculates the best-fit ideal functions based on the provided training data.

4. **Data Mapping**: It maps the test data to the chosen ideal functions if the maximum deviation of the calculated regression does not exceed the largest deviation between training data and the ideal function chosen for it by more than a factor of sqrt(2).

5. **Data Visualization**: It creates logical visualizations for training data, test data, chosen ideal functions, and assigned datasets, including deviation information.

6. **Unit Tests**: The program includes unit tests for essential components.

## Dependencies
- Bokeh 3.3.0
- SQLAlchemy 2.0.22
- Pandas 2.1.1
- NumPy 1.26.1
- and others (listed in `requirements.txt`).

## License
The MIT License governs the use of this project.

## Author
- NaBo

For more details and in-depth documentation, refer to the source code and the specific Python files in the `src/` directory.
