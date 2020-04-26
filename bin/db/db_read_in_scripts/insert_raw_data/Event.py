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

    def __init__(self, event_line):

        # Function Description: This class will encapsulate all the mappings pertaining to an event line.
        # Parameters: event_line (A line from an Event File containing the needed data.)
        # Throws: None
        # Returns: None

        self.event_query_dict = self.create_event_query_dict(event_line)

    def __createHash(self, stringForHash):

        # Function Description: Create a hash which will be the following ID for the event that took place.
        # Parameters: self (The instance of the object), stringForHash (The string that will be hashed into the ID)
        # Returns: newHash (The new ID) Throws: None
        
        if (str(type(stringForHash)) != '<class \'str\'>'):
            raise TypeError("ERROR: || Class -> Event_Driver || Function -> __createHash || Reason -> A non-string entity was inputted.")
        return sha224(stringForHash.encode('utf-8')).hexdigest()

    def create_event_query_dict(self, full_event_line):

        # Function Description: Convert the event instance into a dictionary of keys (The column names from SQL file) with their associated values.
        # Parameters: self (The instance of the object), full_event_line (A line from the event file)
        # Throws: None
        # Returns: eventDict (The dictionary of query components to insert.)

        splitString = full_event_line.replace('"', '')
        splitString = splitString.split(',')
        if len(splitString) != 96: raise ValueError("ERROR: || Class -> Event_Query_Dict || Function -> __createEventQuerydict || Reason -> The array does not contain 96 elements.")
        eventDict = {}                                             # The following is the hard coded dictionary to hold the query information.
        eventDict['idEvent'] = self.__createHash(full_event_line)  # Table Name: Event_Instance, Error_Information, Batter_In_Event (W\ Res), Pitcher_In_Event (W\ Res), All Positional Tables 
        eventDict['Game_ID'] = splitString[0]                      # Table Name: Event_Instance, Game_Day
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
        eventDict['Catcher'] = splitString[18]
        eventDict['First_Base'] = splitString[19]
        eventDict['Second_Base'] = splitString[20]
        eventDict['Third_Base'] = splitString[21]
        eventDict['Shortstop'] = splitString[22]
        eventDict['Left_Field'] = splitString[23]
        eventDict['Center_Field'] = splitString[24]
        eventDict['Right_Field'] = splitString[25]
        eventDict['First_Runner'] = splitString[26]
        eventDict['Second_Runner'] = splitString[27]
        eventDict['Third_Runner'] = splitString[28]
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
        eventDict['Runner_On_1st_Dest'] = splitString[59]
        eventDict['Runner_On_2nd_Dest'] = splitString[60]
        eventDict['Runner_On_3rd_Dest'] = splitString[61]
        eventDict['Play_on_Batter'] = splitString[62]              # Table Name: Event_Instance
        eventDict['Play_On_Runner_On_1st'] = splitString[63]
        eventDict['Play_On_Runner_On_2nd'] = splitString[64]
        eventDict['Play_On_Runner_On_3rd'] = splitString[65]  
        eventDict['SB_Runner_On_1st_Flag'] = splitString[66]
        eventDict['SB_Runner_On_2nd_Flag'] = splitString[67]
        eventDict['SB_Runner_On_3rd_Flag'] = splitString[68]
        eventDict['CS_Runner_On_1st_Flag'] = splitString[69]
        eventDict['CS_Runner_On_2nd_Flag'] = splitString[70]
        eventDict['CS_Runner_On_3rd_Flag'] = splitString[71]
        eventDict['PO_For_Runner_On_1st_Flag'] = splitString[72]
        eventDict['PO_For_Runner_On_2nd_Flag'] = splitString[73]
        eventDict['PO_For_Runner_On_3rd_Flag'] = splitString[74]
        eventDict['Responsible_Pitcher_For_Runner_On_1st'] = splitString[75]
        eventDict['Responsible_Pitcher_For_Runner_On_2nd'] = splitString[76]
        eventDict['Responsible_Pitcher_For_Runner_On_3rd'] = splitString[77]
        eventDict['New_Game_Flag'] = splitString[78]                                 # Table Name: Event_Instance
        eventDict['End_Game_Flag'] = splitString[79]                                 # Table Name: Event_Instance
        eventDict['Pinch_Runner_On_1st'] = splitString[80]
        eventDict['Pinch_Runner_On_2nd'] = splitString[81]
        eventDict['Pinch_Runner_On_3rd'] = splitString[82]
        eventDict['Runner_Removed_For_Pinch-Runner_On_1st'] = splitString[83]
        eventDict['Runner_Removed_For_Pinch-Runner_On_2nd'] = splitString[84]
        eventDict['Runner_Removed_For_Pinch-Runner_On_3rd'] = splitString[85]
        eventDict['Batter_Removed_For_Pinch_Hitter'] = splitString[86]
        eventDict['Position_of_Batter_removed_for_Pinch_Hitter'] = splitString[87]       
        eventDict['Fielder_With_First_Putout'] = splitString[88]                     
        eventDict['Fielder_With_Second_Putout'] = splitString[89]                    
        eventDict['Fielder_With_Third_Putout'] = splitString[90]                         
        eventDict['Fielder_With_First_Assist'] = splitString[91]                         
        eventDict['Fielder_With_Second_Assist'] = splitString[92]                        
        eventDict['Fielder_With_Third_Assist'] = splitString[93]                         
        eventDict['Fielder_With_Fourth_Assist'] = splitString[94]                        
        eventDict['Fielder_With_Fifth_Assist'] = splitString[95]                         
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

        query = "INSERT IGNORE INTO " + table_name + " ("
        second_query_half = ") Values ("
        for i in column_names:
            query += i + ", "                                 # Add the column names.  
            try:
                val = int(event_query_dict[i])
                second_query_half += str(val) + " , "
            except ValueError:                                # Must be a string, insert as a string.
                second_query_half += "\'" + event_query_dict[i] + "\' , "
        query = query[:-2]                                    # Remove the ending of the string (The comma and space)
        second_query_half = second_query_half[:-3]
        query += second_query_half + ");"
        return self.execute_query(query)       

    def insert_event_instance(self, event_query_dict):

        # Function Description: Insert the contents from an event query dict into the Event Instance Table. 
        # Function Parameters: event_query_dict (An event query dictionary object.)
        # Function Throws: Nothing
        # Function Returns: True (If a successful query has taken place.) False (If the query did not execute cleanly.)                 
        
        return self.insert_event_dynamic(['idEvent', 'Game_ID', 'Inning', 'Outs', 'Vis_Score', 'Home_Score','Event_Text', 'Event_Type', 
                                    'Batter_Event_Flag', 'AB_Flag', 'Hit_Value', 'SH_Flag', 'SF_Flag', 'Outs_on_Play', 'Double_Play_Flag', 
                                    'Triple_Play_Flag', 'RBI_On_Play', 'Wild_Pitch_Flag', 'Passed_Ball_Flag', 'Fielded_By', 'Batted_Ball_Type', 
                                    'Bunt_Flag', 'Foul_Flag', 'Hit_Location', 'Num_Errors', 'Batter_Dest', 'Play_on_Batter', 'New_Game_Flag', 
                                    'End_Game_Flag'], event_query_dict, "Event_Instance")

    def insert_error_information(self, error_player_pos, error_type, event_id, error_position):

        # Function Description: The function inserts content into the Error Information table.
        # Function Parameters: error_player_pos (The positional number of the player who made the error (i.e. 1-9)), 
        #    error_type (The type of error that was made), event_id (The id of the event), 
        #    error_position (The position in the event the error was incurred. (1st, 2nd, or 3rd)) 
        # Function Throws: Nothing
        # Function Returns: True (If a successful query has taken place.) False (If the query did not execute cleanly.)
        
        query = "INSERT INTO Error_Information (Error_Player, idEvent, Error_Type, Error_Position) VALUES ('{}', '{}', '{}', '{}')".format(error_player_pos, event_id, error_type, error_position)
        return self.execute_query(query)

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
