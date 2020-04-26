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
from pickle import load                               # Provide pickle capabilities
import pymysql.cursors                                # To Connect to MySQL Database (PyMySQL)

from warnings import filterwarnings                   # Handle warnings from mysql.


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

    def __pinch_related_insertions(self, player_driver, event_query_dict, event_driver, db_connection):

        # Function Description: Insert the contents related to the pinch hitters and runners. (Resp Pitchers, Runners On)
        # Function Parameters: player_driver (The reference to a player driver obeck to insert the player information.)
        #     event_query_dict (The event query dictionary to store the results.),
        #     event_driver (The event driver that allows the insertion into an event related table.)
        #     db_connection (The current open connection to the database.)
        # Function Throws: UnrecognisableMySQLBehaviour (The error is thrown when the query was incorrectly inserted.)
        # Function Returns: Nothing

        if not event_query_dict['Runner_Removed_For_Pinch-Runner_On_1st'] == '':                                                             # Do not attempt an insertion if there is no player to insert.
            check_insertion = event_driver.insert_player_from_event(['Runner_Removed_For_Pinch-Runner_On_1st', 'idEvent'], player_driver, 
                                                                    event_query_dict, 'Pinch_Runner_Removed_1st', 'Runner_Removed_For_Pinch-Runner_On_1st')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Pinch_Runner_Removed_1st table was unsuccessful.")
        if not event_query_dict['Runner_Removed_For_Pinch-Runner_On_1st'] == '':
        check_insertion = event_driver.insert_player_from_event(['Runner_Removed_For_Pinch-Runner_On_2nd', 'idEvent'], player_driver, 
                                                                event_query_dict, 'Pinch_Runner_Removed_2nd', 'Runner_Removed_For_Pinch-Runner_On_2nd')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Pinch_Runner_Removed_2nd table was unsuccessful.")
        if not event_query_dict['Runner_Removed_For_Pinch-Runner_On_1st'] == '':
        check_insertion = event_driver.insert_player_from_event(['Runner_Removed_For_Pinch-Runner_On_3rd', 'idEvent'], player_driver, 
                                                                event_query_dict, 'Pinch_Runner_Removed_3rd', 'Runner_Removed_For_Pinch-Runner_On_3rd')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Pinch_Runner_Removed_3rd table was unsuccessful.")
        if not event_query_dict['Runner_Removed_For_Pinch-Runner_On_1st'] == '':                                                             
            check_insertion = event_driver.insert_player_from_event(['Runner_Removed_For_Pinch-Runner_On_1st', 'idEvent'], player_driver, 
                                                                event_query_dict, 'Pinch_Runner_Removed_1st', 'Runner_Removed_For_Pinch-Runner_On_1st')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Pinch_Runner_Removed_1st table was unsuccessful.")
            
    def __base_runner_insertion(self, player_driver, event_query_dict, event_driver, db_connection):

        # Function Description: Insert the contents related to the base runners. (Resp Pitchers, Runners On)
        # Function Parameters: player_driver (The reference to a player driver obeck to insert the player information.)
        #     event_query_dict (The event query dictionary to store the results.),
        #     event_driver (The event driver that allows the insertion into an event related table.)
        #     db_connection (The current open connection to the database.)
        # Function Throws: UnrecognisableMySQLBehaviour (The error is thrown when the query was incorrectly inserted.)
        # Function Returns: Nothing

        if not event_query_dict['Responsible_Pitcher_For_Runner_On_1st'] == '':                                                             # Do not attempt an insertion if there is no player to insert.
            check_insertion = event_driver.insert_player_from_event(['Responsible_Pitcher_For_Runner_On_1st', 'idEvent'], player_driver, 
                                                                    event_query_dict, 'Responsible_Pitcher_For_First', 'Responsible_Pitcher_For_Runner_On_1st')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Responsible_Pitcher_For_First table was unsuccessful.")
        if not event_query_dict['Responsible_Pitcher_For_Runner_On_2nd'] == '':
            check_insertion = event_driver.insert_player_from_event(['Responsible_Pitcher_For_Runner_On_2nd', 'idEvent'], player_driver, 
                                                                    event_query_dict, 'Responsible_Pitcher_For_Second', 'Responsible_Pitcher_For_Runner_On_2nd')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Responsible_Pitcher_For_Second table was unsuccessful.")
        if not event_query_dict['Responsible_Pitcher_For_Runner_On_3rd'] == '':
            check_insertion = event_driver.insert_player_from_event(['Responsible_Pitcher_For_Runner_On_3rd', 'idEvent'], player_driver, 
                                                                    event_query_dict, 'Responsible_Pitcher_For_Third', 'Responsible_Pitcher_For_Runner_On_3rd')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Responsible_Pitcher_For_Third table was unsuccessful.")
        if not event_query_dict['First_Runner'] == '':
            check_insertion = event_driver.insert_player_from_event(['First_Runner', 'Runner_On_1st_Dest', 'SB_Runner_On_1st_Flag', 'CS_Runner_On_1st_Flag',
                                                                    'PO_For_Runner_On_1st_Flag', 'Play_On_Runner_On_1st', 'Pinch_Runner_On_1st', 'idEvent'], player_driver, 
                                                                    event_query_dict, 'Runner_on_First_Details', 'First_Runner')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Runner_on_First_Details table was unsuccessful.")
        if not event_query_dict['Second_Runner'] == '':
            check_insertion = event_driver.insert_player_from_event(['Second_Runner', 'Runner_On_2nd_Dest', 'SB_Runner_On_2nd_Flag', 'CS_Runner_On_2nd_Flag',
                                                                    'PO_For_Runner_On_2nd_Flag', 'Play_On_Runner_On_2nd', 'Pinch_Runner_On_2nd', 'idEvent'], player_driver, 
                                                                    event_query_dict, 'Runner_on_Second_Details', 'Second_Runner')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Runner_on_Second_Details table was unsuccessful.")
        if not event_query_dict['Third_Runner'] == '':
            check_insertion = event_driver.insert_player_from_event(['Third_Runner', 'Runner_On_3rd_Dest', 'SB_Runner_On_3rd_Flag', 'CS_Runner_On_3rd_Flag',
                                                                    'PO_For_Runner_On_3rd_Flag', 'Play_On_Runner_On_3rd', 'Pinch_Runner_On_3rd', 'idEvent'], player_driver, 
                                                                    event_query_dict, 'Runner_on_Third_Details', 'Third_Runner')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Runner_on_Third_Details table was unsuccessful.")

    def __position_player_insertion(self, player_driver, event_query_dict, event_driver, db_connection):

        # Function Description: The function inserts the required content into the Positional Player tables. (i.e. 'Event_Shortstop')
        # Function Parameters: player_driver (The reference to a player driver obeck to insert the player information.)
        #     event_query_dict (The event query dictionary to store the results.),
        #     event_driver (The event driver that allows the insertion into an event related table.)
        #     db_connection (The current open connection to the database.)
        # Function Throws: UnrecognisableMySQLBehaviour (The error is thrown when the query was unsuccessful.)
        # Function Returns: Nothing

        check_insertion = event_driver.insert_player_from_event(['Shortstop', 'idEvent'], player_driver, 
                                                                event_query_dict, 'Event_Shortstop', 'Shortstop')
        if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Event_Shortstop table was unsuccessful.")
        check_insertion = event_driver.insert_player_from_event(['Right_Field', 'idEvent'], player_driver, 
                                                                event_query_dict, 'Event_Right_Field', 'Right_Field')
        if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Event_Right_Field table was unsuccessful.")
        check_insertion = event_driver.insert_player_from_event(['Center_Field', 'idEvent'], player_driver, 
                                                                event_query_dict, 'Event_Centre_Field', 'Center_Field')
        if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Event_Centre_Field table was unsuccessful.")
        check_insertion = event_driver.insert_player_from_event(['Left_Field', 'idEvent'], player_driver, 
                                                                event_query_dict, 'Event_Left_Field', 'Left_Field')
        if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Event_Left_Field table was unsuccessful.")
        check_insertion = event_driver.insert_player_from_event(['Catcher', 'idEvent'], player_driver, 
                                                                event_query_dict, 'Event_Catcher', 'Catcher')
        if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Event_Catcher table was unsuccessful.")
        check_insertion = event_driver.insert_player_from_event(['First_Base', 'idEvent'], player_driver, 
                                                                event_query_dict, 'Event_First_Base', 'First_Base')
        if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Event_First_Base table was unsuccessful.")
        check_insertion = event_driver.insert_player_from_event(['Second_Base', 'idEvent'], player_driver, 
                                                                event_query_dict, 'Event_Second_Base', 'Second_Base')
        if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Event_Second_Base table was unsuccessful.")
        check_insertion = event_driver.insert_player_from_event(['Third_Base', 'idEvent'], player_driver, 
                                                                event_query_dict, 'Event_Third_Base', 'Third_Base')
        if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Event_Third_Base table was unsuccessful.")

    def __duel_in_event_insertion_res(self, player_driver, event_query_dict, event_driver, db_connection):

        # Function Description: The function inserts the required information into the Res_Batter and Res_Pitcher tables.
        # Function Parameters: player_driver (The reference to a player driver obeck to insert the player information.)
        #     event_query_dict (The event query dictionary to store the results.),
        #     event_driver (The event driver that allows the insertion into an event related table.), 
        #     db_connection (The current open connection to the database.)
        # Function Throws: UnrecognisableMySQLBehaviour (The error is thrown when the query was unsuccessful.)
        # Function Returns: Nothing

        check_insertion = event_driver.insert_player_from_event(['Res_Batter_Name', 'Res_Batter_Hand', 'idEvent'], 
                                                                player_driver, event_query_dict, 'Res_Batter_Information', 'Res_Batter_Name')
        if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Res Batter Information table was unsuccessful.")
        check_insertion = event_driver.insert_player_from_event(['Res_Pitcher_Name', 'Res_Pitcher_Hand', 'idEvent'], 
                                                                player_driver, event_query_dict, 'Res_Pitcher_Information', 'Res_Pitcher_Name')
        if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Res Pitcher Information table was unsuccessful.")

    def __duel_in_event_insertion(self, player_driver, event_query_dict, event_driver, db_connection):

        # Function Description: The function will insert the contents into the Pitcher_In_Event and the Batter_In_Event table.
        # Function Parameters: player_driver (The reference to a player driver obeck to insert the player information.)
        #     event_query_dict (The event query dictionary to store the results.),
        #     event_driver (The event driver that allows the insertion into an event related table.), 
        #     db_connection (The current open connection to the database.)
        # Function Throws: UnrecognisableMySQLBehaviour (The error is thrown when the query was unsuccessful.)
        # Function Returns: Nothing

        check_insertion = event_driver.insert_player_from_event(['Batter_Name', 'idEvent', 'Batting_Team', 'Balls', 'Strikes', 'Batter_Hand',
                                                                'Leadoff_Flag', 'Pinch_Hit_Flag', 'Defensive_Position', 'Lineup_Position'], 
                                                                player_driver, event_query_dict, 'Batter_In_Event', 'Batter_Name')
        if not check_insertion: raise UnrecognisableMySQLBehaviour("The query into the Batter_In_Event Table was unsuccessful.")
        check_insertion = event_driver.insert_player_from_event(['Pitcher_Name', 'idEvent', 'Pitcher_Hand', 'Pitch_Sequence'], 
                                                                player_driver, event_query_dict, 'Pitcher_In_Event', 'Pitcher_Name')
        if not check_insertion: raise UnrecognisableMySQLBehaviour("The query into the Pitcher_In_Event was unsuccessful.")

    def __error_information_insertion(self, event_query_dict, event_driver, db_connection):

        # Function Description: Insert the data into the Error Information Pitcher tables. Data will only be
        #    inserted if the data exists thus making its storage dynamic. There are three tables related to pitcher errors.
        # Function Parameters: event_query_dict (The event dictionary organising the file line data.),
        #    event_driver (The event driver that allows the insertion into an event related table.), 
        #    db_connection (The existing connection to the database.)
        # Function Throws: UnrecognisableMySQLBehaviour (Throw the error if any of the queries are unexpected.)
        # Function Returns: Nothing

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
        check_game = game_driver.check_game(event_query_dict['Game_ID'])                                            # Ensure the game is inserted.
        if check_game == False: 
            check_game = game_driver.insert_game(event_query_dict['Game_ID'], event_query_dict['Visiting_Team'])    # Insert the game if it is not found.
        if check_game == False: raise UnrecognisableMySQLBehaviour("Unable to insert the game into the table after the game was not found within the table.")

    def __event_instance_insertion(self, event_query_dict, event_driver, db_connection):

        # Function Description: Handle the data insertion into the Event Instance table.
        # Function Parameters: event_query_dict (An event query dictionary.), 
        #    event_driver (The event driver that allows the insertion into an event related table.)
        # Function Throws: UnrecognisableMySQLBehaviour (Thrown when an SQL query fails in attempt to inserting data into the db.)
        # Function Returns: Nothing

        check_event = event_driver.insert_event_instance(event_query_dict)
        if (not check_event): raise UnrecognisableMySQLBehaviour("Query Failed attempting to insert into the Event_Instance table.")

    def __propogate_line_into_tables(self, file_line, player_driver, db_connection):

        # Function Description: Given a line from the text file, propogate the query throughout the entire database.
        # Function Parameters: file_line (A line from an event file.), player_driver (A reusable player driver to be used to propogate date throughout the database.), 
        #   db_connection (The connection to the database.)
        # Function Throws: Nothing
        # Function Returns: Nothing

        event_query_dict = Event_Query_Dict(file_line)
        e_q_d = event_query_dict.event_query_dict
        event_driver = Event_Driver(db_connection)                                                                            # Structure the data from the file line.
        self.__game_table_insertion(e_q_d, db_connection)                                         # Propogate into game table. 
        self.__event_instance_insertion(e_q_d, event_driver, db_connection)                       # Propogate into the event instance table.
        self.__error_information_insertion(e_q_d, event_driver, db_connection)                    # Propogate into the error information table.
        self.__duel_in_event_insertion(player_driver, e_q_d, event_driver, db_connection)         # Propogate into the Batter and Pitcher tables.
        self.__duel_in_event_insertion_res(player_driver, e_q_d, event_driver, db_connection)     # Propogate into the Res Batter and Pitcher tables.
        self.__position_player_insertion(player_driver, e_q_d, event_driver, db_connection)       # Propogate the Players who participated in the Event.
        self.__base_runner_insertion(player_driver, e_q_d, event_driver, db_connection)

    def process_event_files(self):

        # Function Description: The function will be the driver of the data insertion process. Assume we will possess 
        #   unzipped event files that are to be processed and insert into the database.
        # Function Parameters: Nothing
        # Function Throws: Nothing
        # Function Returns: Nothing
        #player_driver = Player_Driver(self.conn, self.path_to_player_list, player_reference)                # Let us only create this once to avoid needless File I/O processing.

        path_to_event_files = self.path_to_raw_data / '1990_2019_Event_Files'
        with open(self.path_to_pickle_player_data, 'rb') as pickle_file: player_reference = load(pickle_file)
        player_driver = Player_Driver(self.conn, self.path_to_player_list, player_reference)                # Let us only create this once to avoid needless File I/O processing.
        for file_name in listdir(path_to_event_files):
            count = 0    # TEMP: Delete Me
            if not file_name.endswith('.txt'): raise ValueError("There should only be .txt files in this folder. The file processed was {}.".format(file_name))
            event_file = open(path_to_event_files / file_name, 'r') 
            for file_line in event_file:                                # Processes each file line by line.
                self.__propogate_line_into_tables(file_line, player_driver, self.conn)
                count += 1
                if count > 10:
                    print(file_line)
                    break  # STOP AT 10 LINE
            event_file.close()
        print("FIN")

def clear_tables():     # Temporary Function to Delete Table Content
    db_connection = pymysql.connect(host="localhost", user="root", passwd="praquplDop#odlg73h?c", db="baseball_stats_db")       # The path to the pymysql connector to access the database.
    cursor = db_connection.cursor()
    cursor.execute('DELETE From event_instance;')           # Event_Instance (29 / 29)
    cursor.execute('DELETE From game_day;')                 # Game_Day (5)
    cursor.execute('DELETE From error_information;')        # Error Information (Possible 6)
    cursor.execute('DELETE From player_information')        # Player Information (4 / 4)
    cursor.execute('DELETE From batter_in_event')           # Batter_In_Event (10 / 10)
    cursor.execute('DELETE From pitcher_in_event')          # Pitcher_In_Event (4 / 4)
    cursor.execute('DELETE From res_batter_information')    # Res_Batter_Information (3 / 3)
    cursor.execute('DELETE From res_pitcher_information')   # Res_Pitcher_Information (3 / 3)
    cursor.execute('DELETE From event_shortstop')           # Event_Shortstop (2 / 2)
    cursor.execute('DELETE From event_right_field')         # event_right_field (2 / 2)
    cursor.execute('DELETE From event_centre_field')        # event_centre_field (2 / 2)
    cursor.execute('DELETE From event_left_field')          # event_left_field (2 / 2)
    cursor.execute('DELETE From event_catcher')             # event_catcher (2 / 2)
    cursor.execute('DELETE From event_first_base')          # event_first_base (2 / 2)
    cursor.execute('DELETE From event_second_base')         # event_second_base (2 / 2)
    cursor.execute('DELETE From event_third_base')                 # event_third_base (2 / 2)
    cursor.execute('DELETE From Responsible_Pitcher_For_First')    # Responsible_Pitcher_For_First (2 / 2)
    cursor.execute('DELETE From Responsible_Pitcher_For_Second')   # Responsible_Pitcher_For_Second (2 / 2)
    cursor.execute('DELETE From Responsible_Pitcher_For_Third')    # Responsible_Pitcher_For_Third (2 / 2)
    cursor.execute('DELETE From Runner_on_First_Details')          # runner_on_first_details (8 / 8)
    cursor.execute('DELETE From Runner_on_Second_Details')         # runner_on_second_details (8 / 8)
    cursor.execute('DELETE From Runner_on_Third_Details')          # runner_on_third_details (8 / 8)
    cursor.execute('DELETE From pinch_runner_removed_1st')
    cursor.execute('DELETE From pinch_runner_removed_2nd') 
    cursor.execute('DELETE From pinch_runner_removed_3rd') 
    cursor.execute('DELETE From batter_removed_for_pinch_hitter') 
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
