# Script Description: The script will contain queries that can be used across functions. All one needs to input is a connection to the database.
# Script Version: 1.0

from pymysql import connect

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

        with self.__db_connection__.cursor() as c:
            c.execute(query)
            return c.fetchall()

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
        # Function Returns: A tuple of two lists. The first list contains the home team names while the second list contains the away teams.

        # Home Team equals 1 for Batting Team. The query is formatted like such: 
        #     Game_ID, Batting_Team, Pitcher_Name, Catcher, Center_Field, Left_Field, Right_Field, First_Base, Second_Base, Third_Base, Shortstop
        game_participants = """
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
                                """.format(game_id)
        game_vistors = game_participants[0][2:]             # Given the query conditions, this will always provide the starting lineups.