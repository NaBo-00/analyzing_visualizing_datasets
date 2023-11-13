class EmptyCSVError(Exception):
    """
        Custom exception class for indicating an empty CSV file.

        When an empty CSV file is attempted to be processed, this exception is raised.

        Args:
            file_path (str): The path to the empty CSV file.

        Attributes:
            file_path (str): The path to the empty CSV file.
            message (str): The error message indicating that the CSV file is empty.
    """
    def __init__(self, file_path):
        """
            Initialize the EmptyCSVError instance.

            Args:
                file_path (str): The path to the empty CSV file.
        """

        # Assign the file_path attribute to the provided file_path
        self.file_path = file_path

        # Create an error message
        self.message = f"The CSV file at '{file_path}' is empty."

        # Call the constructor of the parent class (Exception) with the error message
        super().__init__(self.message)