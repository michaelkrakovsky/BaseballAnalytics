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

    def __initiate_player_driver(self):

        # Function Description: Intitiate the player driver used throughout the entire propogation process.
        # Function Parameters: Nothing
        # Function Throws: Nothing
        # Function Returns: The instantiated player driver.

        try:                                                                                                         # Attempt to pickle file. Else, create your own pickle.        
            with open(self.path_to_pickle_player_data, 'rb') as pickle_file: player_reference = load(pickle_file)
            return Player_Driver(self.__db_connection__, self.path_to_player_list, player_reference)
        except FileNotFoundError:
            return Player_Driver(self.__db_connection__, self.path_to_player_list)

    def __initiate_log_file(self, path_to_folder):

        # Function Description: The function will create the log file to store the failed queries from the event files.
        # Function Parameters: path_to_folder (The path to the location of all the error files.)
        # Function Throws: Nothing
        # Function Returns: path_to_log_file (The path to the log file.)

        log_file_name = strftime("%Y-%m-%d_%H_%M_%S", gmtime()) + '.txt'
        path_to_log_file = path_to_folder / log_file_name
        with open(path_to_log_file.absolute(), 'w+') as f: f.write("Starting the file read... \n")
        return path_to_log_file

    def __empty_tables(self, empty_players=False):

        # Function Description: The function will empty the entire database of all data.
        # Function Parameters: empty_players (Decide whether to empty to content from the players table.)
        # Function Throws: Nothing
        # Function Returns: Nothing

        cursor = self.__db_connection__.cursor()
        cursor.execute('DELETE From event_instance;')           # Event_Instance (29 / 29)
        cursor.execute('DELETE From game_day;')                 # Game_Day (5)
        cursor.execute('DELETE From error_information;')        # Error Information (Possible 6)
        if empty_players: cursor.execute('DELETE From player_information')        # Player Information (4 / 4)
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

    def __pinch_related_insertions(self, event_query_dict, event_driver, db_connection):

        # Function Description: Insert the contents related to the pinch hitters and runners. (Resp Pitchers, Runners On)
        # Function Parameters: event_query_dict (The event query dictionary to store the results.),
        #     event_driver (The event driver that allows the insertion into an event related table.)
        #     db_connection (The current open connection to the database.)
        # Function Throws: UnrecognisableMySQLBehaviour (The error is thrown when the query was incorrectly inserted.)
        # Function Returns: Nothing

        if not event_query_dict['Runner_Removed_For_Pinch_Runner_On_1st'] == '':                                                             # Do not attempt an insertion if there is no player to insert.
            check_insertion = event_driver.insert_event_dynamic(['Runner_Removed_For_Pinch_Runner_On_1st', 'idEvent'], 
                                                                    event_query_dict, 'Pinch_Runner_Removed_1st')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Pinch_Runner_Removed_1st table was unsuccessful.")
        if not event_query_dict['Runner_Removed_For_Pinch_Runner_On_2nd'] == '':
            check_insertion = event_driver.insert_event_dynamic(['Runner_Removed_For_Pinch_Runner_On_2nd', 'idEvent'], 
                                                                event_query_dict, 'Pinch_Runner_Removed_2nd')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Pinch_Runner_Removed_2nd table was unsuccessful.")
        if not event_query_dict['Runner_Removed_For_Pinch_Runner_On_3rd'] == '':
            check_insertion = event_driver.insert_event_dynamic(['Runner_Removed_For_Pinch_Runner_On_3rd', 'idEvent'], 
                                                                event_query_dict, 'Pinch_Runner_Removed_3rd')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Pinch_Runner_Removed_3rd table was unsuccessful.")
        if not event_query_dict['Batter_Removed_For_Pinch_Hitter'] == '':                                                             
            check_insertion = event_driver.insert_event_dynamic(['Batter_Removed_For_Pinch_Hitter', 'Position_of_Batter_removed_for_Pinch_Hitter', 'idEvent'], 
                                                                event_query_dict, 'Batter_Removed_For_Pinch_Hitter')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Batter_Removed_For_Pinch_Hitter table was unsuccessful.")
            
    def __base_runner_insertion(self, event_query_dict, event_driver, db_connection):

        # Function Description: Insert the contents related to the base runners. (Resp Pitchers, Runners On)
        # Function Parameters: event_query_dict (The event query dictionary to store the results.),
        #     event_driver (The event driver that allows the insertion into an event related table.)
        #     db_connection (The current open connection to the database.)
        # Function Throws: UnrecognisableMySQLBehaviour (The error is thrown when the query was incorrectly inserted.)
        # Function Returns: Nothing

        if not event_query_dict['Responsible_Pitcher_For_Runner_On_1st'] == '':                                                             # Do not attempt an insertion if there is no player to insert.
            check_insertion = event_driver.insert_event_dynamic(['Responsible_Pitcher_For_Runner_On_1st', 'idEvent'], 
                                                                event_query_dict, 'Responsible_Pitcher_For_First')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Responsible_Pitcher_For_First table was unsuccessful.")
        if not event_query_dict['Responsible_Pitcher_For_Runner_On_2nd'] == '':
            check_insertion = event_driver.insert_event_dynamic(['Responsible_Pitcher_For_Runner_On_2nd', 'idEvent'], 
                                                                event_query_dict, 'Responsible_Pitcher_For_Second')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Responsible_Pitcher_For_Second table was unsuccessful.")
        if not event_query_dict['Responsible_Pitcher_For_Runner_On_3rd'] == '':
            check_insertion = event_driver.insert_event_dynamic(['Responsible_Pitcher_For_Runner_On_3rd', 'idEvent'], 
                                                                event_query_dict, 'Responsible_Pitcher_For_Third')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Responsible_Pitcher_For_Third table was unsuccessful.")
        if not event_query_dict['First_Runner'] == '':
            check_insertion = event_driver.insert_event_dynamic(['First_Runner', 'Runner_On_1st_Dest', 'SB_Runner_On_1st_Flag', 'CS_Runner_On_1st_Flag',
                                                                'PO_For_Runner_On_1st_Flag', 'Play_On_Runner_On_1st', 'Pinch_Runner_On_1st', 'idEvent'], 
                                                                event_query_dict, 'Runner_on_First_Details')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Runner_on_First_Details table was unsuccessful.")
        if not event_query_dict['Second_Runner'] == '':
            check_insertion = event_driver.insert_event_dynamic(['Second_Runner', 'Runner_On_2nd_Dest', 'SB_Runner_On_2nd_Flag', 'CS_Runner_On_2nd_Flag',
                                                                'PO_For_Runner_On_2nd_Flag', 'Play_On_Runner_On_2nd', 'Pinch_Runner_On_2nd', 'idEvent'], 
                                                                event_query_dict, 'Runner_on_Second_Details')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Runner_on_Second_Details table was unsuccessful.")
        if not event_query_dict['Third_Runner'] == '':
            check_insertion = event_driver.insert_event_dynamic(['Third_Runner', 'Runner_On_3rd_Dest', 'SB_Runner_On_3rd_Flag', 'CS_Runner_On_3rd_Flag',
                                                                'PO_For_Runner_On_3rd_Flag', 'Play_On_Runner_On_3rd', 'Pinch_Runner_On_3rd', 'idEvent'], 
                                                                event_query_dict, 'Runner_on_Third_Details')
            if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Runner_on_Third_Details table was unsuccessful.")

    def __position_player_insertion(self, e_q_d, event_driver, db_connection):

        # Function Description: The function inserts the required content into the Positional Player tables. (i.e. 'Event_Shortstop')
        # Function Parameters: e_q_d (The event query dictionary to store the results.),
        #     event_driver (The event driver that allows the insertion into an event related table.)
        #     db_connection (The current open connection to the database.)
        # Function Throws: UnrecognisableMySQLBehaviour (The error is thrown when the query was unsuccessful.)
        # Function Returns: Nothing

        check_query = event_driver.insert_event_dynamic(['Shortstop', 'idEvent'], e_q_d, 'Event_Shortstop')
        if not check_query: raise UnrecognisableMySQLBehaviour("Failed Attempt to insert the Shortstop.")
        check_query = event_driver.insert_event_dynamic(['Right_Field', 'idEvent'], e_q_d, 'Event_Right_Field')
        if not check_query: raise UnrecognisableMySQLBehaviour("Failed Attempt to insert the RF.")
        check_query = event_driver.insert_event_dynamic(['Center_Field', 'idEvent'], e_q_d, 'Event_Centre_Field')
        if not check_query: raise UnrecognisableMySQLBehaviour("Failed Attempt to insert the CF.")
        check_query = event_driver.insert_event_dynamic(['Left_Field', 'idEvent'], e_q_d, 'Event_Left_Field')
        if not check_query: raise UnrecognisableMySQLBehaviour("Failed Attempt to insert the LF.")
        check_query = event_driver.insert_event_dynamic(['Catcher', 'idEvent'], e_q_d, 'Event_Catcher')
        if not check_query: raise UnrecognisableMySQLBehaviour("Failed Attempt to insert the Catcher.")
        check_query = event_driver.insert_event_dynamic(['First_Base', 'idEvent'], e_q_d, 'Event_First_Base')
        if not check_query: raise UnrecognisableMySQLBehaviour("Failed Attempt to insert the First Base.")
        check_query = event_driver.insert_event_dynamic(['Second_Base', 'idEvent'], e_q_d, 'Event_Second_Base')
        if not check_query: raise UnrecognisableMySQLBehaviour("Failed Attempt to insert the Second Base.")
        check_query = event_driver.insert_event_dynamic(['Third_Base', 'idEvent'], e_q_d, 'Event_Third_Base')
        if not check_query: raise UnrecognisableMySQLBehaviour("Failed Attempt to insert the Third Base.")

    def __position_player_insertion_temp(self, e_q_d, event_driver, db_connection):

        # Function Description: The function inserts the required content into the Positional Player tables. (i.e. 'Event_Shortstop')
        # Function Parameters: e_q_d (The event query dictionary to store the results.),
        #     event_driver (The event driver that allows the insertion into an event related table.)
        #     db_connection (The current open connection to the database.)
        # Function Throws: UnrecognisableMySQLBehaviour (The error is thrown when the query was unsuccessful.)
        # Function Returns: Nothing

        queries = []
        queries.append(self.create_query_string(['Shortstop', 'idEvent'], e_q_d, 'Event_Shortstop'))
        queries.append(self.create_query_string(['Right_Field', 'idEvent'], e_q_d, 'Event_Right_Field'))
        queries.append(self.create_query_string(['Center_Field', 'idEvent'], e_q_d, 'Event_Centre_Field'))
        queries.append(self.create_query_string(['Left_Field', 'idEvent'], e_q_d, 'Event_Left_Field'))
        queries.append(self.create_query_string(['Catcher', 'idEvent'], e_q_d, 'Event_Catcher'))
        queries.append(self.create_query_string(['First_Base', 'idEvent'], e_q_d, 'Event_First_Base'))
        queries.append(self.create_query_string(['Second_Base', 'idEvent'], e_q_d, 'Event_Second_Base'))
        queries.append(self.create_query_string(['Third_Base', 'idEvent'], e_q_d, 'Event_Third_Base'))
        check_status = self.execute_queries(queries)
        if not check_status: raise UnrecognisableMySQLBehaviour("A player was incorrectly inserted.")

    def __duel_in_event_insertion_res(self, event_query_dict, event_driver, db_connection):

        # Function Description: The function inserts the required information into the Res_Batter and Res_Pitcher tables.
        # Function Parameters: event_query_dict (The event query dictionary to store the results.),
        #     event_driver (The event driver that allows the insertion into an event related table.), 
        #     db_connection (The current open connection to the database.)
        # Function Throws: UnrecognisableMySQLBehaviour (The error is thrown when the query was unsuccessful.)
        # Function Returns: Nothing

        check_insertion = event_driver.insert_event_dynamic(['Res_Batter_Name', 'Res_Batter_Hand', 'idEvent'], 
                                                            event_query_dict, 'Res_Batter_Information')
        if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Res Batter Information table was unsuccessful.")
        check_insertion = event_driver.insert_event_dynamic(['Res_Pitcher_Name', 'Res_Pitcher_Hand', 'idEvent'], 
                                                            event_query_dict, 'Res_Pitcher_Information')
        if not check_insertion: raise UnrecognisableMySQLBehaviour("The insertion into the Res Pitcher Information table was unsuccessful.")

    def __duel_in_event_insertion(self, event_query_dict, event_driver, db_connection):

        # Function Description: The function will insert the contents into the Pitcher_In_Event and the Batter_In_Event table.
        # Function Parameters: event_query_dict (The event query dictionary to store the results.),
        #     event_driver (The event driver that allows the insertion into an event related table.), 
        #     db_connection (The current open connection to the database.)
        # Function Throws: UnrecognisableMySQLBehaviour (The error is thrown when the query was unsuccessful.)
        # Function Returns: Nothing

        check_insertion = event_driver.insert_event_dynamic(['Batter_Name', 'idEvent', 'Batting_Team', 'Balls', 'Strikes', 'Batter_Hand',
                                                            'Leadoff_Flag', 'Pinch_Hit_Flag', 'Defensive_Position', 'Lineup_Position'], 
                                                            event_query_dict, 'Batter_In_Event')
        if not check_insertion: raise UnrecognisableMySQLBehaviour("The query into the Batter_In_Event Table was unsuccessful.")
        check_insertion = event_driver.insert_event_dynamic(['Pitcher_Name', 'idEvent', 'Pitcher_Hand', 'Pitch_Sequence'], 
                                                            event_query_dict, 'Pitcher_In_Event')
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
        check_game = game_driver.insert_game(event_query_dict['Game_ID'], event_query_dict['Visiting_Team'])           # Insert the game if it is not found.
        if check_game == False: raise UnrecognisableMySQLBehaviour("Unable to insert the game into the table after the game was not found within the table.")

    def __event_instance_insertion(self, event_query_dict, event_driver, db_connection):

        # Function Description: Handle the data insertion into the Event Instance table.
        # Function Parameters: event_query_dict (An event query dictionary.), 
        #    event_driver (The event driver that allows the insertion into an event related table.)
        # Function Throws: UnrecognisableMySQLBehaviour (Thrown when an SQL query fails in attempt to inserting data into the db.)
        # Function Returns: Nothing

        check_event = event_driver.insert_event_instance(event_query_dict)
        if (not check_event): raise UnrecognisableMySQLBehaviour("Query Failed attempting to insert into the Event_Instance table.")

    def __propogate_line_into_tables(self, e_q_d, event_driver, db_connection):

        # Function Description: Given a line from the text file, propogate the query throughout the entire database.
        # Function Parameters: e_q_d (The event query dictionary to propogate throughout the tables.), 
        #    event_driver (An existing event driver to utilise the capailitites in that package.)
        #    db_connection (The connection to the database.)
        # Function Throws: Nothing
        # Function Returns: Nothing
        
        self.__event_instance_insertion(e_q_d, event_driver, db_connection)                       # Propogate into the event instance table.
        self.__error_information_insertion(e_q_d, event_driver, db_connection)                    # Propogate into the error information table.
        self.__duel_in_event_insertion(e_q_d, event_driver, db_connection)                        # Propogate into the Batter and Pitcher tables.
        self.__duel_in_event_insertion_res(e_q_d, event_driver, db_connection)                    # Propogate into the Res Batter and Pitcher tables.
        start = timer()
        self.__position_player_insertion_temp(e_q_d, event_driver, db_connection)                      # Propogate the Players who participated in the Event.
        #self.__position_player_insertion(e_q_d, event_driver, db_connection)                      # Propogate the Players who participated in the Event.
        end = timer()
        print(end - start)
        self.__base_runner_insertion(e_q_d, event_driver, db_connection)                          # Propogate the Players who were on the Base Paths.
        self.__pinch_related_insertions(e_q_d, event_driver, db_connection)                       # Propogate the Players who were Pinch Runners & Hitters.
        self.__putout_insertions(e_q_d, event_driver, db_connection)                              # Propogate the Putout Fielders in the Event.
        self.__assist_insertions(e_q_d, event_driver, db_connection)                              # Propogate the Assist Fielders in the Event.

    def __process_event_file(self, file_name, file_contents):

        # Function Description: The function processes the content from a single file.
        # Function Parameters: file_name (The name of the file.), file_contents (The contents from the event file.)
        # Function Throws: Nothing
        # Function Returns: Nothing

        error_count = 0
        i = 0
        event_driver = Event_Driver(self.__db_connection__)                                                   # Structure the data from the file line.
        previous_game_id = None
        for pos_in_file, file_line in enumerate(file_contents):                                               # Processes each file line by line, record failed insertions into query file.
            e_q_d = Event_Query_Dict(file_line, pos_in_file)
            if previous_game_id != e_q_d.event_query_dict['Game_ID']:                                         # Check whether to propogate into the game table.
                self.__game_table_insertion(e_q_d.event_query_dict, self.__db_connection__)                           
            previous_game_id = e_q_d.event_query_dict['Game_ID']
            try:
                self.__propogate_line_into_tables(e_q_d.event_query_dict, event_driver, self.__db_connection__)
            except UnrecognisableMySQLBehaviour as err:
                self.write_into_log_file(self.log_file.absolute(), ["\n\n Name of File: {}".format(str(file_name)), 
                                        "\n The Reasoning: {}".format(str(err))])
                error_count += 1
            i += 1
            if i > 10: break
        return error_count

    def process_event_files(self):

        # Function Description: The function will be the driver of the data insertion process. Assume we will possess 
        #   unzipped event files that are to be processed and insert into the database.
        # Function Parameters: Nothing
        # Function Throws: Nothing
        # Function Returns: Nothing
        
        path_to_event_files = self.path_to_raw_data / '1990_2019_Event_Files'
        num_files = len([name for name in listdir(path_to_event_files) if path.isfile(path.join(path_to_event_files, name))])
        error_count = 0
        file_count = 0
        self.__empty_tables()                                                                               # Empty out the database.
        #player_driver = self.__initiate_player_driver()                                                     
        #player_driver.player_batch_insertion()                                                              # Insert all the players to forgoe the need for checks.
        start = timer()
        print("Beginning Event file Insertion.")
        self.print_progress_bar(0, num_files, prefix = 'Progress:', suffix = 'Complete', length = 50)       # Initial call to print 0% progress
        for num, file_name in enumerate(listdir(path_to_event_files)):
            if not file_name.endswith('.txt'): raise ValueError("There should only be .txt files in this folder. The file processed was {}.".format(file_name))
            event_file = open(path_to_event_files / file_name, 'r') 
            error_count += self.__process_event_file(path_to_event_files / file_name, event_file)
            event_file.close()
            file_count += 1
            self.print_progress_bar(num + 1, num_files, prefix = 'Progress:', suffix = 'Complete', length = 50)      # Manipulate Error Bar.
            break
        self.write_into_log_file(self.log_file, "\n Number of Errors: {}".format(error_count))
        self.write_into_log_file(self.log_file, strftime("\n%Y-%m-%d_%H_%M_%S", gmtime()))                           # Log the ending time.
        end = timer()
        print(end - start)

from timeit import default_timer as timer

def main():

    # Function Description: Create a database connection and process event files. 

    conn = pymysql.connect(host="localhost", user="root", passwd="praquplDop#odlg73h?c", db="baseball_stats_db")         # The path to the pymysql connector to access the database.
    insert_driver = Insert_Driver(conn)
    insert_driver.process_event_files()

if __name__ == "__main__":
    main()










