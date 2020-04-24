# The following script will insert content into the tables related to games.

from Driver_Exceptions import UnrecognisableMySQLBehaviour
from warnings import filterwarnings                         # Handle warnings from mysql.

class Game_Driver:

    def __init__(self, db_connection):
        
        # Function Description: Intialise the Game_Driver. The Game_Driver will handle all the function related to a Game:
        #       1. Insert a new instance of a Game.
        # Paramters: db_connection (The existing connection to the database (We cannot open up multiple connections at once.))
        # Function Throws: Nothing
        # Function Returns: Nothing

        self.__dbConnect__ = db_connection       # Connect to db.
         
    def __convertDate(self, date):

        # Function Description: Convert the date from the CSV file into to proper MySQL format.
        # Parameters: self (The instance of the object.), 
        # date (str: The date present in the CSV file.), 
        # Throws: None
        # Returns: newDate (str: The new converted date)

        newDate = date[0:4] + '-'
        newDate += date[4:6] + '-'
        newDate += date[6:]
        return newDate   # Format: Year-Month-Day

    def __getQueryComponets(self, event_file_ID):

        # Function Description: Convert the eventID into the needed components to formulate a proper query.
        # Parameters: event_file_ID (The event ID from the EVN files)
        # Throws: ValueError (Thrown when the eventID is not of valid length)
        # Returns: [homeTeam, date, numGameInDay] (The needed information to complete the query)

        if len(event_file_ID) != 12:
            raise ValueError("ERROR: || Class -> Game_Driver || Function -> getQueryComponets || Reason -> Invalid event_file_ID. It is not the proper size.")
        homeTeam = event_file_ID[0:3]
        date = self.__convertDate(event_file_ID[3:-1])      # Format: Year-Month-Day
        numGameInDay = event_file_ID[-1]
        return [homeTeam, date, numGameInDay]        # Array of strings

    def check_game(self, game_Id):

        # Function Description: The function checks if the game exists in the game database.
        # Function Parameters: game_Id (The ID of the game to check within the database.)
        # Function Throws: Nothing
        # Function Returns: True or False (If the game is found, return True. Elsewise, return False.)

        query = "select Game_ID from game_day where Game_ID = \'" + game_Id + "\'"
        return bool(self.__dbConnect__.cursor().execute(query))

    def insert_game(self, game_Id, away_team):
        
        # Function Description: Insert the minimum requirements to a game record which include the game_Id (Formatted: TEX201504290), 
        # and the away team. Other parameters wil be derived from the Event_ID.
        # Function Parameters: game_id (The game ID from the Event files), away_team (The away team in the game)
        # Function Throws: None
        # Function Returns: True (A new game was successfully inserted) False (Nothing was inserted)

        parse_game_id = self.__getQueryComponets(game_Id)            # Returned as [homeTeam, date, numGameInDay]
        query = "INSERT IGNORE INTO game_day (Visiting_Team, Home_Team, Date, Game_ID, NumGameInDay) Values (\'" + away_team + "\', \'" + parse_game_id[0] + "\', \'" + parse_game_id[1] + "\', \'" + game_Id + "\', \'" + parse_game_id[2] + "\');"  
        cursor = self.__dbConnect__.cursor()                   
        filterwarnings('error')                                      # Convert warnings into exceptions to be caught.                   
        try:
            status = cursor.execute(query)                           # Execute Query: And close the cursor.
            self.__dbConnect__.commit()
        except Warning as warn:
            warn = str(warn)                                         # Ensure the warning is a duplicate entry warning to avoid data problems     
            warnNum = warn[1:5]                         
            if (warnNum != "1062"):                                  # An SQL Warning returning (1062, "Duplicate entry" ----- for key Primary)
                raise UnrecognisableMySQLBehaviour("ERROR: || Class -> Game_Driver || Function -> insertGame || Reason -> The warning was not the expected 'Duplicate Entry'. Please investigate to avoid data entry discrepancies.")
            status = 0
        filterwarnings('always')                        # Turn the filter for warnings back on.
        cursor.close()
        if (status == 1):
            return True
        return False               
