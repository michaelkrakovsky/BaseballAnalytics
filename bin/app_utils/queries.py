# Script Description: The script will contain queries that can be used across functions. All one needs to input is a connection to the database.
# Script Version: 1.0

from pymysql import connect
from warnings import filterwarnings
from BaseballAnalytics.bin.app_utils.common_help import Log_Helper

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

    def get_offensive_features(self, player_id, game_id):

        # Function Description: Retrieve the features of a given player prior to entering the new game. The features are available from the previous game.
        # Function Parameters: player_id (The player id associated in which we wish to retrieve the data.), game_id (The game id needed to look backwards.)
        # Function Throws: Nothing
        # Function Returns: A list containing the offensive features. The amount of features was determined in previous queries but does not matter in this function.
        #    If the player does not have much data, I will be returning -1 to signal the prescence of a new player.

        features = self.fetch_data("""
                                    select Ten_Rolling_BA, Ten_Rolling_OBP, Ten_Rolling_SLG from offensive_features inner join
                                    game_day on game_day.Game_ID=offensive_features.Game_ID
                                    where player_id = '{}'
                                    and game_day.Date < (select game_day.Date from game_day where game_day.Game_ID = '{}')
                                    order by game_day.Date Desc;
                                    """.format(player_id, game_id))
        if len(features) < 10:
            return [-1, -1, -1]
        return list(features[0])                           # Return the first row which contains the data from the previous day.

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
        if len(features) < 5:                              # I reduced the number of previous games for pitcher by half.
            return [-1, -1, -1]
        return list(features[0])                           # Return the first row which contains the data from the previous day.

    def sub_pitching_features(self, pitchers, game_id):

        # Function Description: Substitute the pitcher ids provided with the pitching features. The features will be returned in the same order the names are provided.
        # Function Parameters: pitchers (The player id we wish to retrieve the data for.), game_id (The game id needed to look backwards.) 
        # Function Throws: Nothing
        # Function Returns: A complete list of the featues to be inputted into the model. The list will vary depending on the number of players and features for each player.

        pitcher_features = []
        for pitcher in pitchers:
            pitcher_features = pitcher_features + self.get_pitchers_features(pitcher, game_id)
        return pitcher_features

    def sub_offensive_features(self, batters, game_id):

        # Function Description: Substitute the batters ids provided with the batting features. The features will be returned in the same order the names are provided.
        # Function Parameters: batters (The player id we wish to retrieve the data for.), game_id (The game id needed to look backwards.) 
        # Function Throws: Nothing
        # Function Returns: A complete list of the featues to be inputted into the model. The list will vary depending on the number of players and features for each player.

        offensive_features = []
        for batter in batters:
            offensive_features = offensive_features + self.get_offensive_features(batter, game_id)
        return offensive_features

    def get_game_features(self, game_id):

        # Function Description: Get all the features for a given game id. This involves getting the players who played in the game and then retrieving their associated features.
        # Function Parameters: game_id (The game id used to acquire the player features.)
        # Function Throws: Nothing
        # Function Returns: A single list containing the features of the game.

        game_features = []
        vis_players, home_players = self.get_players_in_game_vOne(game_id)
        game_features += self.get_pitchers_features(vis_players[0], game_id) 
        for player_id in vis_players[1:]:                                             # Add all the visitor players to the feature sets.
            game_features += self.get_offensive_features(player_id, game_id)   
        game_features += self.get_pitchers_features(home_players[0], game_id) 
        for player_id in home_players[1:]:
            game_features += self.get_offensive_features(player_id, game_id)          # Add all the home players to the feature sets.
        return game_features

    def get_all_game_features(self, game_ids):

        # Function Description: Given a list of game ids, retrieve the features for every game.
        # Function Parameters: game_ids (The list of game ids.)
        # Function Throws: Nothing
        # Function Returns: A list of lists containing the game features.

        num_games = len(game_ids)
        all_game_features = {}
        lh = Log_Helper()
        lh.print_progress_bar(0, num_games, prefix = 'Progress:', suffix = 'Complete', length = 50)           # Initial call to print 0% progress
        for num, game_id in enumerate(game_ids):
            all_game_features[game_id] = self.get_game_features(game_id)
            lh.print_progress_bar(num + 1, num_games, prefix = 'Progress:', suffix = 'Complete', length = 50)           # Initial call to print 0% progress
        return all_game_features
