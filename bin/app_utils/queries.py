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

    def get_all_player_ids(self):

        # Function Description: Retrieve the entire list of players from the data base.
        # Function Parameters: Nothing
        # Function Throws: Nothing
        # Function Returns: The entire list of players existing within the database.

        return self.fetch_data('select player_information.player_id from player_information;')

    def get_all_game_ids(self):

        # Function Description: Retrieve all the game ids from the database in preparation for modelling. Ensure the proper ordering is present.
        # Function Parameters: Nothing
        # Function Throws: Nothing
        # Function Returns: The list of game ids within the database ordered by date.

        return self.fetch_data('select game_day.Game_ID, year(game_day.Date), day(game_day.Date), month(game_day.Date) from game_day order by game_day.Date, game_day.Game_ID;')

    def get_game_outcomes(self):

        # Function Description: The function will retrieve the game outcomes with the date in separated columns.
        # Function Parameters: Nothing
        # Function Throws: Nothing
        # Function Returns: The list of game ids with the associated outcomes and dates. 
        #     (Game_ID, year, day, month, Home_Score, Vis_Score, Home_Team, Visitng_Team, Home_Win) where a winning home team is flagged at 0.

        return self.fetch_data("""select event_instance.Game_ID, year(game_day.Date), day(game_day.Date), month(game_day.Date), event_instance.Home_Score, 
                                  event_instance.Vis_Score, game_day.Home_Team, game_day.Visiting_Team,
                                  (case when event_instance.Vis_Score > event_instance.Home_Score then 1 else 0 end) as Home_Win
                                        from event_instance
                                        inner join game_day on event_instance.Game_ID=game_day.Game_ID 
                                        where event_instance.End_Game_Flag = 'T'
                                        order by game_day.Date, game_day.Game_ID;""")

    def get_only_outcomes(self):

        # Function Description: The function returns only the outputs given the same conditions of the query in get_game_outcomes above. This ensures consistancy and allows the user to inspect the 
        #    outcomes prior to only desiring the outcomes.
        # Function Parameters: Nothing
        # Function Throws: Nothing
        # Function Returns: The list of game outcomes as 0s and 1s where a winning home team is flagged at 0.

        outcomes = self.fetch_data("""select (case when event_instance.Vis_Score > event_instance.Home_Score then 1 else 0 end) as Home_Win
                                from event_instance
                                inner join game_day on event_instance.Game_ID=game_day.Game_ID 
                                where event_instance.End_Game_Flag = 'T'
                                order by game_day.Date, game_day.Game_ID;""")
        list_outcomes = []
        for outcome in outcomes:
            list_outcomes.append(outcome[0])
        return list_outcomes

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
                org_features[player_id] = [[feature[0], float(feature[2]), float(feature[3]), float(feature[4])]]     # Intiate the first player value.
            else: 
                temp_list = org_features[player_id]
                temp_list.append([feature[0], float(feature[2]), float(feature[3]), float(feature[4])])               # Append to that order.
        return org_features

    def get_starting_pitcher(self, pitchers, game_id, team_batting):

        # Function Description: Givin all the batting events in a game, extract the starting the lineup.
        # Function Parameters: batting_players (The dictionary containing all the events from all games.), 
        #    game_id (The game id you wish to extract the betting lineup.), team_batting (The batting team: The Visting Team is 0, the Home Team is 1.)
        # Function Throws: Nothing
        # Function Returns: The list of players in the batting lineup.

        isolate_pitchers = [(team, player_id, e_id) for team, player_id, e_id in pitchers[game_id] if team == team_batting]     # Return only the first name for now.
        isolate_pitchers.sort(key=lambda x: int(search(r'\d+', x[2][:3]).group()))
        return isolate_pitchers[0][1]

    def get_players_in_game_vOne(self, game_id):

        # Function Description: The function returns only the players and the starting pitcher with the respective game ids. This will be the first attempt of gathering
        #    the starting lineup.
        # Function Parameters: game_id (The game_id you wish to use to get the game participants.)
        # Function Throws: Nothing
        # Function Returns: A tuple containing two lists. The first list contains the home team names while the second list contains the away teams.

        # Home Team equals 1 for Batting Team. The query is formatted like such: 
        #     Game_ID, Batting_Team, Pitcher_Name, Catcher, Center_Field, Left_Field, Right_Field, First_Base, Second_Base, Third_Base, Shortstop
        game_participants = self.fetch_data("""
                                            select Distinct game_day.Game_ID, batter_in_event.Batting_Team, pitcher_in_event.Pitcher_Name,       
                                            event_catcher.Catcher, event_centre_field.Center_Field, event_left_field.Left_Field,
                                            event_right_field.Right_Field, event_first_base.First_Base, event_second_base.Second_Base, 
                                            event_third_base.Third_Base, event_shortstop.Shortstop
                                                from game_day
                                                inner join event_instance on game_day.Game_ID=event_instance.Game_ID
                                                inner join batter_in_event on event_instance.idEvent=batter_in_event.idEvent
                                                inner join pitcher_in_event on pitcher_in_event.idEvent=event_instance.idEvent
                                                inner join event_catcher on event_catcher.idEvent=event_instance.idEvent
                                                inner join event_centre_field on event_centre_field.idEvent=event_instance.idEvent
                                                inner join event_left_field on event_left_field.idEvent=event_instance.idEvent
                                                inner join event_right_field on event_right_field.idEvent=event_instance.idEvent
                                                inner join event_first_base on event_first_base.idEvent=event_instance.idEvent
                                                inner join event_second_base on event_second_base.idEvent=event_instance.idEvent
                                                inner join event_third_base on event_third_base.idEvent=event_instance.idEvent
                                                inner join event_shortstop on event_shortstop.idEvent=event_instance.idEvent
                                                where event_instance.Game_ID = '{}' order by batter_in_event.batting_team, CHAR_LENGTH(event_instance.idEvent), event_instance.idEvent;
                                                """.format(game_id))
        game_vistors = game_participants[0][2:]                             # Given the query conditions, this will always provide the starting lineups.
        for loc, part in enumerate(game_participants):
            if part[1] == 1:
                game_homers = game_participants[loc][2:]                      # This will provide the values of the home team. Once retrieved, we have all what we need.
                break
        return (game_vistors, game_homers)

    def get_all_offensive_features(self, query_loc, get_again_flag=False):

        # Function Description: Retrieve the features of a given player prior to entering the new game. The features are available from the previous game.
        # Function Parameters: query_loc (The location of results of previous queries.), 
        #    get_again_flag (The function will talk to the database once again and place the results. (CI))
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
                                Ten_Rolling_BA, Ten_Rolling_OBP, Ten_Rolling_SLG from offensive_features inner join
                                game_day on game_day.Game_ID=offensive_features.Game_ID
                                order by game_day.Date asc
                                """)        
        with open(query_loc, 'wb') as f: dump(features, f)
        return self.org_by_player_then_game(features)

    def get_starting_batters(self, batting_players, game_id, team_batting):

        # Function Description: Givin all the batting events in a game, extract the starting the lineup.
        # Function Parameters: batting_players (The dictionary containing all the events from all games.), 
        #    game_id (The game id you wish to extract the betting lineup.), team_batting (The batting team: The Visting Team is 0, the Home Team is 1.)
        # Function Throws: Nothing
        # Function Returns: The list of players in the batting lineup.
                                                        
        filter_team = [(g_id, team, e_id) for g_id, team, e_id in batting_players[game_id] if team == team_batting] 
        filter_team.sort(key=lambda x: int(search(r'\d+', x[2][:3]).group()))      # Sort the string by the leading numbers of each id.
        player_count = 0                                                           # Add the first unique 9 players found in the event lineup.
        player_lineup = []
        for tup in filter_team:
            if tup[0] not in player_lineup: 
                player_lineup.append(tup[0])
                player_count += 1
            if player_count >= 9: break                     # Exit the loop when you have all the players.
        return player_lineup

    def get_batters_in_all_games_vOne(self, query_loc, get_again_flag=False):

        # Function Description: The function returns only the players and the starting pitcher with the respective game ids. This will be the first attempt of gathering
        #    the starting lineup.
        # Function Parameters: query_loc (The location of results of previous queries.), 
        #    get_again_flag (The function will talk to the database once again and replace the results. (CI))
        # Function Throws: Nothing222
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

    def get_pitchers_in_all_games_vOne(self, query_loc, get_again_flag=False):

        # Function Description: Retrieve the list of all pitchers who participated in every game.
        # Function Parameters: query_loc (The location of results of previous queries.), 
        #    get_again_flag (The function will talk to the database once again and replace the results. (CI))
        # Function Throws: Nothing
        # Function Returns: A dictionary with the game ids as keys storing the pitchers who participates.

        # Home Team equals 1 for Batting Team. The query is formatted like such: 
        #     Game_ID, Batter_Name, Batting_Team, idEvent
        
        if get_again_flag == False:                  # Check if the query was executed before prior to performing another query.
            with open(query_loc, 'rb') as f:
                data = load(f)
                return self.convert_query_to_dict(data)
        game_participants = self.fetch_data("""select DISTINCT event_instance.Game_ID, batter_in_event.Batting_Team, 
                                        pitcher_in_event.Pitcher_Name, pitcher_in_event.idEvent
                                            from event_instance
                                            inner join pitcher_in_event on pitcher_in_event.idEvent=event_instance.idEvent
                                            inner join batter_in_event on batter_in_event.idEvent=event_instance.idEvent
                                    """)
        with open(query_loc, 'wb') as f:
            dump(game_participants, f)
        return self.convert_query_to_dict(game_participants)

    def get_offensive_features(self, offensive_features, player_id, game_id):

        # Function Description: Retrieve the features of a given player prior to entering the new game. The features are available from the previous game.
        # Function Parameters: player_id (The player id associated in which we wish to retrieve the data.), game_id (The game id needed to look backwards.)
        # Function Throws: Nothing
        # Function Returns: A list containing the offensive features. The amount of features was determined in previous queries but does not matter in this function.
        #    If the player does not have much data, I will be returning -1 to signal the prescence of a new player.

        player_stats = offensive_features[player_id]
        if len(player_stats) < 4:                          # Not enough games played to create reasonable stats.
            return [-1, -1, -1]
        for idx, games in enumerate(player_stats):
            if games[0] == game_id:
                return player_stats[idx - 1][1:]           # Return the stats from the day before. Should we particularily focus on a seaosn? Should things get a rest?

    def get_pitchers_features(self, player_id, game_id):

        # Function Description: Retrieve the features of a given pitcher prior to entering the new game. The features are available from the previous game.
        # Function Parameters: player_id (The player id associated in which we wish to retrieve the data.), game_id (The game id needed to look backwards.)
        # Function Throws: Nothing
        # Function Returns: A list containing the offensive features. The amount of features was determined in previous queries but does not matter in this function.
        #    If the player does not have much data, I will be returning -1 to signal the prescence of a new player.

        features = self.fetch_data("""
                                    select Ten_Rolling_Ks, Ten_Rolling_WHIP, Ten_Rolling_RA from pitching_features inner join
                                    game_day on game_day.Game_ID=pitching_features.Game_ID
                                    where player_id = '{}'
                                    and game_day.Date < (select game_day.Date from game_day where game_day.Game_ID = '{}')
                                    order by game_day.Date Desc;
                                    """.format(player_id, game_id))
        if len(features) < 2:                              # I reduced the number of previous games for pitcher by half.
            return [-1, -1, -1]
        return list(features[0])                           # Return the first row which contains the data from the previous day.                         # Return the first row which contains the data from the previous day.

    def sub_pitching_features(self, pitchers, game_id):

        # Function Description: Substitute the pitcher ids provided with the pitching features. The features will be returned in the same order the names are provided.
        # Function Parameters: pitchers (The player id we wish to retrieve the data for.), game_id (The game id needed to look backwards.) 
        # Function Throws: Nothing
        # Function Returns: A complete list of the featues to be inputted into the model. The list will vary depending on the number of players and features for each player.

        pitcher_features = []
        for pitcher in pitchers:
            pitcher_features += self.get_pitchers_features(pitcher, game_id)
        return [float(feat) for feat in pitcher_features]

    def sub_offensive_features(self, offensive_features, batters, game_id):

        # Function Description: Substitute the batters ids provided with the batting features. The features will be returned in the same order the names are provided.
        # Function Parameters: offensive_features (The dictionary containing the player ids that are tied to the offensive features.) 
        #    batters (The player id we wish to retrieve the data for.), game_id (The game id needed to look backwards.) 
        # Function Throws: Nothing
        # Function Returns: A complete list of the featues to be inputted into the model. The list will vary depending on the number of players and features for each player.

        game_offensive_features = []
        for batter in batters:
            game_offensive_features += self.get_offensive_features(offensive_features, batter, game_id)
        return game_offensive_features

    def get_game_features(self, all_batters, all_pitcher, offensive_features, game_id):

        # Function Description: Get all the features for a given game id. This involves getting the players who played in the game and then retrieving their associated features.
        # Function Parameters: all_batters (All of the batters information.) all_pitcher (All of the pitchers information.), 
        #     offensive_features (All of the offensive features that are used to predict outcome.), 
        #     game_id (The game id used to acquire the player features.)
        # Function Throws: Nothing
        # Function Returns: A single list containing the features of the game.

        game_features = []
        home_players = [self.get_starting_pitcher(all_pitcher, game_id, 0)]
        home_players += self.get_starting_batters(all_batters, game_id, 1)
        game_features += self.sub_pitching_features([home_players[0]], game_id)       # Substitute the player names for their features.
        game_features += self.sub_offensive_features(offensive_features, home_players[1:], game_id)
        vis_players = [self.get_starting_pitcher(all_pitcher, game_id, 1)]            # Vice versa.
        vis_players += self.get_starting_batters(all_batters, game_id, 0)
        game_features += self.sub_pitching_features([vis_players[0]], game_id)
        game_features += self.sub_offensive_features(offensive_features, vis_players[1:], game_id)
        if len(game_features) != 60: raise ValueError("The correct number of features was not returned.")
        return game_features
