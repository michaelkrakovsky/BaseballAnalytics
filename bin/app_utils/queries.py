# Script Description: The script will contain queries that can be used across functions. All one needs to input is a connection to the database.
# Script Version: 1.0

from pymysql import connect

class Queries():

    def __init__(self, db_connection):

        # Class Description: The class will provide accessible and reuseable queries accross stages.
        # Class Instantiators: db_connection (pymysql.connections.Connection: The connection to the database.)

        if (str(type(db_connection)) == '<class \'pymysql.connections.Connection\'>'):
            self.__db_connection__ = db_connection
        else:
            raise ValueError("The user did not provide the correct pymysql connector.")

    def fetch_data(self, query):

        # Function Description: Retrieve all the data given a particular query.
        # Function Parameters: query (The query to execute in the database.)
        # Function Throws: Nothing
        # Function Returns: The contents from the query.

        with self.__db_connection__.cursor() as c:
            c.execute(query)
            return c.fetchall()

    def get_all_player_ids(self):

        # Function Description: Retrieve the entire list of players from the data base.
        # Function Parameters: Nothing
        # Function Throws: Nothing
        # Function Returns: The entire list of players existing within the database.

        query = 'select player_information.player_id from player_information;'
        return self.fetch_data(query)

