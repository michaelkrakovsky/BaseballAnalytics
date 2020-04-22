# The following utility will insert player information into the database. 

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

    def __init__(self, dbConnection, path_to_player_list):

        # Function Description: Intialise the Player_Driver. The Player_Driver will handle all the function related to the players including:
        #       1. Ensure and possibly insert a potentially new player into the database.
        # Paramters: dbConnection (pymysql.connections.Connection: The connection to the database.), 
        #     path_to_player_list (file: The path locating the list of players.)
        # Throws: ValueError (Within multiple functions to check types.)
        # Returns: None

        if (str(type(dbConnection)) == '<class \'pymysql.connections.Connection\'>'):
            self.__dbConnect__ = dbConnection
        else:
            raise ValueError("ERROR: || Class -> Player_Driver || Function -> __init__ || Reason -> Connection parameter is invalid.")
        if (str(type(path_to_player_list)) == '<class \'str\'>'):
            try:
                with open(path_to_player_list) as f:                         # The following checks are somewhat vunerable. However, the intent is not to enhance
                    firstLine = f.readline()                                 # security but to guard and inform the programmer about careless mistakes in the code.                                  
                    if ("Last_Name,First_Name,idPlayer Details,Player_Debut\n" == str(firstLine)):
                        self.__playerList__ = self.__generatePlayerList(path_to_player_list)
                    else:
                        raise ValueError("ERROR: || Class -> Player_Driver || Function -> __init__ || Reason -> The file does not contain the proper information.")
            except FileNotFoundError:
                raise FileNotFoundError("ERROR: || Class -> Player_Driver || Function -> __init__ || Reason -> The player file does not exist.")

    def __convertDate(self, date):

        # Function Description: Convert the date from the CSV file into to proper MySQL format.
        # Parameters: self (The instance of the object.), 
        # date (str: The date present in the CSV file.), 
        # Throws: None
        # Returns: newDate (str: The new converted date)

        newDate = date[-4:] + '-'
        newDate += date[0:2] + '-'
        newDate += date[3:5]
        return newDate   # Format: Year-Month-Day   

    def __generatePlayerList(self, path_to_player_list):

        # Function Description: Generate a dictionary to store the foundational information about each player.
        # Parameters: self (The instance of the object), 
        # path_to_player_list (str: The path locating the list of players.)
        # Throws: None
        # Returns: playerList (Dict: A dictionary containing a list of all the players identifies by the users key.)

        with open(path_to_player_list) as f:                        
            f.readline()                                   # Throw away the first line, the title line.
            playerDict = {}
            for line in f:
                noNewLines = line.rstrip()
                splitElements = noNewLines.split(',')
                newPlayer = Player(splitElements[1], splitElements[0], splitElements[3])    # How the data is formatted in the CSV file.
                playerDict[splitElements[2]] = newPlayer
        return playerDict

    def __build_query(self, playerID):

        # Function Description: Build the query string to send to the database.
        # Function Parameters: context_found (When you want to insert a player as a Positional Player or Pitcher Player), 
        #   playerID (str: The player ID you wish to verify within the database.)
        # Function Throws: Nothing
        # Funtion Returns: query (The query to be inserted into the database.)

        analyse_player = self.__playerList__[playerID]
        convert_date = self.__convertDate(analyse_player.playerDebut)
        query = "INSERT IGNORE INTO player_information (player_id, Last_Name, First_Name, Player_Debut) values (\'" + playerID + "\', \'" + analyse_player.lastName + "\', \'" + analyse_player.firstName + "\', \'" + convert_date + "\')"
        return query

    def check_player(self, player_Id):

        # Function Description: The function checks if the player exists in the player database.
        # Function Parameters: player_Id (The ID of the player to check within the database.)
        # Function Throws: Nothing
        # Function Returns: True or False (If the player is found, return True. Elsewise, return False.)

        pass   # Build

    def insert_player(self, playerID):

        # Function Description: Attempt to insert a player into the database.
        # Function Parameters: playerID (str: The player ID you wish to verify within the database.)
        # Function Throws: ValueError (When the proper input has not been properly submitted.)
        # Function Returns: 0 (If nothing was inserted.), 1 (If something was inserted.)
        
        if (playerID in self.__playerList__):
            aCursor = self.__dbConnect__.cursor()
            query = self.__build_query(playerID)            # Retrieve the query to insert into the database.                
            filterwarnings('error')                         # Convert warnings into exceptions to be caught.                             
            try:
                status = aCursor.execute(query)             # Execute Query: And close the cursor.
                self.__dbConnect__.commit()    
            except Warning as warn:
                warn = str(warn)                            # Ensure the warning is a duplicate entry warning to avoid data problems     
                warnNum = warn[1:5]                         
                if (warnNum != "1062"):                     # 1062 is a warning that the ID already exists.
                    raise UnrecognisableMySQLBehaviour("ERROR: || Class -> Player_Driver || Function -> checkAndInsert || Reason -> The warning was not the expected 'Duplicate Entry'. Please investigate to avoid data entry discrepancies.")
                status = 0                                
            filterwarnings('always')                        # Turn the filter for warnings back on.
            aCursor.close()
        else:
            raise ValueError("ERROR: || Class -> Player_Driver || Function -> checkAndInsert || Reason -> The Player ID does not exist in the CSV File.")
        return status                   # 1 For a Successful Query, 0 For an Unsuccessful