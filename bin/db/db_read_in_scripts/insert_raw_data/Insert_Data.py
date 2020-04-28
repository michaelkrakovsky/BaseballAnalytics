# Program Description: Insert all the players (pitchers and positional) and event information into the database.
# Date: April 3, 2019
# Author: Michael Krakovsky
# Version: 1.0

# Author's Notes: This problem is both interesting and challenging because we are confronted with a dependecy issue. We are required to insert 
# the player information prior to the event information; however, we are unable to discern between the type of player. One solution would be
# to insert the data synchronously where the ID is checked in a defined dictionary prior to being inserted. Whenever ID is to be inserted, 
# (either as a positional player or pitcher), the ID prescence will be confirmed. Without proper confirmation, the ID will be inserted into the database.

from pathlib import Path
from os import listdir, path
from Driver_Exceptions import UnrecognisableMySQLBehaviour
from Driver import Driver
from Player import Player_Driver
from Event import Event_Query_Dict, Event_Driver
from Game import Game_Driver
from pickle import load                               # Provide pickle capabilities
import pymysql.cursors                                # To Connect to MySQL Database (PyMySQL)
from time import strftime, gmtime

class Insert_Driver(Driver):

    def __init__(self, db_connection):

        # Class Description: The class will manage and control the data insertions into the baseball database. Note, 
        #   the class does not perform any queries. The queries are delegated to the specific drivers.

        Driver.__init__(self, db_connection)                                                          # The path to the pymysql connector to access the database.
        self.path_to_raw_data = Path("BaseballAnalytics/bin/db/raw_data/")                            # The path to the raw data that will be inserted into the database.
        self.path_to_player_list = self.path_to_raw_data / 'rosters'                                  # The folder containing the player data.
        self.path_to_pickle_player_data = self.path_to_player_list / 'pickle_player_data.pickle'      # The path to the pickle file containing the player information. 
        self.log_folder = Path('BaseballAnalytics/logs/insert_file_logs/')                            # The path to the log file.
        self.path_to_raw_data = Path('C:/Users/micha/Desktop/')
        self.log_file = self.__initiate_log_file(self.log_folder)

    def __initiate_log_file(self, path_to_folder):

        # Function Description: The function will create the log file to store the failed queries from the event files.
        # Function Parameters: path_to_folder (The path to the location of all the error files.)
        # Function Throws: Nothing
        # Function Returns: path_to_log_file (The path to the log file.)

        log_file_name = strftime("%Y-%m-%d_%H_%M_%S", gmtime()) + '.txt'
        path_to_log_file = path_to_folder / log_file_name
        with open(path_to_log_file.absolute(), 'w+') as f: f.write("Starting the file read... \n")
        return path_to_log_file

    def __empty_tables(self):

        # Function Description: The function will empty the entire database of all data.
        # Function Parameters: Nothing
        # Function Throws: Nothing
        # Function Returns: Nothing

        cursor = self.__db_connection__.cursor()
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
        cursor.execute('DELETE From event_third_base')                  # event_third_base (2 / 2)
        cursor.execute('DELETE From Responsible_Pitcher_For_First')     # Responsible_Pitcher_For_First (2 / 2)
        cursor.execute('DELETE From Responsible_Pitcher_For_Second')    # Responsible_Pitcher_For_Second (2 / 2)
        cursor.execute('DELETE From Responsible_Pitcher_For_Third')     # Responsible_Pitcher_For_Third (2 / 2)
        cursor.execute('DELETE From Runner_on_First_Details')           # runner_on_first_details (8 / 8)
        cursor.execute('DELETE From Runner_on_Second_Details')          # runner_on_second_details (8 / 8)
        cursor.execute('DELETE From Runner_on_Third_Details')           # runner_on_third_details (8 / 8)
        cursor.execute('DELETE From pinch_runner_removed_1st')          # pinch_runner_removed_1st (2 / 2)
        cursor.execute('DELETE From pinch_runner_removed_2nd')          # pinch_runner_removed_2nd (2 / 2)
        cursor.execute('DELETE From pinch_runner_removed_3rd')          # pinch_runner_removed_3rd (2 / 2)
        cursor.execute('DELETE From batter_removed_for_pinch_hitter')   # position_of_batter_for_pinch_hitter (3 / 3)
        cursor.execute('DELETE From fielder_assist_information')        # fielder_assist_information (3 / 3)
        cursor.execute('DELETE From fielder_putout_information')        # fielder_putout_information (3 / 3)
        self.__db_connection__.commit()
        cursor.close() 

    def __assist_insertions(self, event_query_dict, event_driver, db_connection):

        # Function Description: Insert the data into the Assist Tables. Data will only be
        #    inserted if the data exists thus making its storage dynamic.
        # Function Parameters: event_query_dict (The event dictionary organising the file line data.),
        #    event_driver (The event driver that allows the insertion into an event related table.), 
        #    db_connection (The existing connection to the database.)
        # Function Throws: UnrecognisableMySQLBehaviour (Throw the error if any of the queries are unexpected.)
        # Function Returns: Nothing

        event_status = False                                                        # Anything other than 0 indicates that a Assist was incurred.
        if int(event_query_dict['Fielder_With_First_Assist']) != 0:                 # Stop propogating if we get a zero.
            event_status = event_driver.insert_fielding_instance(event_query_dict['idEvent'], event_query_dict['Fielder_With_First_Assist'], 1, 'Fielder_Assist_Information')
            if not event_status: raise UnrecognisableMySQLBehaviour("The First Assist was incorrectly inserted.")
            if int(event_query_dict['Fielder_With_Second_Assist']) != 0:
                event_status = event_driver.insert_fielding_instance(event_query_dict['idEvent'], event_query_dict['Fielder_With_Second_Assist'], 2, 'Fielder_Assist_Information')
                if not event_status: raise UnrecognisableMySQLBehaviour("The Second Assist was incorrectly inserted.")
                if int(event_query_dict['Fielder_With_Third_Assist']) != 0: 
                    event_status = event_driver.insert_fielding_instance(event_query_dict['idEvent'], event_query_dict['Fielder_With_Third_Assist'], 3, 'Fielder_Assist_Information')
                    if not event_status: raise UnrecognisableMySQLBehaviour("The Third Assist was incorrectly inserted.")
                    if int(event_query_dict['Fielder_With_Fourth_Assist']) != 0: 
                        event_status = event_driver.insert_fielding_instance(event_query_dict['idEvent'], event_query_dict['Fielder_With_Fourth_Assist'], 4, 'Fielder_Assist_Information')
                        if not event_status: raise UnrecognisableMySQLBehaviour("The Fourth Assist was incorrectly inserted.")
                        if int(event_query_dict['Fielder_With_Fifth_Assist']) != 0: 
                            event_status = event_driver.insert_fielding_instance(event_query_dict['idEvent'], event_query_dict['Fielder_With_Fifth_Assist'], 5, 'Fielder_Assist_Information')
                            if not event_status: raise UnrecognisableMySQLBehaviour("The Fifth Assist was incorrectly inserted.")

    def __putout_insertions(self, event_query_dict, event_driver, db_connection):

        # Function Description: Insert the data into the Putout Tables. Data will only be
        #    inserted if the data exists thus making its storage dynamic.
        # Function Parameters: event_query_dict (The event dictionary organising the file line data.),
        #    event_driver (The event driver that allows the insertion into an event related table.), 
        #    db_connection (The existing connection to the database.)
        # Function Throws: UnrecognisableMySQLBehaviour (Throw the error if any of the queries are unexpected.)
        # Function Returns: Nothing

        event_status = False                                                        # Anything other than 0 indicates that a Putout was incurred.
        if int(event_query_dict['Fielder_With_First_Putout']) != 0:                 # Stop propogating if we get a zero.
            event_status = event_driver.insert_fielding_instance(event_query_dict['idEvent'], event_query_dict['Fielder_With_First_Putout'], 1, 'Fielder_Putout_Information')
            if not event_status: raise UnrecognisableMySQLBehaviour("The First Putout was incorrectly inserted.")
            if int(event_query_dict['Fielder_With_Second_Putout']) != 0:
                event_status = event_driver.insert_fielding_instance(event_query_dict['idEvent'], event_query_dict['Fielder_With_Second_Putout'], 2, 'Fielder_Putout_Information')
                if not event_status: raise UnrecognisableMySQLBehaviour("The Second Putout was incorrectly inserted.")
                if int(event_query_dict['Fielder_With_Third_Putout']) != 0: 
                    event_status = event_driver.insert_fielding_instance(event_query_dict['idEvent'], event_query_dict['Fielder_With_Third_Putout'], 3, 'Fielder_Putout_Information')
                    if not event_status: raise UnrecognisableMySQLBehaviour("The Third Putout was incorrectly inserted.")

    def __pinch_related_insertions(self, player_driver, event_query_dict, event_driver, db_connection):

        # Function Description: Insert the contents related to the pinch hitters and runners. (Resp Pitchers, Runners On)
        # Function Parameters: player_driver (The reference to a player driver obeck to insert the player information.)
        #     event_query_dict (The event query dictionary to store the results.),
        #     event_driver (The event driver that allows the insertion into an event related table.)
        #     db_connection (The current open connection to the database.)
        # Function Throws: UnrecognisableMySQLBehaviour (The error is thrown when the query was incorrectly inserted.)
        # Function Returns: Nothing

        if not event_query_dict['Runner_Removed_For_Pinch_Runner_On_1st'] == '':                                                             # Do not attempt an insertion if there is no player to insert.
            check_insertion = event_driver.insert_player_from_event(['Runner_Removed_For_Pinch_Runner_On_1st', 'idEvent'], player_driver, 
                                                                    event_query_dict, 'Pinch_Runner_Removed_1st', 'Runner_Removed_For_Pinch_Runner_On_1st')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Pinch_Runner_Removed_1st table was unsuccessful.")
        if not event_query_dict['Runner_Removed_For_Pinch_Runner_On_2nd'] == '':
            check_insertion = event_driver.insert_player_from_event(['Runner_Removed_For_Pinch_Runner_On_2nd', 'idEvent'], player_driver, 
                                                                event_query_dict, 'Pinch_Runner_Removed_2nd', 'Runner_Removed_For_Pinch_Runner_On_2nd')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Pinch_Runner_Removed_2nd table was unsuccessful.")
        if not event_query_dict['Runner_Removed_For_Pinch_Runner_On_3rd'] == '':
            check_insertion = event_driver.insert_player_from_event(['Runner_Removed_For_Pinch_Runner_On_3rd', 'idEvent'], player_driver, 
                                                                event_query_dict, 'Pinch_Runner_Removed_3rd', 'Runner_Removed_For_Pinch_Runner_On_3rd')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Pinch_Runner_Removed_3rd table was unsuccessful.")
        if not event_query_dict['Batter_Removed_For_Pinch_Hitter'] == '':                                                             
            check_insertion = event_driver.insert_player_from_event(['Batter_Removed_For_Pinch_Hitter', 'Position_of_Batter_removed_for_Pinch_Hitter', 'idEvent'], 
                                                                player_driver, event_query_dict, 'Batter_Removed_For_Pinch_Hitter', 'Batter_Removed_For_Pinch_Hitter')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Batter_Removed_For_Pinch_Hitter table was unsuccessful.")
            
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
        event_driver = Event_Driver(db_connection)                                                # Structure the data from the file line.
        self.__game_table_insertion(e_q_d, db_connection)                                         # Propogate into game table. 
        self.__event_instance_insertion(e_q_d, event_driver, db_connection)                       # Propogate into the event instance table.
        self.__error_information_insertion(e_q_d, event_driver, db_connection)                    # Propogate into the error information table.
        self.__duel_in_event_insertion(player_driver, e_q_d, event_driver, db_connection)         # Propogate into the Batter and Pitcher tables.
        self.__duel_in_event_insertion_res(player_driver, e_q_d, event_driver, db_connection)     # Propogate into the Res Batter and Pitcher tables.
        self.__position_player_insertion(player_driver, e_q_d, event_driver, db_connection)       # Propogate the Players who participated in the Event.
        self.__base_runner_insertion(player_driver, e_q_d, event_driver, db_connection)           # Propogate the Players who were on the Base Paths.
        self.__pinch_related_insertions(player_driver, e_q_d, event_driver, db_connection)        # Propogate the Players who were Pinch Runners & Hitters.
        self.__putout_insertions(e_q_d, event_driver, db_connection)                              # Propogate the Putout Fielders in the Event.
        self.__assist_insertions(e_q_d, event_driver, db_connection)                              # Propogate the Assist Fielders in the Event.

    def __process_event_file(self, player_driver, file_name, file_contents):

        # Function Description: The function processes the content from a single file.
        # Function Parameters: player_driver (An already accessible player driver to insert players.)
        # file_name (The name of the file.), file_contents (The contents from the event file.)
        # Function Throws: Nothing
        # Function Returns: Nothing

        error_count = 0
        for file_line in file_contents:                                                              # Processes each file line by line, record failed insertions into query file.
            try:
                self.__propogate_line_into_tables(file_line, player_driver, self.__db_connection__)
            except UnrecognisableMySQLBehaviour as err:
                self.write_into_log_file(self.log_file.absolute(), ["\n\n Name of File: {}".format(str(file_name)), 
                                        "\n The Reasoning: {}".format(str(err))])
                error_count += 1
        return error_count

    def process_event_files(self):

        # Function Description: The function will be the driver of the data insertion process. Assume we will possess 
        #   unzipped event files that are to be processed and insert into the database.
        # Function Parameters: Nothing
        # Function Throws: Nothing
        # Function Returns: Nothing
        
        path_to_event_files = self.path_to_raw_data / '1990_2019_Event_Files'
        num_files = len([name for name in listdir(path_to_event_files) if path.isfile(path.join(path_to_event_files, name))])
        self.print_progress_bar(0, num_files, prefix = 'Progress:', suffix = 'Complete', length = 50)       # Initial call to print 0% progress
        error_count = 0
        file_count = 0
        self.__empty_tables()                                                                                        # Empty out the database.
        with open(self.path_to_pickle_player_data, 'rb') as pickle_file: player_reference = load(pickle_file)
        player_driver = Player_Driver(self.__db_connection__, self.path_to_player_list, player_reference)            # Let us only create this once to avoid needless File I/O processing.
        for num, file_name in enumerate(listdir(path_to_event_files)):
            if not file_name.endswith('.txt'): raise ValueError("There should only be .txt files in this folder. The file processed was {}.".format(file_name))
            event_file = open(path_to_event_files / file_name, 'r') 
            error_count += self.__process_event_file(player_driver, path_to_event_files / file_name, event_file)
            event_file.close()
            file_count += 1
            self.print_progress_bar(num + 1, num_files, prefix = 'Progress:', suffix = 'Complete', length = 50)      # Manipulate Error Bar.
        self.write_into_log_file(self.log_file, "\n Number of Errors: {}".format(error_count))
        self.write_into_log_file(self.log_file, strftime("\n%Y-%m-%d_%H_%M_%S", gmtime()))                           # Log the ending time.

def main():

    # Function Description: Create a database connection and process event files. 

    conn = pymysql.connect(host="localhost", user="root", passwd="praquplDop#odlg73h?c", db="baseball_stats_db")         # The path to the pymysql connector to access the database.
    insert_driver = Insert_Driver(conn)
    insert_driver.process_event_files()

if __name__ == "__main__":
    main()










