# Program Description: All the function to insert a player into the database.
# Date: April 23, 2019
# Author: Michael Krakovsky
# Version: 1.0

from pymysql import connect
from warnings import filterwarnings                         # Handle warnings from mysql.
from hashlib import sha224
from pyperclip import copy
from Driver_Exceptions import UnrecognisableMySQLBehaviour
from Player import Player_Driver
from Game import Game_Driver

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
        if len(splitString) != 96:
            raise ValueError("ERROR: || Class -> Event_Query_Dict || Function -> __createEventQuerydict || Reason -> The array does not contain 96 elements.")
        eventDict = {}              # The following is the hard coded dictionary to hold the query information.
        eventDict['idEvent'] = self.__createHash(full_event_line)  # Map each key to the correct value within the query.
        eventDict['Game_ID'] = splitString[0]                      # Table Name: Event_Instance
        eventDict['Visiting_Team'] = splitString[1]                # Table Name: Game_Day
        eventDict['Inning'] = splitString[2]                       # Table Name: Event_Instance
        eventDict['Batting_Team'] = splitString[3]                 # Table Name: Event_Instance
        eventDict['Outs'] = splitString[4]                         # Table Name: Event_Instance
        eventDict['Balls'] = splitString[5]                        # Table Name: Event_Instance
        eventDict['Strikes'] = splitString[6]                      # Table Name: Event_Instance
        eventDict['Pitch_Sequence'] = splitString[7]               # Table Name: Event_Instance
        eventDict['Vis_Score'] = splitString[8]                    # Table Name: Event_Instance
        eventDict['Home_Score'] = splitString[9]                   # Table Name: Event_Instance
        eventDict['Batter_Name'] = splitString[10]                 # Table Name: Event_Instance
        eventDict['Batter_Hand'] = splitString[11]                 # Table Name: Event_Instance
        eventDict['Res_Batter_Name'] = splitString[12]
        eventDict['Res_Batter_Hand'] = splitString[13]
        eventDict['Pitcher_Name'] = splitString[14]                # Table Name: Event_Instance
        eventDict['Pitcher_Hand'] = splitString[15]                # Table Name: Event_Instance
        eventDict['Res_Pitcher_Name'] = splitString[16]
        eventDict['Res_Pitcher_Hand'] = splitString[17]
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
        eventDict['Leadoff_Flag'] = splitString[30]                # Table Name: Event_Instance
        eventDict['Pinch_Hit_Flag'] = splitString[31]              # Table Name: Event_Instance
        eventDict['Defensive_Position'] = splitString[32]          # Table Name: Event_Instance
        eventDict['Lineup_Position'] = splitString[33]             # Table Name: Event_Instance
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
        eventDict['1st_Error_Player'] = splitString[52] 
        eventDict['1st_Error_Type'] = splitString[53]
        eventDict['2nd_Error_Player'] = splitString[54]
        eventDict['2nd_Error_Type'] = splitString[55]
        eventDict['3rd_Error_Player'] = splitString[56]
        eventDict['3rd_Error_Type'] = splitString[57]
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
        eventDict['Fielder_With_First_Putout'] = splitString[88]                         # Table Name: Event_Instance
        eventDict['Fielder_With_Second_Putout'] = splitString[89]                        # Table Name: Event_Instance
        eventDict['Fielder_With_Third_Putout'] = splitString[90]                         # Table Name: Event_Instance
        eventDict['Fielder_With_First_Assist'] = splitString[91]                         # Table Name: Event_Instance
        eventDict['Fielder_With_Second_Assist'] = splitString[92]                        # Table Name: Event_Instance
        eventDict['Fielder_With_Third_Assist'] = splitString[93]                         # Table Name: Event_Instance
        eventDict['Fielder_With_Fourth_Assist'] = splitString[94]                        # Table Name: Event_Instance
        eventDict['Fielder_With_Fifth_Assist'] = splitString[95]                         # Table Name: Event_Instance
        return eventDict

class Event_Driver:

    def __init__(self, db_connection):
        
        # Function Description: Intialise the Event_Driver. The Event_Driver will handle all the function related to insert an Event:
        #       1. Insert a new instance of an Event.
        # Function Paramters: db_connection (pymysql.connections.Connection: The connection to the database.), 
        # Function Throws: ValueError (Within multiple functions to check types.)
        # Function Returns: None

        if (str(type(db_connection)) == '<class \'pymysql.connections.Connection\'>'):
            self.__dbConnect__ = db_connection
        else:
            raise ValueError("ERROR: || Class -> Event_Driver || Function -> __init__ || Reason -> Connection parameter is invalid.")
    
    def __buildQueryString(self, column_names, event_dict, table_name):

        # Function Description: Build Insert statements based on the names and values given.
        # Parameters: self (The instance of the object), column_names (The names to insert), 
        # event_dict (The values of the event in a dictionary), table_name (The name of the table) 
        # Throws: None
        # Returns: query (The query string)

        query = "INSERT IGNORE INTO " + table_name + " ("
        secondHalfQuery = ") Values ("
        for i in column_names:
            query += i + ", "                                 # Add the column names.  
            try:
                val = int(event_dict[i])
                secondHalfQuery += str(val) + " , "
            except ValueError:                                # Must be a string, insert as a string.
                secondHalfQuery += "\'" + event_dict[i] + "\' , "
        query = query[:-2]                                    # Remove the ending of the string (The comma and space)
        secondHalfQuery = secondHalfQuery[:-3]
        query += secondHalfQuery + ");"
        return query

    def __insertQuery(self, column_names, event_dict, table_name):

        # Function Description: Different types of query depending on the Column Names and Column Values. 
        # Function Parameters: column_names (The names to insert), event_dict (The values of the event in a dictionary)
        #   table_name (The name of the table) 
        # Function Throws: None
        # Function Returns: True (If a successful query has taken place.) False (If the query did not execute cleanly.)

        query = self.__buildQueryString(column_names, event_dict, table_name)
        aCursor = self.__dbConnect__.cursor() 
        filterwarnings('error')                                      # Convert warnings into exceptions to be caught.                   
        try:
            copy(query)     #### DELETEEEE
            status = aCursor.execute(query)                          # Execute Query: And close the cursor.
            self.__dbConnect__.commit()    
        except Warning as warn:
            warn = str(warn)                                         # Ensure the warning is a duplicate entry warning to avoid data problems     
            warnNum = warn[1:5]                         
            if (warnNum != "1062"):                 # An SQL Warning returning (1062, "Duplicate entry" ----- for key Primary)
                raise UnrecognisableMySQLBehaviour("ERROR: || Class -> Game_Driver || Function -> __insertQuery || Reason -> The warning was not the expected 'Duplicate Entry'. Please investigate to avoid data entry discrepancies.")
            status = 0
        filterwarnings('always')                        # Turn the filter for warnings back on.
        aCursor.close()
        if (status == 1):
            return True
        return False 

    def insert_event_instance(self, event_query_dict):

        # Function Description: Insert the contents from an event query dict into the Event Instance Table. 
        # Function Parameters: event_query_dict (An event query dictionary object.)
        # Function Throws: Nothing
        # Function Returns: True (If a successful query has taken place.) False (If the query did not execute cleanly.)                 
        
        return self.__insertQuery(['idEvent', 'Game_ID', 'Inning', 'Outs', 'Vis_Score', 'Home_Score','Event_Text', 'Event_Type', 
                                    'Batter_Event_Flag', 'AB_Flag', 'Hit_Value', 'SH_Flag', 'SF_Flag', 'Outs_on_Play', 'Double_Play_Flag', 
                                    'Triple_Play_Flag', 'RBI_On_Play', 'Wild_Pitch_Flag', 'Passed_Ball_Flag', 'Fielded_By', 'Batted_Ball_Type', 
                                    'Bunt_Flag', 'Foul_Flag', 'Hit_Location', 'Num_Errors', 'Batter_Dest', 'Play_on_Batter', 'New_Game_Flag', 
                                    'End_Game_Flag'], event_query_dict, "Event_Instance")
