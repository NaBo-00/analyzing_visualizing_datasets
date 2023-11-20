from sqlalchemy import create_engine


class DatabaseConnector:
    """
       DatabaseConnector class for establishing a database connection.

       This class offers functions to initialize a database connection using SQLAlchemy.

       Args:
           db_file (str): Path to db file.

       Attributes:
           db_file (str): Path to db file.
           engine (sqlalchemy.engine.base.Engine): DB engine for data operations.
   """

    def __init__(self, db_file):
        """
            Initialize DatabaseConnector.

            Args:
                db_file (str): db file.
        """
        try:
            # Store db file path
            self.db_file = db_file

            # Create a db engine using SQLAlchemy
            self.engine = create_engine(f"sqlite:///{db_file}")
        except Exception as e:
            # Handle exceptions
            print(f"An error occurred during initialization of DatabaseConnector: {e}")