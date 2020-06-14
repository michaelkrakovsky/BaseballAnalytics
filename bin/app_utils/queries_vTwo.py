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