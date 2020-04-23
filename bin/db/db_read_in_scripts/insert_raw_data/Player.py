# The following utility will insert player information into the database. 

from os import path
from pickle import dump, load, HIGHEST_PROTOCOL
from Driver_Exceptions import UnrecognisableMySQLBehaviour
from warnings import filterwarnings                         # Handle warnings from mysql.

class Player:

    def __init__(self, fName, lName, playerDebut):

        # Function Description: Intialise the Player object. The Player object will encapsulate basic knowledge to make the code more readable.
        # Parameters: self (The instance of the object), 
        # fName (The player's first name.), lName (The player's last name.), playerDebut (The date of deployment.) 
        # Throws: ValueError (Throw when one parameter is not a string.)
        # Returns: None

        if (str(type(fName)) != "<class \'str\'>"):
            raise ValueError("ERROR: || Class -> Player || Function -> __init__ || Reason -> First Name is not a string.")
        elif (str(type(lName)) != "<class \'str\'>"):
            raise ValueError("ERROR: || Class -> Player || Function -> __init__ || Reason -> Last Name is not a string.")
        elif (str(type(playerDebut)) != "<class \'str\'>"):
            raise ValueError("ERROR: || Class -> Player || Function -> __init__ || Reason -> Player Debut is not a string.")
        else:
            self.firstName = fName
            self.lastName = lName
            self.playerDebut = playerDebut

class Player_Driver:

    def __init__(self, db_connection, path_to_raw_player_data, player_dict=None):

        # Function Description: Intialise the Player_Driver. The Player_Driver will handle all the function related to the players including:
        #       1. Ensure and possibly insert a potentially new player into the database.
        # Function Parameters: db_connection (pymysql.connections.Connection: The connection to the database.), 
        #     path_to_raw_player_data (The path to the raw player data. At a minimum, there should exist the excel file of the roster.) 
        # Function Throws: FileNotFoundError (The error is thrown when the roster excel file or roster pickle file is not found.)
        # Function Returns: Nothing

        self.__dbConnect__ = db_connection
        self.path_to_player_list = path_to_raw_player_data / 'player_data.csv'
        self.path_to_pickle_player_list = path_to_raw_player_data / 'pickle_player_data.pickle'
        if player_dict != None:                                                                   # Discover where to get the player list contents. From the pickle file, excel file or parameters.
            self.__player_list__ = player_dict
        else:
            self.__player_list__ = self.__process_player_file_contents(self.path_to_player_list, self.path_to_pickle_player_list)

    def __convert_date(self, date):

        # Function Description: Convert the date from the CSV file into to proper MySQL format.
        # Parameters: self (The instance of the object.), 
        # date (str: The date present in the CSV file.), 
        # Throws: None
        # Returns: newDate (str: The new converted date)

        newDate = date[-4:] + '-'
        newDate += date[0:2] + '-'
        newDate += date[3:5]
        return newDate   # Format: Year-Month-Day   

    def __generate_player_list(self, path_to_player_list):

        # Function Description: Generate a dictionary to store the foundational information about each player.
        # Parameters: self (The instance of the object), 
        # path_to_player_list (str: The path locating the list of players.)
        # Throws: None
        # Returns: playerList (Dict: A dictionary containing a list of all the players identified by the users key.)

        with open(path_to_player_list) as f:                        
            f.readline()                                   # Throw away the first line, the title line.
            playerDict = {}
            for line in f:
                noNewLines = line.rstrip()
                splitElements = noNewLines.split(',')
                newPlayer = Player(splitElements[1], splitElements[0], splitElements[3])    # How the data is formatted in the CSV file.
                playerDict[splitElements[2]] = newPlayer
        return playerDict

    def __process_player_file_contents(self, path_to_player_list, path_to_pickle_player_list):

        # Function Description: Get the roster file from either the pickle file or the excel file. Create the pickle file from
        #    excel file if it does not exist.
        # Function Parameters: path_to_player_list (The path to the Excel file containing the player information.), 
        #     path_to_pickle_player_list (The path to the pickle file containing th eplayer information.)
        # Function Throws: FileNotFoundError (The exception is thrown if the excel file is not found.)
        # Function Returns: player_dict (The contents from the excel file in a dictionary structure.)

        if not path.isfile(path_to_player_list): raise FileNotFoundError("The excel file containing the roster information was not found.")
        if not path.isfile(path_to_pickle_player_list):                                                                                         # Create a new pickle file with the player contents.
            player_dict = self.__generate_player_list(path_to_player_list)
            with open(path_to_pickle_player_list, "wb+") as pickle_file: dump(player_dict, pickle_file, protocol=HIGHEST_PROTOCOL)
            return player_dict
        with open(path_to_pickle_player_list, 'rb') as pickle_file:
            return load(pickle_file)

    def __build_query(self, player_Id):

        # Function Description: Build the query string to send to the database.
        # Function Parameters: context_found (When you want to insert a player as a Positional Player or Pitcher Player), 
        #   player_Id (str: The player ID you wish to verify within the database.)
        # Function Throws: Nothing
        # Funtion Returns: query (The query to be inserted into the database.)

        analyse_player = self.__player_list__[player_Id]
        convert_date = self.__convert_date(analyse_player.playerDebut)
        query = "INSERT IGNORE INTO player_information (player_id, Last_Name, First_Name, Player_Debut) values (\'" + player_Id + "\', \'" + analyse_player.lastName + "\', \'" + analyse_player.firstName + "\', \'" + convert_date + "\')"
        return query

    def check_and_insert_player(self, player_Id):

        # Function Description: The function checks to see if the player is in the database. If it is not
        #    present, the player will be inserted into the database.
        # Function Parameters: player_Id (The player to insert into the database.)
        # Function Throws: Nothing
        # Function Returns: True or False (If the player is successfully inserted or is already inserted, return True. Elsewise, return False.)

        if self.check_player(player_Id): return True
        return self.insert_player(player_Id)

    def check_player(self, player_Id):

        # Function Description: The function checks if the player exists in the player database.
        # Function Parameters: player_Id (The ID of the player to check within the database.)
        # Function Throws: Nothing
        # Function Returns: True or False (If the player is found, return True. Elsewise, return False.)

        query = 'select player_id from player_information where player_id = \'' + player_Id + '\';'
        return bool(self.__dbConnect__.cursor().execute(query))

    def insert_player(self, player_Id):

        # Function Description: Attempt to insert a player into the database.
        # Function Parameters: player_Id (str: The player ID you wish to verify within the database.)
        # Function Throws: ValueError (When the proper input has not been properly submitted.)
        # Function Returns: True or False (True will be returned if the query was successfully executed. Elsewise, False will be returned.)
        
        if (player_Id in self.__player_list__):
            cursor = self.__dbConnect__.cursor()
            query = self.__build_query(player_Id)           # Retrieve the query to insert into the database.                
            filterwarnings('error')                         # Convert warnings into exceptions to be caught.                             
            try:
                status = cursor.execute(query)             # Execute Query: And close the cursor.
                self.__dbConnect__.commit()    
            except Warning as warn:
                warn = str(warn)                            # Ensure the warning is a duplicate entry warning to avoid data problems     
                warnNum = warn[1:5]                         
                if (warnNum != "1062"):                     # 1062 is a warning that the ID already exists.
                    raise UnrecognisableMySQLBehaviour("ERROR: || Class -> Player_Driver || Function -> checkAndInsert || Reason -> The warning was not the expected 'Duplicate Entry'. Please investigate to avoid data entry discrepancies.")
                status = 0                                
            filterwarnings('always')                        # Turn the filter for warnings back on.
            cursor.close()
        else:
            raise ValueError("ERROR: || Class -> Player_Driver || Function -> checkAndInsert || Reason -> The Player ID does not exist in the CSV File.")
        return bool(status)                                 # 1 For a Successful Query, 0 For an Unsuccessful