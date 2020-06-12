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

        # Function Description: The function will perform basic exploratory observations within the pitchers data structure.
        # Function Parameters: pitcher_query (The pitcher dictionary with all the pitcher names.)
        # Function Throws: Nothing
        # Function Returns: Nothing - The function will print information about the query structure. 

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