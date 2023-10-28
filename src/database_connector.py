from sqlalchemy import create_engine


class DatabaseConnector:
    """
       DatabaseConnector class for establishing a database connection.

       This class provides methods to initialize a database connection by specifying the path
       to the database file. It uses SQLAlchemy's `create_engine` to create the database engine.

       Args:
           db_file (str): Path to the database file.

       Attributes:
           db_file (str): The path to the database file.
           engine (sqlalchemy.engine.base.Engine): The database engine for data operations.
   """

    def __init__(self, db_file):
        """
            Initialize DatabaseConnector.

            Args:
                db_file (str): Path to the database file.
        """
        try:
            # Store the path to the database file
            self.db_file = db_file

            # Create a database engine using SQLAlchemy
            self.engine = create_engine(f"sqlite:///{db_file}")
        except Exception as e:
            # Handle any exceptions that may occur during initialization
            print(f"An error occurred during DatabaseConnector initialization: {e}")
