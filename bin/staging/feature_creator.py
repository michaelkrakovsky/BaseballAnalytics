# Script Description: The script will prepare all the features related to offensive. The data will queried and then stored in the database
#    to prevent work being re-executed. The intent will be that all players will have there features calculated starting with the first record.
# Script Notes: To date there are three features that will be used related specific to offensive:
#    1. Batting Average
#    2. On Base Percentage
#    3. Slugging Percentage
# Script Creator: Michael Krakovsky
# Script Version: 0.1

import sys
sys.path.extend('../../../')                                             # Import the entire project to be found.
from BaseballAnalytics.bin.app_utils.common_help import log_helper
from BaseballAnalytics.bin.app_utils.queries import Queries
from warnings import filterwarnings                                      # Handle warnings from mysql.
from pymysql import connect

class Offensive_Features():

    def __init__(self, db_connection):

        # Class Description: The class will direct the queries in creating the stats and inputting them into the database. To be exact, 
        #    I will create the tables prior to executing the queries. The tables can be found in the schema diagram.
        # Class Instantiators: db_connection (pymysql.connections.Connection: The connection to the database.)

        if (str(type(db_connection)) == '<class \'pymysql.connections.Connection\'>'):
            self.__db_connection__ = db_connection
        else:
            raise ValueError("The user did not provide the correct pymysql connector.")

    def execute_query(self, query):

        # Function Description: The generic query executor that utilises the current connection to the database and executes a query.
        # Function Parameters: query (The query that will be executed.)
        # Function Throws: Nothing
        # Function Returns: True or False (True will be returned if there are no warnings or errors. False will be returned otherwise.)

        cursor = self.__db_connection__.cursor() 
        filterwarnings('error')                                     # Convert warnings into exceptions to be caught.                   
        try:
            status = cursor.execute(query)                          # Execute Query: And close the cursor.
            self.__db_connection__.commit()                         # This essentially saves the query execution to the database.
        except Exception as ex:
            status_str = str(ex)
            status_num = status_str[1:5]
            if status_num == '1265':                                 # Commit the query if it matches the appropriate status number.
                status = 1
                self.__db_connection__.commit() 
            else:
                status = 0
        filterwarnings('always')                                    # Turn the filter for warnings back on.
        cursor.close()
        return bool(status)

    def insert_offensive_information(self, player_id):

        # Function Description: The query will insert all the necessary offensive information (the basis at least) into the database.
        # Function Parameters: player_id (The player for who's values you wish to retrieve.)
        # Function Throws: Nothing
        # Function Returns: Nothing

        # 10 Day Moving BA, 10 Day OBP, 10 Day SLG
        offensive_query = """
                            insert into offensive_features(Game_ID, player_id, Ten_Rolling_BA, Ten_Rolling_OBP, Ten_Rolling_SLG)
                            select A.Game_ID, A.player_id,
                                round(avg(A.Game_Hits / A.Game_AB) over (Order by A.Date rows between 9 preceding and current row), 5) as Ten_Day_BA,
                                round(avg((A.Game_Hits + A.Game_Walks + A.Game_Hit_By_Pitch) / (A.Game_AB + A.Game_Walks + A.Game_Hit_By_Pitch + A.Game_SF)) 
                                    over (Order by A.Date rows between 9 preceding and current row), 5) as Ten_Day_OBP, 
                                round(avg((A.Total_Game_Bases / A.Game_AB)) over (Order by A.Date rows between 9 preceding and current row), 5) as Ten_Day_SLG 
                                from (select game_day.Game_ID, game_day.Date, player_information.player_id,
                                sum(case when event_instance.AB_Flag = 'T' then 1 else 0 end) as Game_AB, 
                                sum(case when event_instance.Hit_Value > 0 then 1 else 0 end) as Game_Hits,
                                sum(case when event_instance.SF_Flag = 'T' then 1 else 0 end) as Game_SF,
                                sum(event_instance.Hit_Value) as Total_Game_Bases,
                                sum(case when regexp_like(event_instance.Event_Text, '^W$|^IW$|^W(\\\\.|\\\\+).*$|^IW(\\\\.|\\\\+).*$') then 1 else 0 end) as Game_Walks, 
                                sum(case when regexp_like(event_instance.Event_Text, '^HP.*$') then 1 else 0 end) as Game_Hit_By_Pitch
                                    from player_information inner join 
                                    batter_in_event on batter_in_event.Batter_Name = player_information.player_id inner join
                                    event_instance on event_instance.idEvent = batter_in_event.idEvent inner join
                                    game_day on event_instance.Game_ID = game_day.Game_ID
                                        where player_information.player_id = """ + '\'' + player_id + '\'' + '\n group by game_day.Game_ID) as A;'
        return self.execute_query(offensive_query)



def main():

    # Function Description: Create a database connection and process event files. 

    conn = connect(host="localhost", user="root", passwd="praquplDop#odlg73h?c", db="baseball_stats_db")         # The path to the pymysql connector to access the database.
    feat_creator = Offensive_Features(conn)
    #feat_creator.insert_offensive_information('bautj002')
    qs = Queries(conn)
    qs.get_all_player_ids()

if __name__ == "__main__":
    main()