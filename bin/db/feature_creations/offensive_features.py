# Script Description: The script will prepare all the features related to offensive. The data will queried and then stored in the database
#    to prevent work being re-executed. The intent will be that all players will have there features calculated starting with the first record.
# Script Notes: To date there are three features that will be used related specific to offensive:
#    1. Batting Average
#    2. On Base Percentage
#    3. Slugging Percentage
# Script Creator: Michael Krakovsky
# Script Version: 0.1

class offensive_features():

    def __init__(self, db_connection):

        # Class Description: The class will direct the queries in creating the stats and inputting them into the database. To be exact, 
        #    I will create the tables prior to executing the queries. The tables can be found in the schema diagram.
        # Class Instantiators: db_connection (pymysql.connections.Connection: The connection to the database.)

        if (str(type(db_connection)) == '<class \'pymysql.connections.Connection\'>'):
            self.__db_connection__ = db_connection
        else:
            raise ValueError("The user did not provide the correct pymysql connector.")