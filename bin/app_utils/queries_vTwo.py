# Script Description: The script will contain queries that can be used across functions. All one needs to input is a connection to the database.
# Script Version: 2.0

from pymysql import connect
from warnings import filterwarnings
from BaseballAnalytics.bin.app_utils.common_help import Log_Helper
from re import search
from pickle import load, dump
from timeit import default_timer as timer

class Queries():

    def __init__(self, db_connection):

        # Class Description: The class will provide accessible and reuseable queries accross stages.
        # Class Instantiators: db_connection (pymysql.connections.Connection: The connection to the database.)

        if (str(type(db_connection)) == '<class \'pymysql.connections.Connection\'>'):
            self.__db_connection__ = db_connection
        else:
            raise ValueError("The user did not provide the correct pymysql connector.")

    def fetch_data(self, query):

        # Function Description: Retrieve all the data given a particular query.
        # Function Parameters: query (The query to execute in the database.)
        # Function Throws: Nothing
        # Function Returns: The contents from the query.
        
        filterwarnings('error')    
        try:
            with self.__db_connection__.cursor() as c:
                c.execute(query)
                filterwarnings('always')
                return c.fetchall()
        except Exception as ex:
            print("The expections {}".format(ex))
            print("The query {}".format(query))
            raise Exception("A fire is buring in fetch_data.")

    def convert_query_to_dict(self, data):
        
        # Function Description: Convert the data from a query into a dictionay to be indexed.
        #    The game id MUST BE the first value in the column.
        # Function Parameters: data (The data that was extractred from the query.)
        # Function Throws: Nothing
        # Function Returns: The dictionary containing a list of events associated with the Game Id
        
        query_dict = {}
        for row in data:
            if row[0] not in query_dict:
                query_dict[row[0]] = [list(row[1:])]
            else:
                game_list = query_dict[row[0]]
                game_list.append(list(row[1:]))
        return query_dict

    def get_game_outcomes(self, day=1, month=1):

        # Function Description: The function will retrieve the game outcomes with the date formatted in separated columns. In addition, 
        #    the user will have the option to filter out games before a specific day in the year. If no options are included, no filtering
        #    will be executed.
        # Function Parameters: Nothing
        # Function Throws: Nothing
        # Function Returns: The list of game ids with the associated outcomes and dates. 
        #     (Game_ID, year, day, month, Home_Score, Vis_Score, Home_Team, Visitng_Team, Home_Win) where a winning home team is flagged at 0.

        return list(self.fetch_data("""select event_instance.Game_ID, year(game_day.Date) as Year, day(game_day.Date) as Day, 
                                month(game_day.Date) as Month, event_instance.Home_Score, 
                                event_instance.Vis_Score, game_day.Home_Team, game_day.Visiting_Team,
                                (case when event_instance.Vis_Score > event_instance.Home_Score then 1 else 0 end) as Home_Win
                                        from event_instance
                                        inner join game_day on event_instance.Game_ID=game_day.Game_ID 
                                        where event_instance.End_Game_Flag = 'T'
                                        and not (day(game_day.Date) < {} and month(game_day.Date) < {})
                                        order by game_day.Date, game_day.Game_ID;""".format(day, month)))

    def org_by_player_then_game(self, features):

        # Function Description: The function will organise a raw query into a dictionary of lists. The lists within the dictionary are organised from oldest to greatest.
        # Function Parameters: features (The features that must be organised. Note, the Game_ID must be located in the first column 
        #    while the player_id is located in the second column.)
        # Function Throws: Nothing
        # Function Returns: The dictionary of lists where the GameID within the list are ordered.

        org_features = {}
        for feature in features:                 # Create the dict of lists of lists where lists are stored as uner the player id.
            player_id = feature[1]
            if player_id not in org_features: 
                org_features[player_id] = [[feature[0]] + [float(i) for i in feature[2:]]]         # Intiate the first player value.
            else: 
                temp_list = org_features[player_id]
                temp_list.append([feature[0]] + [float(i) for i in feature[2:]])                   # Append to that order.
        return org_features

    def unpack_pitchers(self, pitcher_query):

        """# Function Description: The function will perform basic exploratory observations within the pitchers data structure.
        # Function Parameters: pitcher_query (The pitcher dictionary with all the pitcher names.)
        # Function Throws: Nothing
        # Function Returns: Nothing - The function will print information about the query structure.""" 

        for team in pitcher_query:
            all_team = pitcher_query[team]
            for year in all_team:
                all_year = all_team[year]
                for game in all_year:
                    all_game = all_year[game]
                    for event in all_game:
                        print("An Event {}".format(event))
                        break
                    print("Num Events {}".format(len(all_game)))
                    break
                print("Num Games {}".format(len(all_year)))
                break
            print("Num Years {}".format(len(all_team)))
            break
        print("Num Teams {}".format(len(pitcher_query)))

    def add_event(self, team, year, query_dict, game_id, pitcher_name, event_id):

        """# Function Description: The function will add the pitcher names to the game event.
        # Function Parameters: team (The team to add the event.),
        #    year (The year that was played.) 
        #    query_dict (The dictionary that holds all the events.), 
        #    game_id (The game id the event is associated with.), 
        #    pitcher_name (The pitcher name that was in the event.), 
        #    event_id (The name of the event id.)
        # Function Throws: Nothing
        # Function Returns: Nothing - But it will modify a dictionary to hold game ids each with the home pitchers and away pitchers.
        #    {team : {year : {game_id : [pitcher_name, event_id]}}}"""    
        
        if team not in query_dict:                                              # A team does not exist, create a team. 
            query_dict[team] = {year : {game_id : [[pitcher_name, event_id]]}}     
        else:
            team_year = query_dict[team]
            if year not in team_year:                                           # A year does not exist, create a year.
                team_year[year] = {game_id : [[pitcher_name, event_id]]}
            else:
                year_games = team_year[year]
                if game_id not in year_games:                                   # A game does not exist, create a game.
                    year_games[game_id] = [[pitcher_name, event_id]]
                else:
                    year_games[game_id].append([pitcher_name, event_id])

    def pitcher_query_to_dict(self, data):
        
        """# Function Description: Convert the data from a query into a dictionay to be indexed.
        #    The game id MUST BE the first value in the column.
        # Function Parameters: data (The data that was extractred from the query.)
        # Function Throws: Nothing
        # Function Returns: The dictionary containing a list of events associated with the Game Id."""
        
        query_dict = {}
        for row in data:
            game_id = row[0]
            year = row[1]
            batting_team = row[4]
            home_team = row[5]
            vis_team = row[6]
            pitcher_name = row[7]
            event_id = row[8]
            if batting_team == 0:                        # Add home pitchers to the proper game depending on home team or away team. Home Team = 1
                self.add_event(home_team, year, query_dict, game_id, pitcher_name, event_id)     # We need to invert the outcomes. If the away team is batting, then the home team is pitching.
            else:
                self.add_event(vis_team, year, query_dict, game_id, pitcher_name, event_id)
        return query_dict

    def get_pitchers_in_all_games(self, query_loc, get_again_flag=False):

        """# Function Description: Retrieve the list of all pitchers who participated in every game.
        # Function Parameters: query_loc (The location of results of previous queries.), 
        #    get_again_flag (The function will talk to the database once again and replace the results. (CI))
        # Function Throws: Nothing
        # Function Returns: A dictionary with the game ids as keys storing the pitchers who participates."""

        # Home Team equals 1 for Batting Team. The query is formatted like such: 
        #     Game_ID, Batter_Name, Batting_Team, idEvent

        if get_again_flag == False:                  # Check if the query was executed before prior to performing another query.
            with open(query_loc, 'rb') as f:
                data = load(f)
                return self.pitcher_query_to_dict(data)
        game_participants = self.fetch_data("""select event_instance.Game_ID, Year(game_day.date) as Year, Day(game_day.date) as Day,
                                            Month(game_day.date) as Month, batter_in_event.Batting_Team,
                                            game_day.Home_Team, game_day.Visiting_Team,
                                            pitcher_in_event.Pitcher_Name, pitcher_in_event.idEvent
                                            from event_instance
                                            inner join pitcher_in_event on pitcher_in_event.idEvent=event_instance.idEvent
                                            inner join batter_in_event on batter_in_event.idEvent=event_instance.idEvent
                                            inner join game_day on game_day.Game_ID=event_instance.Game_ID
                                    """)
        with open(query_loc, 'wb') as f: dump(game_participants, f)
        return self.pitcher_query_to_dict(game_participants)

    def process_game(self, game_events):

        """Function Description: Process a game by capturing all the pitchers who participated for the team.
        Function Parameters: game_events (The events related to the specific game.)
        Function Throws: Nothing
        Function Returns: A dictionary formatted like such. {pitcher_name : [num_instances, apearance_in_game]}"""

        game_events.sort(key=lambda x: int(search(r'\d+', x[1][:3]).group()))      # Sort the string by the leading numbers of each id.
        game_profile = {}
        num_instance = 1
        for event in game_events:
            pitcher_name = event[0]
            if pitcher_name not in game_profile:                                   # If a new pitcher is observed, add it to the dictionary.
                game_profile[pitcher_name] = [1, num_instance]
                num_instance += 1
            else:
                game_profile[pitcher_name][0] += 1
        return game_profile 

    def add_pitcher_to_dict(self, dictionary, pitcher, innings):

        """Function Description: Add a pitcher to the dictionary related to the aggregation function.
        Function Parameters: dictionary (The dictionary to add the pitcher.), 
            pitcher (The pitcher to be added.), innings The innings the pitcher plays.
        Function Throws: Nothing
        Function Returns: Nothing
        """
        if pitcher not in dictionary:
            dictionary[pitcher] = innings
        else:
            dictionary[pitcher] += innings

    def order_pitchers(self, pitcher_appearences):

        """Function Description: Order the pitchers from most innings played to least.
        Function Parameter: pitcher_appearences (The dictionary of pitchers who participated in the games.)
        Function Throws: Nothing
        Function Returns: The list of pitchers."""

        # TO OPTIMISE: IMPLEMENT A MAX HEAP TO REDUCE O(n^2) to O(n)
        pitchers = []
        for _ in range(0, len(pitcher_appearences)):
            max = 0
            max_pitcher = ""
            for pitcher, num in pitcher_appearences.items():
                if num > max:
                    max = num
                    max_pitcher = pitcher
            pitchers.append(max_pitcher)
            del pitcher_appearences[max_pitcher]
        return pitchers

    def get_pitchers_in_window(self, games):

        """Function Description: Given the pitchers in a window, determine the entire pitching roster.
        Function Parameters: games (The games to be processed.)
        Function Throws: Nothing
        Function Returns: A tuple of lists containing the pitchers ordered by number of innings played.
            The first element contains the starting pitchers. The second element contains the relief pitchers."""

        starter_total_innings = {}
        relief_total_inings = {}
        for game in games:
            game_pitchers = game[1]                                                   # Here are the pitchers in the game.
            for pitcher in game_pitchers:                                             # Aggregate the pitchers within the rosters by number of appearances and position.
                if game_pitchers[pitcher][1] == 1:                                    # If the appearance number equals 1, then it is a starting pitcher. 
                    self.add_pitcher_to_dict(starter_total_innings, pitcher, game_pitchers[pitcher][0])
                else:
                    relief_total_inings[pitcher] = game_pitchers[pitcher][0]
        return (self.order_pitchers(starter_total_innings), self.order_pitchers(relief_total_inings)) 

    def get_unique_relief_pitchers(self, starting_pitchers, relief_pitchers):

        """Function Description: Only retrieve pitchers that are dedicated relief pitchers.
        Function Parameters: starting_pitchers (The pitchers who started in the window size.), 
            relief_pitchers (Pitchers who were relievers in the window size.)
        Function Throws: Nothing
        Function Returns: Pitchers that only existed as relief pitchers."""

        only_relief = []
        for relief in relief_pitchers:
            if relief not in starting_pitchers:
                only_relief.append(relief)
        return only_relief

    def tie_relievers_to_games(self, relief_games, relief_profile, games, team):

        """Function Description: Prepare the data in which it can be shipped to the model.
        Function Parameters: relief_games (The existing dictionary containing the relief pitchers.)
            relief_profile (The final relief pitchers to be appended to the model.), 
            games (The games that was used within the model.), 
            team (The team that contains the relief pitchers.)
        Function Throws: Nothing
        Function Returns: A dictionary containing the games and the pitchers who participated. {game_id : [relief_pitchers]}"""

        for game in games:
            if game[0] not in relief_games:
                relief_games[game[0]] = {team : relief_profile}
            else:
                relief_games[game[0]][team] = relief_profile
        return relief_games

    def process_year(self, year_games, relief_games, team, window_size=40):

        """Function Description: Process a year of players compiling all the rosters into their respective windows.
        Function Parameters: year_games (The dictionary containing all the games and their events), 
            team (The team that contains the relief pitchers.)
            window_size (The size of the window to consolidate all the players.)
        Function Throws: Nothing
        Function Returns: A dictionary containing the games and the expected roster. {game_id : {pitcher_one, pitcher_two, ..., pitcher_n}}"""

        agg_pitchers = [[game_id, self.process_game(year_games[game_id])] for game_id in year_games]
        agg_pitchers.sort(key=lambda x: x[0][3:])        # Sort the string by the ending game digits.
        window_min = 0
        window_max = window_size
        while window_max <= len(year_games):             # Find the pitchers on the roster within the desired time frame.
            if (162 - window_max) < 20:                  # Just add the final games as to not create a small window.
                window_max = len(year_games)
            starting_pitchers, relief_pitchers = self.get_pitchers_in_window(agg_pitchers[window_min:window_max])
            relief_pitchers = self.get_unique_relief_pitchers(starting_pitchers, relief_pitchers)
            self.tie_relievers_to_games(relief_games, relief_pitchers, agg_pitchers[window_min:window_max], team)
            window_min = window_max
            window_max += window_size                    # We will eventually get out of the loop with these increments.
        
    def get_relief_pitchers(self, pitchers, window_size=40):

        """# Function Description: Retrieve all the pitchers who participated on the teams starting lineup.
            The function will all correct for the fewest number of players to appear in the games. For instance, 
            if only three relievers participated in the last n games, then all profiles will contain the top three most prevelant relievers.
        # Function Parameters: pitchers (The dictionary containing all the pitchers.), 
        #    window_size (The pitchers on the roster within the specified timeframe.)
        # Function Throws: Nothing
        # Function Returns: A dictionary containing the pitcher names within the specified time frame."""

        relief_games = {}
        for team in pitchers:
            for year in pitchers[team]:
                self.process_year(pitchers[team][year], relief_games, team, window_size)
        num_relievers = []
        for game in relief_games:                    # Find the number of relievers in all window sizes.
            for team in relief_games[game]:
                if len(relief_games[game][team]) not in num_relievers:
                    num_relievers.append(len(relief_games[game][team]))
        num_relievers = min(num_relievers)
        print("The number of relievers to contian: {}".format(num_relievers))
        new_relief_pitchers = {}                     # Ensure all relievers in the games are the same.
        for game in relief_games:
            for team in relief_games[game]:
                if game not in new_relief_pitchers:
                    new_relief_pitchers[game] = {team : relief_games[game][team][:num_relievers]}
                else:
                    new_relief_pitchers[game][team] = relief_games[game][team][:num_relievers]
        return new_relief_pitchers

    def get_starting_pitchers(self, pitchers):

        """# Function Description: Get starting pitchers from all games from both away and home teams.
        # Function Parameters: pitchers (The dictionary containing all the pitchers.), 
        # Function Throws: Nothing
        # Function Returns: A dictionary containing the starting pitchers attatched to each game id."""

        starting_pitchers = {}
        for team in pitchers:
            for year in pitchers[team]:
                for game_id in pitchers[team][year]:
                    game_events = pitchers[team][year][game_id].copy() 
                    game_events.sort(key=lambda x: int(search(r'\d+', x[1][:3]).group()))      # Sort the string by the leading numbers of each id.
                    if game_id not in starting_pitchers:
                        starting_pitchers[game_id] = {team : game_events[0][0]}                # The first event will contain the starting pitcher.
                    else:
                        starting_pitchers[game_id][team] = game_events[0][0] 
        return starting_pitchers

    def get_batters(self, query_loc, get_again_flag=False):

        # Function Description: The function returns only the players and the starting pitcher with the respective game ids. This will be the first attempt of gathering
        #    the starting lineup.
        # Function Parameters: query_loc (The location of results of previous queries.), 
        #    get_again_flag (The function will talk to the database once again and replace the results. (CI))
        # Function Throws: Nothing
        # Function Returns: A tuple containing two lists. The first list contains the home team names while the second list contains the away teams.

        # Home Team equals 1 for Batting Team. The query is formatted like such: 
        #     Game_ID, Batter_Name, Batting_Team, idEvent
        
        if get_again_flag == False:                  # Check if the query was executed before prior to performing another query.
            with open(query_loc, 'rb') as f:
                data = load(f)
                return self.convert_query_to_dict(data)
        game_participants = self.fetch_data("""select event_instance.Game_ID, batter_in_event.Batter_Name, 
                                        batter_in_event.Batting_Team, batter_in_event.idEvent 
                                        from batter_in_event 
                                        inner join event_instance on batter_in_event.idEvent=event_instance.idEvent
                                    """)
        with open(query_loc, 'wb') as f:
            dump(game_participants, f)
        return self.convert_query_to_dict(game_participants)

    def get_all_offensive_features(self, query_loc, get_again_flag=False):

        # Function Description: Retrieve the features all batters after the specified game id.
        # Function Parameters: query_loc (The location of results of previous queries.), 
        #    get_again_flag (The function will call the database overwriting the results. (CI))
        # Function Throws: Nothing
        # Function Returns: A list containing the offensive features. The amount of features was determined in previous queries but does not matter in this function.
        #    If the player does not have much data, I will be returning -1 to signal the prescence of a new player.

        if get_again_flag == False:                  # Use the information already provided.
            with open(query_loc, 'rb') as f:
                data = load(f)
                return self.org_by_player_then_game(data)
        # Else, execute the query and recalulate.
        features = self.fetch_data("""                        
                                select offensive_features.Game_ID, offensive_features.player_id, 
                                Ten_Rolling_OBP, Ten_Rolling_SLG from offensive_features inner join
                                game_day on game_day.Game_ID=offensive_features.Game_ID
                                order by game_day.Date asc
                                """)        
        with open(query_loc, 'wb') as f: dump(features, f)
        return self.org_by_player_then_game(features)

    def get_all_pitching_features(self, query_loc, get_again_flag=False):

        # Function Description: Retrieve the features all pitchers after the specified game id.
        # Function Parameters: query_loc (The location of results of previous queries.), 
        #    get_again_flag (The function will call the database overwriting the results. (CI))
        # Function Throws: Nothing
        # Function Returns: A list containing the offensive features. The amount of features was determined in previous queries but does not matter in this function.
        #    If the player does not have much data, I will be returning -1 to signal the prescence of a new player.

        if get_again_flag == False:                  # Use the information already provided.
            with open(query_loc, 'rb') as f:
                data = load(f)
                return self.org_by_player_then_game(data)
        # Else, execute the query and recalulate.
        features = self.fetch_data("""                        
                                select pitching_features.Game_ID, pitching_features.player_id,
                                Ten_Rolling_Ks, Ten_Rolling_WHIP, Ten_Rolling_RA from pitching_features inner join
                                game_day on game_day.Game_ID=pitching_features.Game_ID
                                order by game_day.Date Asc;
                                """)        
        with open(query_loc, 'wb') as f: dump(features, f)
        return self.org_by_player_then_game(features)