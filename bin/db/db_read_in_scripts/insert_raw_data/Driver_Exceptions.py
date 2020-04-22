# The class will store all exceptions related to inserting content into the database.

class UnrecognisableMySQLBehaviour(Exception):    

    def __init__(self, msg):

        # Function Description: Use a custom exception to clarify Error messages when handling SQL Queries
        # Parameters: self (The instance of the object), msg (The string to print as the exception)
        # Throws: None # Returns: None

        super().__init__(msg)