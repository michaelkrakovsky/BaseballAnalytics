# Script Description: The script will contain a basis of functionality used across all feature adding objects namely insertion functions.
# Script Version: 1.0

from warnings import filterwarnings

class Generic_Features():

    def __init__(self, db_connection):

        # Class Description: The class will contain a basis of functionality used across all feature adding objects. 

        if (str(type(db_connection)) == '<class \'pymysql.connections.Connection\'>'):
            self.__db_connection__ = db_connection
        else:
            raise ValueError("The user did not provide the correct pymysql connector.")
        self.log_folder = 'feature_creator_logs'

    def execute_query(self, query):

        # Function Description: The generic query executor that utilises the current connection to the database and executes a query.
        # Function Parameters: query (The query that will be executed.)
        # Function Throws: Nothing
        # Function Returns: True or False (True will be returned if there are no warnings or errors. False will be returned otherwise.)

        cursor = self.__db_connection__.cursor() 
        filterwarnings('error')                                     # Convert warnings into exceptions to be caught.                   
        try:
            cursor.execute(query)                                   # Execute Query: And close the cursor.
            self.__db_connection__.commit()                         # This essentially saves the query execution to the database.
        except Exception as ex:
            status_str = str(ex)
            status_num = status_str[1:5]
            if status_num == '1265':                                 # Commit the query if it matches the appropriate status number.
                self.__db_connection__.commit() 
            else:
                return False
        filterwarnings('always')                                    # Turn the filter for warnings back on.
        cursor.close()
        return True
