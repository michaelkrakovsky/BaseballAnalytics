# Program Description: Insert all the players (pitchers and positional) and event information into the database.
# Date: April 3, 2019
# Author: Michael Krakovsky
# Version: 1.0

# Author's Notes: This problem is both interesting and challenging because we are confronted with a dependecy issue. We are required to insert 
# the player information prior to the event information; however, we are unable to discern between the type of player. One solution would be
# to insert the data synchronously where the ID is checked in a defined dictionary prior to being inserted. Whenever ID is to be inserted, 
# (either as a positional player or pitcher), the ID prescence will be confirmed. Without proper confirmation, the ID will be inserted into the database.

from pathlib import Path
from os import listdir
from Driver_Exceptions import UnrecognisableMySQLBehaviour
from Player import Player_Driver
from Event import Event_Query_Dict, Event_Driver
from Game import Game_Driver
import pymysql.cursors                                # To Connect to MySQL Database (PyMySQL)

from warnings import filterwarnings                   # Handle warnings from mysql.

from pickle import load                               # Provide pickle capabilities
# from Game import Game_Driver
# from Event import Event_Driver
# from Player import Player_Driver
# from zipfile import ZipFile                         # Used to unzip event files
# import pandas as pd                                 # Gain access to the pandas library
# import pymysql.cursors
# import pickle                                       # Gain access to pickling capabilities
# import pyperclip                                    # Gain access to computer clipboard
# import sys
# import time                                         # Gain access to time capabilities

class Insert_Driver():

    def __init__(self):

        # Class Description: The class will manage and control the data insertions into the baseball database. Note, 
        #   the class does not perform any queries. The queries are delegated to the specific drivers.

        self.path_to_log_files = Path("BaseballAnalytics/logs/insert_file_logs/")                                               # The path to the log file.
        self.path_to_raw_data = Path("BaseballAnalytics/bin/db/raw_data/")                                                      # The path to the raw data that will be inserted into the database.
        self.path_to_player_list = self.path_to_raw_data / 'rosters'                                                            # The folder containing the player data.
        self.path_to_pickle_player_data = self.path_to_player_list / 'pickle_player_data.pickle'                                # The path to the pickle file containing the player information.
        self.conn = pymysql.connect(host="localhost", user="root", passwd="praquplDop#odlg73h?c", db="baseball_stats_db")       # The path to the pymysql connector to access the database.

    def __remove_query_redunancies(self, string_name):

        ### IS THIS NECESSARY ###
        # Function Description: Take the line of data, remove unecessary data points, and return as a string
        # Parameters: string_name (The string of data that requires manipulation)
        # Throws: None
        # Returns: new_string (The string with the proper changes)

        string_name = string_name.rstrip()                   # Remove newline characters.
        separated_data = string_name.split(',')              # Split the csv formatted data into an array.
        if (separated_data != ['']):                         # Guard against the null character in the file.            
            try:
                separated_data.pop(1)                        # Remove the visiting team (Will be used in Game Table) 
            except:
                return string_name                           # Return what was inputted into in the string to be viewed in the error report.
            new_string = ""
            for i in separated_data:                         # Convert list back into a string to be inserted.
                new_string = new_string + i + ','
            new_string = new_string[:-1]                     # Remove comma and newline redundantly added.
            return new_string
        return None                                          # Return none when the list is null.

    def __batter_in_event_insertion(self, event_query_dict, db_connection):

        # Function Description: The function will insert all the proper contents into the Batter_In_Event table.
        # Function Parameters: event_query_dict (The event query dictionary to store the results.), 
        #     db_connection (The current open connection to the database.)
        # Function Throws: UnrecognisableMySQLBehaviour (The exception is thrown when the query was unsuccessfully executed.)
        # Function Returns: Nothing

        event_driver = Event_Driver(db_connection)
        check_insertion = insert_event_dynamic(['Batter_Name', 'idEvent', 'Batting_Team', 'Balls', 'Strikes', 'Batter_Hand', 
                                            'Leadoff_Flag', 'Pinch_Hit_Flag', 'Defensive_Position', 'Lineup_Position'], 
                                            event_query_dict.event_query_dict, 'Batter_In_Event')
        if not check_insertion: raise UnrecognisableMySQLBehaviour("The query into the Batter_In_Event Table was unsucessful.")

    def __error_information_insertion(self, event_query_dict, db_connection):

        # Function Description: Insert the data into the Error Information Pitcher tables. Data will only be
        #    inserted if the data exists thus making its storage dynamic. There are three tables related to pitcher errors.
        # Function Parameters: event_query_dict (The event dictionary organising the file line data.), 
        #    db_connection (The existing connection to the database.)
        # Function Throws: UnrecognisableMySQLBehaviour (Throw the error if any of the queries are unexpected.)
        # Function Returns: Nothing

        event_driver = Event_Driver(db_connection)
        event_status = False                                                        # Anything other than 0 indicates that an error was incurred.
        if int(event_query_dict['1st_Error_Player']) != 0:                          # Stop propogating if we get a zero.
            event_status = event_driver.insert_error_information(event_query_dict['1st_Error_Player'], event_query_dict['1st_Error_Type'], event_query_dict['idEvent'], 1)
            if not event_status: raise UnrecognisableMySQLBehaviour("The 1st Error Player was incorrectly inserted.")
            if int(event_query_dict['2nd_Error_Player']) != 0:
                event_status = event_driver.insert_error_information(event_query_dict['2nd_Error_Player'], event_query_dict['2nd_Error_Type'], event_query_dict['idEvent'], 2)
                if not event_status: raise UnrecognisableMySQLBehaviour("The 2nd Error Player was incorrectly inserted.")
                if int(event_query_dict['3rd_Error_Player']) != 0: 
                    event_status = event_driver.insert_error_information(event_query_dict['3rd_Error_Player'], event_query_dict['3rd_Error_Type'], event_query_dict['idEvent'], 3)
                    if not event_status: raise UnrecognisableMySQLBehaviour("The 3rd Error Player was incorrectly inserted.")

    def __game_table_insertion(self, event_query_dict, db_connection):

        # Function Description: Given a line from the text file, propogate the query throughout the entire database.
        # Function Parameters: event_query_dict (An event query dictionary contianing the information to query the file line.), 
        #   db_connection (The connection to the database.)
        # Function Throws: UnrecognisableMySQLBehaviour (Throw the error when the query was not successfully executed.)
        # Function Returns: Nothing

        game_driver = Game_Driver(db_connection)
        check_game = game_driver.check_game(event_query_dict['Game_ID'])                                           # Ensure the game is inserted.
        if check_game == False: 
            check_game = game_driver.insert_game(event_query_dict['Game_ID'], event_query_dict['Visiting_Team'])    # Insert the game if it is not found.
        if check_game == False:
            raise UnrecognisableMySQLBehaviour("Unable to insert the game into the table after the game was not found within the table.")

    def __event_instance_insertion(self, event_query_dict, db_connection):

        # Function Description: Handle the data insertion into the Event Instance table.
        # Function Parameters: event_query_dict (An event query dictionary)
        # Function Throws: UnrecognisableMySQLBehaviour (Thrown when an SQL query fails in attempt to inserting data into the db.)
        # Function Returns: Nothing

        event_driver = Event_Driver(db_connection)
        check_event = event_driver.insert_event_instance(event_query_dict)
        if (not check_event): raise UnrecognisableMySQLBehaviour("Query Failed attempting to insert into the Event_Instance table.")

    def __propogate_line_into_tables(self, file_line, player_driver, db_connection):

        # Function Description: Given a line from the text file, propogate the query throughout the entire database.
        # Function Parameters: file_line (A line from an event file.), player_driver (A reusable player driver to be used to propogate date throughout the database.), 
        #   db_connection (The connection to the database.)
        # Function Throws: Nothing
        # Function Returns: Nothing

        event_query_dict = Event_Query_Dict(file_line)                                        # Structure the data from the file line.
        self.__game_table_insertion(event_query_dict.event_query_dict, db_connection)         # Propogate into game table. 
        self.__event_instance_insertion(event_query_dict.event_query_dict, db_connection)     # Propogate into the event instance table.
        self.__error_information_insertion(event_query_dict.event_query_dict, db_connection)  # Propogate into the error information table.
        self.__batter_in_event_insertion()

    def process_event_files(self):

        # Function Description: The function will be the driver of the data insertion process. Assume we will possess 
        #   unzipped event files that are to be processed and insert into the database.
        # Function Parameters: Nothing
        # Function Throws: Nothing
        # Function Returns: Nothing

        path_to_event_files = self.path_to_raw_data / '1990_2019_Event_Files'
        with open(self.path_to_pickle_player_data, 'rb') as pickle_file: player_reference = load(pickle_file)
        player_driver = Player_Driver(self.conn, self.path_to_player_list, player_reference)                # Let us only create this once to avoid needless File I/O processing.
        for file_name in listdir(path_to_event_files):
            if not file_name.endswith('.txt'): raise ValueError("There should only be .txt files in this folder. The file processed was {}.".format(file_name))
            event_file = open(path_to_event_files / file_name, 'r') 
            for file_line in event_file:                                # Processes each file line by line.
                self.__propogate_line_into_tables(file_line, player_driver, self.conn)
                break  # STOP AT ONE LINE
            event_file.close()

def clear_tables():     # Temporary Function to Delete Files
    db_connection = pymysql.connect(host="localhost", user="root", passwd="praquplDop#odlg73h?c", db="baseball_stats_db")       # The path to the pymysql connector to access the database.
    cursor = db_connection.cursor()
    cursor.execute('DELETE From event_instance;')           # Event_Instance (29 / 29)
    cursor.execute('DELETE From game_day;')                 # Game_Day (5)
    cursor.execute('DELETE From error_information;')        # Error Information (Possible 6)
    cursor.execute('DELETE From player_information')        # Player Information (4 / 4)
    db_connection.commit()
    cursor.close() 

######### READ IN PLAYER FILE FIRST!!!!
# cursor = db_connection.cursor()
clear_tables()
insert_driver = Insert_Driver()
insert_driver.process_event_files()
#player_driver = Player_Driver(db_connection, Path("BaseballAnalytics/bin/db/raw_data/rosters/"))     # Let us only create this once to avoid needless File I/O processing.

# filterwarnings('error')                         # Convert warnings into exceptions to be caught.                             
# cursor.execute('DELETE FROM game_day where game_day.game_ID = \'TOR201903280\'')               # Empty the tables.
# #cursor.execute('DELETE FROM Event_Instance')
# db_connection.commit()
# try_again = True                                # Track whether we should attempt to the query once.
# attempt_counter = 0
# while try_again and attempt_counter < 5:
#     attempt_counter += 1
#     try:
#         print("SIIIII")
#         cursor.execute(event_query)                  
#     except Warning as warn:
#         print(attempt_counter)
#         print(warn)
#         try_again = False
#         warn = str(warn)
#         warn_number = warn[1:5]
#         if int(warn_number) == 1452:                # Handle warning 1452, indicating foreign key constraint failure. 
#             try_again = True                        # Attempt to insert a query again if a foreign constraint failure was raised. 
#             result = handle_foreign_key_constraint(db_connection, warn) 
#             print(result)






# # Function Name: appendFailureReport
# # Function Description: Document when a query fails and provide meaningful output. Each error message will be separated by 10 '/' chars.
# # Make sure the file is already CREATED!
# # Parameters: folderName (The folder where the query was formed), fileName (The file where the query was formed), 
# # numberID (The ID where the query failed), queryString (The query that was inputted), errorFile (The file to write error reports.)
# # Returns: newString (The string with the proper changes)
# # Throws: None

# def appendFailureReport(folderName, fileName, numberID, queryString, errorFile):
#     stringToWrite = "The folder name: " + str(folderName) + '\n'                       # Build a string. Protect against types by converting params to strings.
#     stringToWrite += "The file name: " + str(fileName) + '\n'
#     stringToWrite += "The ID where the error occured: " + str(numberID) + '\n'
#     stringToWrite += "The query string that was attepted: " + str(queryString) + '\n'
#     stringToWrite += ('/' * 10) + '\n'                                                 # End the string distinctly with 10 '/' chars.
#     f = open(errorFile, "a+")               # Open file, create a file if it doesn't exist. Write, then close file.
#     f.write(stringToWrite)
#     f.close()

# # Function Name: pickleRosterName
# # Function Description: Read the data into a dataframe and store away into a pickle file to be used for different function.
# # Parameters: fileName (The excel file name with the full rosters)
# # Returns: None
# # Throws: None

# def pickleRosterName(fileName):
#     df = pd.read_excel(fileName)
#     tempName = "rosterNames.pickle"         # Store the location of where the file will be pickled
#     tempName = PICKLE_DIR + tempName
#     df.to_pickle(tempName)
#     print("Finished Pickling Roster File.")

# # Function Name: writeEventFileMySql
# # Function Description: Read the data into mySQL and pickle into a file for later use.
# # Parameters: eventFilesDir (The directory with folders holding folder of event files related to the decade)
# # Returns: None
# # Throws: None

# def writeEventFileMySql(eventFilesDir):
#     aCursor = conn.cursor()                                                         # Once connection is established, cursor will be used to insert data.
#     startTime = time.time()
#     shiftingTime = time.time()                                                # Signal to the user that the program is still running
#     numErrors = 0
#     for folder in os.listdir(eventFilesDir):                                  # Loop through each file to read data into the database
#         for fileName in os.listdir(os.path.join(eventFilesDir, folder)):
#             conjoinedFileName = os.path.join(eventFilesDir, folder, fileName)      # Build the path 
#             with open(conjoinedFileName) as f:                                     # Loop through the entire file and input each line into MySQL.
#                 for line in f:
#                     currentID, numErrors = executeQuery(currentID, line, folder, fileName, aCursor, numErrors)        # Manipulate the current ID 
#         currentTime = time.time()
#         if ((currentTime - shiftingTime) > 300):                                                # Indicate number of entries after five minutes
#             print("Time that has passed: " + str((time.time() - startTime) / 60))
#             print("The number of events inserted: " + str(currentID))
#             print(75 * "-")
#             shiftingTime = time.time()                                           # Reset marker to current time
#     conn.commit()                                                                # The connection must be committed to save all the data inputted.
#     aCursor.close()                                                                    # Close the connection
#     print("Connection closed. The database has been loaded. Total runtime: " + str((time.time() - startTime) / 60))
#     print("Total number of events inserted: " + str(currentID))
  


# #pickleRosterName()          # Read the roster file into the dataframe (Requires only one run)
# #readRosterIntoMySQL()            # Read the roster file into the mySQL (Requires only one run)
# #writeEventFileMySql(EVENT_FILES)

# #conn = connect(host="localhost", user="root", passwd="praquplDop#odlg73h?c", db="baseball_stats_db")

# #playerListFile = r"C:\Users\micha\Documents\GitHub\BaseballAnalytics\Documentation\NamesOfPlayersInTheMLB.csv"
# #evnFilesRootDir = r"C:\Users\micha\Documents\Analytics_And_Coding\BaseBall_Analytics\EVN_Or_EVA_Files_To_CSV\Processed_Files"
# #p = Player_Driver(conn, playerListFile)
# #g = Game_Driver(conn)
# #e = Event_Driver(conn)
# #p.checkAndInsert("andre001", "Positional")
# #g.insertGame('TEX201504290', 'SEA') 
