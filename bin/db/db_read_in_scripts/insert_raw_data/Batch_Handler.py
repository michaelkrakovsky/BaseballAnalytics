# Module Description: The module will  take in various data packates and conjugate them into multiple queues.
#    Each queue will be encapsulated in an outer shell that possesses the first half of the query and possibly
#    other metadata.
# Module Version: 1.0
# Module Author: Michael Krakovsky

from Driver import Driver

class Batch_Driver(Driver):

    def __init__(self, db_connection, max_size=1000):

        # Class Description: The function will manage all the individual batch queues. Note: The key identifying each Batch_Queue
        #    must match each table name.
        # Class Parameters: db_connection (The existing connection to the database.), 
        #    max_size (The point where we insert all the queues into the database.)
        
        Driver.__init__(self, db_connection)
        self.max_size = max_size
        self.queues = {}
        self.current_size = 0               # Manage the size of the queue. Empty the queue when it gets to large.

    def __empty_priority_queues(self):

        # Function Description: The function empties the priority queues first. (i.e. Game Table and the Event Table)
        # Function Parameters: Nothing
        # Function Throws: Nothing
        # Function Returns: Nothing
        game_query = "INSERT INTO Game_Day (Visiting_Team, Home_Team, Date, Game_ID, NumGameInDay) VALUES (%s, %s, %s, %s, %s)"
        event_query = """INSERT INTO Event_Instance (idEvent, Game_ID, Inning, Outs, Vis_Score, Home_Score, Event_Text, Event_Type, Batter_Event_Flag,
                 AB_Flag, Hit_Value, SH_Flag, SF_Flag, Outs_on_Play, Double_Play_Flag, Triple_Play_Flag, RBI_On_Play, Wild_Pitch_Flag, Passed_Ball_Flag, 
                 Fielded_By, Batted_Ball_Type, Bunt_Flag, Foul_Flag, Hit_Location, Num_Errors, Batter_Dest, Play_on_Batter, New_Game_Flag, End_Game_Flag)  
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
        if game_query in self.queues: 
            self.execute_many(game_query, self.queues[game_query])   # Combine the Game Day queries first.
            self.queues[game_query] = []                             # Reset the list
        if event_query in self.queues: 
            self.execute_many(event_query, self.queues[event_query])       # Combine the Event Instance queries second.
            self.queues[event_query] = []

    def empty_batch_driver(self):

        # Function Description: The function will empty all of its contents into the database.
        # Function Parameters: Nothing
        # Function Throws: Nothing
        # Function Returns: Nothing

        self.__empty_priority_queues()
        for q in self.queues: 
            self.execute_many(q, self.queues[q])          # Combine empty the remaining Queues.
            self.queues[q] = []
        self.current_size = 0

    def add_query(self, key_name, query):

        # Function Description: Add the query to the appropriate queue.
        # Function Parameters: key_name (The name of the table and the identifier to the queue.)
        #    query (The query to be executed. This can also be a list of queries to execute.)
        # Function Throws: Nothing
        # Function Returns: Nothing

        if (self.current_size + 1) >= self.max_size: self.empty_batch_driver()     # Ensure there is enough space and then add the queries.
        if key_name not in self.queues: self.queues[key_name] = []
        q = self.queues[key_name]
        q.append(query)
        self.current_size += 1

