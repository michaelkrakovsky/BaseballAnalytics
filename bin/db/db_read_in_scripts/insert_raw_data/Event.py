# Program Description: All the function to insert a player into the database.
# Date: April 23, 2019
# Author: Michael Krakovsky
# Version: 1.0

from hashlib import sha224
from Driver import Driver
from Player import Player_Driver
from Game import Game_Driver
from Driver_Exceptions import UnrecognisableMySQLBehaviour

class Event_Query_Dict:

    def __init__(self, event_line, num_in_file):

        # Function Description: This class will encapsulate all the mappings pertaining to an event line.
        # Function Parameters: event_line (A line from an Event File containing the needed data.)
        # Function Throws: None
        # Function Returns: None

        self.event_query_dict = self.create_event_query_dict(event_line, num_in_file)

    def __createHash(self, string_for_hash):

        # Function Description: Create a hash which will be the following ID for the event that took place.
        # Parameters: string_for_hash (The string that will be hashed into the ID)
        # Returns: newHash (The new ID) Throws: None
        
        if (str(type(string_for_hash)) != '<class \'str\'>'):
            raise TypeError("ERROR: || Class -> Event_Driver || Function -> __createHash || Reason -> A non-string entity was inputted.")
        return sha224(string_for_hash.encode('utf-8')).hexdigest()

    def create_event_query_dict(self, full_event_line, num_in_file):

        # Function Description: Convert the event instance into a dictionary of keys (The column names from SQL file) with their associated values.
        # Function Parameters: full_event_line (A line from the event file), num_in_file (The number in the file where the event line appears.)
        # Throws: None
        # Returns: eventDict (The dictionary of query components to insert.)

        splitString = full_event_line.replace('"', '')
        splitString = splitString.split(',')
        if len(splitString) != 96: raise ValueError("ERROR: || Class -> Event_Query_Dict || Function -> __createEventQuerydict || Reason -> The array does not contain 96 elements.")
        eventDict = {}                                             # The following is the hard coded dictionary to hold the query information.
        eventDict['idEvent'] = str(num_in_file) + splitString[0]   # Table Name: Event_Instance, Error_Information, Batter_In_Event (W\ Res), Pitcher_In_Event (W\ Res), All Positional Tables 
        eventDict['Game_ID'] = splitString[0]                      # All Resp Tables, All Base Runners, All Pinch Runners and Hitters, Fielding Information Table Name: Event_Instance, Game_Day
        eventDict['Visiting_Team'] = splitString[1]                # Table Name: Game_Day
        eventDict['Inning'] = splitString[2]                       # Table Name: Event_Instance
        eventDict['Batting_Team'] = splitString[3]                 # Table Name: Batter_In_Event    
        eventDict['Outs'] = splitString[4]                         # Table Name: Event_Instance
        eventDict['Balls'] = splitString[5]                        # Table Name: Batter_In_Event  
        eventDict['Strikes'] = splitString[6]                      # Table Name: Batter_In_Event  
        eventDict['Pitch_Sequence'] = splitString[7]               # Table Name: Pitcher_In_Event
        eventDict['Vis_Score'] = splitString[8]                    # Table Name: Event_Instance
        eventDict['Home_Score'] = splitString[9]                   # Table Name: Event_Instance
        eventDict['Batter_Name'] = splitString[10]                 # Table Name: Batter_In_Event 
        eventDict['Batter_Hand'] = splitString[11]                 # Table Name: Batter_In_Event 
        eventDict['Res_Batter_Name'] = splitString[12]             # Table_Name: Res_Batter_Information
        eventDict['Res_Batter_Hand'] = splitString[13]             # Table_Name: Res_Batter_Information
        eventDict['Pitcher_Name'] = splitString[14]                # Table Name: Pitcher_In_Event  
        eventDict['Pitcher_Hand'] = splitString[15]                # Table Name: Pitcher_In_Event
        eventDict['Res_Pitcher_Name'] = splitString[16]            # Table Name: Res_Pitcher_Information
        eventDict['Res_Pitcher_Hand'] = splitString[17]            # Table Name: Res_Pitcher_Information
        eventDict['Catcher'] = splitString[18]                     # Table Name: Event_Catcher_Base
        eventDict['First_Base'] = splitString[19]                  # Table Name: Event_First_Base
        eventDict['Second_Base'] = splitString[20]                 # Table Name: Event_Second_Base
        eventDict['Third_Base'] = splitString[21]                  # Table Name: Event_Thrid_Base
        eventDict['Shortstop'] = splitString[22]                   # Table Name: Event_Shortstop
        eventDict['Left_Field'] = splitString[23]                  # Table Name: Event_Left_Field
        eventDict['Center_Field'] = splitString[24]                # Table Name: Event_Centre_Field
        eventDict['Right_Field'] = splitString[25]                 # Table Name: Event_Right_Field
        eventDict['First_Runner'] = splitString[26]                # Table Name: runner_on_first_details
        eventDict['Second_Runner'] = splitString[27]               # Table Name: runner_on_second_details
        eventDict['Third_Runner'] = splitString[28]                # Table Name: runner_on_third_details
        eventDict['Event_Text'] = splitString[29]                  # Table Name: Event_Instance
        eventDict['Leadoff_Flag'] = splitString[30]                # Table Name: Batter_In_Event            
        eventDict['Pinch_Hit_Flag'] = splitString[31]              # Table Name: Batter_In_Event     
        eventDict['Defensive_Position'] = splitString[32]          # Table Name: Batter_In_Event    
        eventDict['Lineup_Position'] = splitString[33]             # Table Name: Batter_In_Event 
        eventDict['Event_Type'] = splitString[34]                  # Table Name: Event_Instance
        eventDict['Batter_Event_Flag'] = splitString[35]           # Table Name: Event_Instance
        eventDict['AB_Flag'] = splitString[36]                     # Table Name: Event_Instance
        eventDict['Hit_Value'] = splitString[37]                   # Table Name: Event_Instance
        eventDict['SH_Flag'] = splitString[38]                     # Table Name: Event_Instance
        eventDict['SF_Flag'] = splitString[39]                     # Table Name: Event_Instance
        eventDict['Outs_on_Play'] = splitString[40]                # Table Name: Event_Instance
        eventDict['Double_Play_Flag'] = splitString[41]            # Table Name: Event_Instance
        eventDict['Triple_Play_Flag'] = splitString[42]            # Table Name: Event_Instance
        eventDict['RBI_On_Play'] = splitString[43]                 # Table Name: Event_Instance
        eventDict['Wild_Pitch_Flag'] = splitString[44]             # Table Name: Event_Instance
        eventDict['Passed_Ball_Flag'] = splitString[45]            # Table Name: Event_Instance
        eventDict['Fielded_By'] = splitString[46]                  # Table Name: Event_Instance
        eventDict['Batted_Ball_Type'] = splitString[47]            # Table Name: Event_Instance
        eventDict['Bunt_Flag'] = splitString[48]                   # Table Name: Event_Instance
        eventDict['Foul_Flag'] = splitString[49]                   # Table Name: Event_Instance
        eventDict['Hit_Location'] = splitString[50]                # Table Name: Event_Instance
        eventDict['Num_Errors'] = splitString[51]                  # Table Name: Event_Instance
        eventDict['1st_Error_Player'] = splitString[52]            # Table Name: Error_Information (Only if it exists)
        eventDict['1st_Error_Type'] = splitString[53]              # Table Name: Error_Information (Only if it exists)
        eventDict['2nd_Error_Player'] = splitString[54]            # Table Name: Error_Information (Only if it exists)
        eventDict['2nd_Error_Type'] = splitString[55]              # Table Name: Error_Information (Only if it exists)
        eventDict['3rd_Error_Player'] = splitString[56]            # Table Name: Error_Information (Only if it exists)
        eventDict['3rd_Error_Type'] = splitString[57]              # Table Name: Error_Information (Only if it exists)
        eventDict['Batter_Dest'] = splitString[58]                 # Table Name: Event_Instance
        eventDict['Runner_On_1st_Dest'] = splitString[59]          # Table Name: runner_on_first_details
        eventDict['Runner_On_2nd_Dest'] = splitString[60]          # Table Name: runner_on_second_details
        eventDict['Runner_On_3rd_Dest'] = splitString[61]          # Table Name: runner_on_third_details
        eventDict['Play_on_Batter'] = splitString[62]              # Table Name: Event_Instance
        eventDict['Play_On_Runner_On_1st'] = splitString[63]       # Table Name: runner_on_first_details
        eventDict['Play_On_Runner_On_2nd'] = splitString[64]       # Table Name: runner_on_second_details
        eventDict['Play_On_Runner_On_3rd'] = splitString[65]       # Table Name: runner_on_third_details
        eventDict['SB_Runner_On_1st_Flag'] = splitString[66]       # Table Name: runner_on_first_details
        eventDict['SB_Runner_On_2nd_Flag'] = splitString[67]       # Table Name: runner_on_second_details
        eventDict['SB_Runner_On_3rd_Flag'] = splitString[68]       # Table Name: runner_on_third_details
        eventDict['CS_Runner_On_1st_Flag'] = splitString[69]       # Table Name: runner_on_first_details
        eventDict['CS_Runner_On_2nd_Flag'] = splitString[70]       # Table Name: runner_on_second_details
        eventDict['CS_Runner_On_3rd_Flag'] = splitString[71]       # Table Name: runner_on_third_details
        eventDict['PO_For_Runner_On_1st_Flag'] = splitString[72]                     # Table Name: runner_on_first_details
        eventDict['PO_For_Runner_On_2nd_Flag'] = splitString[73]                     # Table Name: runner_on_second_details
        eventDict['PO_For_Runner_On_3rd_Flag'] = splitString[74]                     # Table Name: runner_on_third_details
        eventDict['Responsible_Pitcher_For_Runner_On_1st'] = splitString[75]         # Table Name: Responsible_Pitcher_For_First
        eventDict['Responsible_Pitcher_For_Runner_On_2nd'] = splitString[76]         # Table Name: Responsible_Pitcher_For_Second
        eventDict['Responsible_Pitcher_For_Runner_On_3rd'] = splitString[77]         # Table Name: Responsible_Pitcher_For_Third
        eventDict['New_Game_Flag'] = splitString[78]                                 # Table Name: Event_Instance
        eventDict['End_Game_Flag'] = splitString[79]                                 # Table Name: Event_Instance
        eventDict['Pinch_Runner_On_1st'] = splitString[80]                           # Table Name: runner_on_first_details
        eventDict['Pinch_Runner_On_2nd'] = splitString[81]                           # Table Name: runner_on_second_details
        eventDict['Pinch_Runner_On_3rd'] = splitString[82]                           # Table Name: runner_on_third_details
        eventDict['Runner_Removed_For_Pinch_Runner_On_1st'] = splitString[83]        # Table Name: pinch_runner_removed_1st
        eventDict['Runner_Removed_For_Pinch_Runner_On_2nd'] = splitString[84]        # Table Name: pinch_runner_removed_2nd
        eventDict['Runner_Removed_For_Pinch_Runner_On_3rd'] = splitString[85]        # Table Name: pinch_runner_removed_3rd
        eventDict['Batter_Removed_For_Pinch_Hitter'] = splitString[86]               # Table Name: position_of_batter_for_pinch_hitter
        eventDict['Position_of_Batter_removed_for_Pinch_Hitter'] = splitString[87]   # Table Name: position_of_batter_for_pinch_hitter   
        eventDict['Fielder_With_First_Putout'] = splitString[88]                     # Table Name: fielder_putout_information                 
        eventDict['Fielder_With_Second_Putout'] = splitString[89]                    # Table Name: fielder_putout_information            
        eventDict['Fielder_With_Third_Putout'] = splitString[90]                     # Table Name: fielder_putout_information      
        eventDict['Fielder_With_First_Assist'] = splitString[91]                     # Table Name: fielder_assist_information    
        eventDict['Fielder_With_Second_Assist'] = splitString[92]                    # Table Name: fielder_assist_information    
        eventDict['Fielder_With_Third_Assist'] = splitString[93]                     # Table Name: fielder_assist_information    
        eventDict['Fielder_With_Fourth_Assist'] = splitString[94]                    # Table Name: fielder_assist_information    
        eventDict['Fielder_With_Fifth_Assist'] = splitString[95]                     # Table Name: fielder_assist_information    
        return eventDict

class Event_Driver(Driver):

    def __init__(self, db_connection):
        
        # Function Description: Intialise the Event_Driver. Inherits from Driver.
        # Function Parameters: db_connection (pymysql.connections.Connection: The connection to the database.)  
        # Function Throws: Nothing
        # Function Returns: Nothing

        Driver.__init__(self, db_connection)                            # Send the parameters up.

    def insert_event_dynamic(self, column_names, event_query_dict, table_name):

        # Function Description: Build Insert statements based on the names and values given.
        #    Once the query is built, execute it!
        # Function Parameters: column_names (The names of the columns to insert into the database.), 
        #     event_query_dict (The dictionary that contains all the values that will be inserted into the database.), 
        #     table_name (The name of the table that will recieve the new content.) 
        # Function Throws: Nothing
        # Function Returns: True or False (True will be turned if there are no warnings or errors. False will be returned otherwise.)

        return self.execute_query(self.create_query_string(column_names, event_query_dict, table_name))       

    def build_error_information(self, error_player_pos, error_type, event_id, error_position):

        # Function Description: The function inserts content into the Error Information table.
        # Function Parameters: error_player_pos (The positional number of the player who made the error (i.e. 1-9)), 
        #    error_type (The type of error that was made), event_id (The id of the event), 
        #    error_position (The position in the event the error was incurred. (1st, 2nd, or 3rd)) 
        # Function Throws: Nothing
        # Function Returns: The query that will insert the error information.
        
        return "INSERT INTO Error_Information (Error_Player, idEvent, Error_Type, Error_Position) VALUES ('{}', '{}', '{}', '{}');".format(error_player_pos, event_id, error_type, error_position)

    def insert_fielding_instance(self, event_id, fielder_pos, putout_number, table_name):

        # Function Description: Insert Fielding Information from either a Putout or an Assist.
        # Function Parameters: event_id (The event Id connected to the fielding information.), 
        #     fielder_pos (The position of the fielder (1-9) who made the play.), 
        #     putout_number (The putout number within the event (1-3).), 
        #     table_name (The table to insert the content into. (Either assist or putout.))
        # Function Throws: ValueError (The error is thrown if the table name is incorrect.)
        # Function Returns: The query will be later inserted into the data base.

        if table_name == 'Fielder_Assist_Information':
            return "INSERT INTO Fielder_Assist_Information (idEvent, Fielder_Number, Assist_Number) VALUES ('{}', '{}', '{}');".format(event_id, fielder_pos, putout_number)
        elif table_name == 'Fielder_Putout_Information':
            return "INSERT INTO Fielder_Putout_Information (idEvent, Fielder_Number, Putout_Number) VALUES ('{}', '{}', '{}');".format(event_id, fielder_pos, putout_number)
        else:
            raise ValueError("The table name entered was incorrect.") 

    def insert_player_from_event(self, column_names, player_driver, event_query_dict, table_name, column_of_player_name):

        # Function Description: The function will insert all the required contents into event tables that ALSO
        #     require the insertion of a Player ID.
        # Function Parameters: player_driver (The reference to a player driver obeck to insert the player information.)
        #     column_names (The names of the columns to insert into the database.), 
        #     event_query_dict (The dictionary that contains all the values that will be inserted into the database.), 
        #     table_name (The name of the table that will recieve the new content.), 
        #     column_of_player_name (The name of the key within the event query dictionary that requires insertion into the player database.)
        # Function Throws: Nothing
        # Function Returns: True or False (The function throws True when the query was successful in its insertion. Otherwise, the function will be False.)
        
        player_check = player_driver.check_and_insert_player(event_query_dict[column_of_player_name])
        if not player_check: raise UnrecognisableMySQLBehaviour("The player was not properly inserted or found in the Player Information table.")
        return self.insert_event_dynamic(column_names, event_query_dict, table_name)