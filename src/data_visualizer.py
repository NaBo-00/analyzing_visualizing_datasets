from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource


class DataVisualizer:
    """
        DataVisualizer class for visualizing data.

        This class includes methods to create interactive Bokeh plots for visualizing best fit functions and mapping between
        training and ideal functions.

        Methods:
            visualize_best_fit(train_data, ideal_data, best_fit_results): Visualize best fit functions.
            visualize_mapping(train_data, ideal_data, best_fit_results, close_datapoints, remaining_data_points):
                Visualize mapping between training and ideal functions.
    """

    @staticmethod
    def visualize_best_fit(train_data, ideal_data, best_fit_results):
        """
            Visualize best fit functions.

            Args:
                train_data (pd.DataFrame): Training data.
                ideal_data (pd.DataFrame): Ideal data.
                best_fit_results (pd.DataFrame): Best fit results.
        """
        try:
            # Create Bokeh plot
            x_values = train_data['x']
            plot = figure(title="Best Fit Functions", x_axis_label="x", y_axis_label="y")

            # Define colors for each line
            colors = ['blue', 'green', 'red', 'purple']

            # Plot training data functions
            for i, train_col in enumerate(best_fit_results["Training Data Function"]):
                train_source = ColumnDataSource(data={'x': x_values, 'y': train_data[train_col]})
                plot.line('x', 'y', source=train_source, line_width=2, legend_label=f'{train_col} (Train)', line_color=colors[i])

            # Plot ideal data functions
            for i, ideal_col in enumerate(best_fit_results["Best Ideal Function"]):
                ideal_source = ColumnDataSource(data={'x': x_values, 'y': ideal_data[ideal_col]})
                plot.line('x', 'y', source=ideal_source, line_width=2, legend_label=f'{ideal_col} (Ideal)', line_color=colors[i])

            # Configure plot labels and styling
            plot.legend.title = 'Functions'
            plot.legend.label_text_font_size = "10pt"
            plot.title.text_font_size = "16pt"
            plot.xaxis.axis_label_text_font_size = "14pt"
            plot.yaxis.axis_label_text_font_size = "14pt"

            # Define and save the output file
            output_path = "graphs/best_fit.html"
            output_file(output_path)

            # Show plot
            show(plot)
        except Exception as e:
            # Handle exceptions
            print(f"An error occurred during visualize_best_fit(): {e}")

    @staticmethod
    def visualize_mapping(train_data, ideal_data, best_fit_results, close_datapoints, remaining_data_points):
        """
            Visualize mapping between training and ideal functions.

            Args:
                train_data (pd.DataFrame): Training data.
                ideal_data (pd.DataFrame): Ideal data.
                best_fit_results (pd.DataFrame): Best fit results.
                close_datapoints (dict): Close data points.
                remaining_data_points (np.array): Remaining data points.
        """
        try:
            # Create Bokeh plot
            x_values = train_data['x']
            plot = figure(title="Mapping", x_axis_label="x", y_axis_label="y")

            # Define colors for each points
            colors = ['blue', 'green', 'red', 'purple']

            # Plot training data functions
            for i, train_col in enumerate(best_fit_results["Training Data Function"]):
                train_source = ColumnDataSource(data={'x': x_values, 'y': train_data[train_col]})
                plot.line('x', 'y', source=train_source, line_width=2, legend_label=f'{train_col} (Train)', line_color=colors[i])

            # Plot ideal data functions
            for i, ideal_col in enumerate(best_fit_results["Best Ideal Function"]):
                ideal_source = ColumnDataSource(data={'x': x_values, 'y': ideal_data[ideal_col]})
                plot.line('x', 'y', source=ideal_source, line_width=2, legend_label=f'{ideal_col} (Ideal)', line_color=colors[i])

            # Plot close data points for each ideal function
            for ideal_function_name, data_points in close_datapoints.items():
                color_index = best_fit_results["Best Ideal Function"].to_list().index(ideal_function_name)
                color = colors[color_index]

                x_values = data_points[:, 0]
                y_values = data_points[:, 1]

                test_data_source = ColumnDataSource(data={'x': x_values, 'y': y_values})
                plot.circle('x', 'y', source=test_data_source, size=8, color=color, legend_label=f'Test Data ({ideal_function_name})')

            # Plot remaining data points
            x_values_remaining = remaining_data_points[:, 0]
            y_values_remaining = remaining_data_points[:, 1]

            test_data_source_remaining = ColumnDataSource(data={'x': x_values_remaining, 'y': y_values_remaining})
            plot.circle('x', 'y', source=test_data_source_remaining, size=8, color='yellow', line_color='black', legend_label='Out of Bounds')

            # Configure plot labels and styling
            plot.legend.title = 'Functions'
            plot.legend.label_text_font_size = "10pt"
            plot.title.text_font_size = "16pt"
            plot.xaxis.axis_label_text_font_size = "14pt"
            plot.yaxis.axis_label_text_font_size = "14pt"

            # Define and save the output file
            output_path = "graphs/mapping.html"
            output_file(output_path)

            # Show plot
            show(plot)
        except Exception as e:
            # Handle exceptions
            print(f"An error occurred during visualize_mapping(): {e}")