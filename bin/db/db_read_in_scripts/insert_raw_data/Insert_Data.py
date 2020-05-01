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
from timeit import default_timer as timer
from Driver import Driver
from Player import Player_Driver
from Batch_Handler import Batch_Driver
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

    def __assist_insertions(self, e_q_d, event_driver):

        # Function Description: Insert the data into the Assist Tables. Data will only be
        #    inserted if the data exists thus making its storage dynamic.
        # Function Parameters: e_q_d (The event dictionary organising the file line data.),
        #    event_driver (The event driver that allows the insertion into an event related table.), 
        # Function Throws: Nothing
        # Function Returns: queries (The queries that will be inserted into the database.)

        queries = []                                                     # Anything other than 0 indicates that a Assist was incurred.
        if int(e_q_d['Fielder_With_First_Assist']) != 0:                 # Stop propogating if we get a zero.
            queries.append(event_driver.insert_fielding_instance(e_q_d['idEvent'], e_q_d['Fielder_With_First_Assist'], 1, 'Fielder_Assist_Information'))
            if int(e_q_d['Fielder_With_Second_Assist']) != 0:
                queries.append(event_driver.insert_fielding_instance(e_q_d['idEvent'], e_q_d['Fielder_With_Second_Assist'], 2, 'Fielder_Assist_Information'))
                if int(e_q_d['Fielder_With_Third_Assist']) != 0: 
                    queries.append(event_driver.insert_fielding_instance(e_q_d['idEvent'], e_q_d['Fielder_With_Third_Assist'], 3, 'Fielder_Assist_Information'))
                    if int(e_q_d['Fielder_With_Fourth_Assist']) != 0: 
                        queries.append(event_driver.insert_fielding_instance(e_q_d['idEvent'], e_q_d['Fielder_With_Fourth_Assist'], 4, 'Fielder_Assist_Information'))
                        if int(e_q_d['Fielder_With_Fifth_Assist']) != 0: 
                            queries.append(event_driver.insert_fielding_instance(e_q_d['idEvent'], e_q_d['Fielder_With_Fifth_Assist'], 5, 'Fielder_Assist_Information'))
        return queries

    def __putout_insertions(self, e_q_d, event_driver):

        # Function Description: Insert the data into the Putout Tables. Data will only be
        #    inserted if the data exists thus making its storage dynamic.
        # Function Parameters: e_q_d (The event dictionary organising the file line data.),
        #    event_driver (The event driver that allows the insertion into an event related table.), 
        # Function Throws: Nothing
        # Function Returns: queries (The queries that will be inserted into the database.)

        queries = []                                                     # Anything other than 0 indicates that a Putout was incurred.
        if int(e_q_d['Fielder_With_First_Putout']) != 0:                 # Stop propogating if we get a zero.
            queries.append(event_driver.insert_fielding_instance(e_q_d['idEvent'], e_q_d['Fielder_With_First_Putout'], 1, 'Fielder_Putout_Information'))
            if int(e_q_d['Fielder_With_Second_Putout']) != 0:
                queries.append(event_driver.insert_fielding_instance(e_q_d['idEvent'], e_q_d['Fielder_With_Second_Putout'], 2, 'Fielder_Putout_Information'))
                if int(e_q_d['Fielder_With_Third_Putout']) != 0: 
                    queries.append(event_driver.insert_fielding_instance(e_q_d['idEvent'], e_q_d['Fielder_With_Third_Putout'], 3, 'Fielder_Putout_Information'))
        return queries

    def __pinch_related_insertions(self, e_q_d):

        # Function Description: Insert the contents related to the pinch hitters and runners. (Resp Pitchers, Runners On)
        # Function Parameters: event_querye_q_d_dict (The event query dictionary to store the results.),
        #     event_driver (The event driver that allows the insertion into an event related table.)
        #     db_connection (The current open connection to the database.)
        # Function Throws: UnrecognisableMySQLBehaviour (The error is thrown when the query was incorrectly inserted.)
        # Function Returns: queries (The queries that will be inserted related to pinch related events.)

        queries = []
        if not e_q_d['Runner_Removed_For_Pinch_Runner_On_1st'] == '':                                        # Do not attempt an insertion if there is no player to insert.
            queries.append(self.create_query_string(['Runner_Removed_For_Pinch_Runner_On_1st', 'idEvent'], 
                                                    e_q_d, 'Pinch_Runner_Removed_1st'))
        if not e_q_d['Runner_Removed_For_Pinch_Runner_On_2nd'] == '':
            queries.append(self.create_query_string(['Runner_Removed_For_Pinch_Runner_On_2nd', 'idEvent'], 
                                                    e_q_d, 'Pinch_Runner_Removed_2nd'))
        if not e_q_d['Runner_Removed_For_Pinch_Runner_On_3rd'] == '':
            queries.append(self.create_query_string(['Runner_Removed_For_Pinch_Runner_On_3rd', 'idEvent'], 
                                                    e_q_d, 'Pinch_Runner_Removed_3rd'))
        if not e_q_d['Batter_Removed_For_Pinch_Hitter'] == '':                                                             
            queries.append(self.create_query_string(['Batter_Removed_For_Pinch_Hitter', 'Position_of_Batter_removed_for_Pinch_Hitter', 'idEvent'], 
                                                    e_q_d, 'Batter_Removed_For_Pinch_Hitter'))
        return queries
            
    def __base_runner_insertion(self, e_q_d):

        # Function Description: Insert the contents related to the base runners. (Resp Pitchers, Runners On)
        # Function Parameters: event_query_dict (The event query dictionary to store the results.),
        # Function Throws: UnrecognisableMySQLBehaviour (The error is thrown when the query was incorrectly inserted.)
        # Function Returns: queries( The queries that will be executed into the database.)

        queries = []
        if not e_q_d['Responsible_Pitcher_For_Runner_On_1st'] == '':                                                             # Do not attempt an insertion if there is no player to insert.
            queries.append(self.create_query_string(['Responsible_Pitcher_For_Runner_On_1st', 'idEvent'], 
                                                    e_q_d, 'Responsible_Pitcher_For_First'))
        if not e_q_d['Responsible_Pitcher_For_Runner_On_2nd'] == '':
            queries.append(self.create_query_string(['Responsible_Pitcher_For_Runner_On_2nd', 'idEvent'], 
                                                    e_q_d, 'Responsible_Pitcher_For_Second'))
        if not e_q_d['Responsible_Pitcher_For_Runner_On_3rd'] == '':
            queries.append(self.create_query_string(['Responsible_Pitcher_For_Runner_On_3rd', 'idEvent'], 
                                                    e_q_d, 'Responsible_Pitcher_For_Third'))
        if not e_q_d['First_Runner'] == '':
            queries.append(self.create_query_string(['First_Runner', 'Runner_On_1st_Dest', 'SB_Runner_On_1st_Flag', 'CS_Runner_On_1st_Flag',
                                                    'PO_For_Runner_On_1st_Flag', 'Play_On_Runner_On_1st', 'Pinch_Runner_On_1st', 'idEvent'], 
                                                    e_q_d, 'Runner_on_First_Details'))
        if not e_q_d['Second_Runner'] == '':
            queries.append(self.create_query_string(['Second_Runner', 'Runner_On_2nd_Dest', 'SB_Runner_On_2nd_Flag', 'CS_Runner_On_2nd_Flag',
                                                    'PO_For_Runner_On_2nd_Flag', 'Play_On_Runner_On_2nd', 'Pinch_Runner_On_2nd', 'idEvent'], 
                                                    e_q_d, 'Runner_on_Second_Details'))
        if not e_q_d['Third_Runner'] == '':
            queries.append(self.create_query_string(['Third_Runner', 'Runner_On_3rd_Dest', 'SB_Runner_On_3rd_Flag', 'CS_Runner_On_3rd_Flag',
                                                    'PO_For_Runner_On_3rd_Flag', 'Play_On_Runner_On_3rd', 'Pinch_Runner_On_3rd', 'idEvent'], 
                                                    e_q_d, 'Runner_on_Third_Details'))
        return queries

    def __position_player_insertion_queries(self, e_q_d):

        # Function Description: The function inserts the required content into the Positional Player tables. (i.e. 'Event_Shortstop')
        # Function Parameters: e_q_d (The event query dictionary to store the results.),
        # Function Throws: UnrecognisableMySQLBehaviour (The error is thrown when the query was unsuccessful.)
        # Function Returns: queries (The queries to insert for all the players within the event.)

        queries = []
        queries.append(self.create_query_string(['Shortstop', 'idEvent'], e_q_d, 'Event_Shortstop'))
        queries.append(self.create_query_string(['Right_Field', 'idEvent'], e_q_d, 'Event_Right_Field'))
        queries.append(self.create_query_string(['Center_Field', 'idEvent'], e_q_d, 'Event_Centre_Field'))
        queries.append(self.create_query_string(['Left_Field', 'idEvent'], e_q_d, 'Event_Left_Field'))
        queries.append(self.create_query_string(['Catcher', 'idEvent'], e_q_d, 'Event_Catcher'))
        queries.append(self.create_query_string(['First_Base', 'idEvent'], e_q_d, 'Event_First_Base'))
        queries.append(self.create_query_string(['Second_Base', 'idEvent'], e_q_d, 'Event_Second_Base'))
        queries.append(self.create_query_string(['Third_Base', 'idEvent'], e_q_d, 'Event_Third_Base'))
        return queries

    def __duel_in_event_insertion(self, e_q_d):

        # Function Description: The function will insert the contents into the Pitcher_In_Event and the Batter_In_Event table.
        # Function Parameters: e_q_d (The event query dictionary to store the results.),
        # Function Throws: UnrecognisableMySQLBehaviour (The error is thrown when the query was unsuccessful.)
        # Function Returns: Nothing

        queries = []
        queries.append(self.create_query_string(['Batter_Name', 'idEvent', 'Batting_Team', 'Balls', 'Strikes', 'Batter_Hand', 'Leadoff_Flag', 
                                                'Pinch_Hit_Flag', 'Defensive_Position', 'Lineup_Position'], e_q_d, 'Batter_In_Event'))
        queries.append(self.create_query_string(['Pitcher_Name', 'idEvent', 'Pitcher_Hand', 'Pitch_Sequence'], e_q_d, 'Pitcher_In_Event'))
        queries.append(self.create_query_string(['Res_Batter_Name', 'Res_Batter_Hand', 'idEvent'], e_q_d, 'Res_Batter_Information'))
        queries.append(self.create_query_string(['Res_Pitcher_Name', 'Res_Pitcher_Hand', 'idEvent'], e_q_d, 'Res_Pitcher_Information'))
        return queries

    def __error_information_insertion(self, e_q_d, event_driver):

        # Function Description: Insert the data into the Error Information Pitcher tables. Data will only be
        #    inserted if the data exists thus making its storage dynamic. There are three tables related to pitcher errors.
        # Function Parameters: e_q_d (The event dictionary organising the file line data.),
        #    event_driver (The event driver that allows the insertion into an event related table.), 
        # Function Throws:
        # Function Returns: queries (The queries to insert into the database.)

        queries = []                                                     # Anything other than 0 indicates that an error was incurred.
        if int(e_q_d['1st_Error_Player']) != 0:                          # Stop propogating if we get a zero.
            queries.append(event_driver.build_error_information(e_q_d['1st_Error_Player'], e_q_d['1st_Error_Type'], e_q_d['idEvent'], 1))
            if int(e_q_d['2nd_Error_Player']) != 0:
                queries.append(event_driver.build_error_information(e_q_d['2nd_Error_Player'], e_q_d['2nd_Error_Type'], e_q_d['idEvent'], 2))
                if int(e_q_d['3rd_Error_Player']) != 0: 
                    queries.append(event_driver.build_error_information(e_q_d['3rd_Error_Player'], e_q_d['3rd_Error_Type'], e_q_d['idEvent'], 3))
        return queries

    def __event_instance_insertion(self, e_q_d):

        # Function Description: Handle the data insertion into the Event Instance table.
        # Function Parameters: event_query_dict (An event query dictionary.),
        # Function Throws: Nothing
        # Function Returns: The query to insert into the event table. (Ensure it is a list as to be added properly to the query list.)

        return [self.create_query_string(['idEvent', 'Game_ID', 'Inning', 'Outs', 'Vis_Score', 'Home_Score','Event_Text', 'Event_Type', 
                                    'Batter_Event_Flag', 'AB_Flag', 'Hit_Value', 'SH_Flag', 'SF_Flag', 'Outs_on_Play', 'Double_Play_Flag', 
                                    'Triple_Play_Flag', 'RBI_On_Play', 'Wild_Pitch_Flag', 'Passed_Ball_Flag', 'Fielded_By', 'Batted_Ball_Type', 
                                    'Bunt_Flag', 'Foul_Flag', 'Hit_Location', 'Num_Errors', 'Batter_Dest', 'Play_on_Batter', 'New_Game_Flag', 
                                    'End_Game_Flag'], e_q_d, "Event_Instance")]

    def __propogate_line_into_tables(self, e_q_d, event_driver, batch_handler):

        # Function Description: Given a line from the text file, propogate the query throughout the entire database.
        # Function Parameters: e_q_d (The event query dictionary to propogate throughout the tables.), 
        #    event_driver (An existing event driver to utilise the capailitites in that package.)
        #    batch_handler (The mechanism to handle batch requests.)
        # Function Throws: Nothing
        # Function Returns: Nothing
        
        batch_handler.add_query('Event_Instance', self.__event_instance_insertion(e_q_d))                         # Propogate into the event instance table.
        batch_handler.add_query('Error_Information', self.__error_information_insertion(e_q_d, event_driver))     # Propogate into the error information table.
        batch_handler.add_query('Duel_Tables', self.__duel_in_event_insertion(e_q_d))                             # Propogate into the Batter and Pitcher tables.
        batch_handler.add_query('Positional_Players', self.__position_player_insertion_queries(e_q_d))            # Propogate the Players who participated in the Event.
        batch_handler.add_query('Base_Runners', self.__base_runner_insertion(e_q_d))                              # Propogate the Players who were on the Base Paths.
        batch_handler.add_query('Pinch_Tables', self.__pinch_related_insertions(e_q_d))                           # Propogate the Players who were Pinch Runners & Hitters.
        batch_handler.add_query('Putout_Tables', self.__putout_insertions(e_q_d, event_driver))                   # Propogate the Putout Fielders in the Event.
        batch_handler.add_query('Assist_Tables', self.__assist_insertions(e_q_d, event_driver))                   # Propogate the Assist Fielders in the Event.

    def __process_event_file(self, file_contents):

        # Function Description: The function processes the content from a single file.
        # Function Parameters: file_contents (The contents from the event file.)
        # Function Throws: Nothing
        # Function Returns: Nothing

        game_driver = Game_Driver(self.__db_connection__)
        batch_driver = Batch_Driver(self.__db_connection__, 500)
        event_driver = Event_Driver(self.__db_connection__)                                                   # Structure the data from the file line.
        previous_game_id = None
        for pos_in_file, file_line in enumerate(file_contents):                                               # Processes each file line by line, record failed insertions into query file.
            e_q_d = Event_Query_Dict(file_line, pos_in_file)
            if previous_game_id != e_q_d.event_query_dict['Game_ID']:                                         # Insert a new game if necessary.
                batch_driver.add_query('Game_Day', game_driver.insert_game(e_q_d.event_query_dict['Game_ID'], e_q_d.event_query_dict['Visiting_Team']))
                previous_game_id = e_q_d.event_query_dict['Game_ID']
            self.__propogate_line_into_tables(e_q_d.event_query_dict, event_driver, batch_driver)
        batch_driver.empty_batch_driver()             # Empty the remaining batch driver as not to lose the queued queries.

    def process_event_files(self):

        # Function Description: The function will be the driver of the data insertion process. Assume we will possess 
        #   unzipped event files that are to be processed and insert into the database.
        # Function Parameters: Nothing
        # Function Throws: Nothing
        # Function Returns: Nothing
        
        path_to_event_files = self.path_to_raw_data / '1990_2019_Event_Files'
        num_files = len([name for name in listdir(path_to_event_files) if path.isfile(path.join(path_to_event_files, name))])
        self.__empty_tables()                                                                               # Empty out the database.
        start = timer()
        player_driver = self.__initiate_player_driver()                                                     
        player_driver.player_batch_insertion()                                                              # Insert all the players to forgoe the need for checks.
        
        print("Beginning Event file Insertion.")
        self.print_progress_bar(0, num_files, prefix = 'Progress:', suffix = 'Complete', length = 50)       # Initial call to print 0% progress
        for num, file_name in enumerate(listdir(path_to_event_files)):
            break
            if not file_name.endswith('.txt'): raise ValueError("There should only be .txt files in this folder. The file processed was {}.".format(file_name))
            event_file = open(path_to_event_files / file_name, 'r') 
            self.__process_event_file(event_file)
            event_file.close()
            self.print_progress_bar(num + 1, num_files, prefix = 'Progress:', suffix = 'Complete', length = 50)      # Manipulate Error Bar.
        self.write_into_log_file(self.log_file, strftime("\n%Y-%m-%d_%H_%M_%S", gmtime()))                           # Log the ending time.
        end = timer()
        print("Total time was: " + str(end - start))

def main():

    # Function Description: Create a database connection and process event files. 

    conn = pymysql.connect(host="localhost", user="root", passwd="praquplDop#odlg73h?c", db="baseball_stats_db")         # The path to the pymysql connector to access the database.
    insert_driver = Insert_Driver(conn)
    insert_driver.process_event_files()

if __name__ == "__main__":
    main()










