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
from timeit import default_timer as timer
from BaseballAnalytics.bin.app_utils.common_help import Log_Helper
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

    def create_all_offensive_information(self):

        # Function Description: The orchestration function which fills the offensive features with all information for each player.\
        # Function Parameters: Nothing
        # Function Throws: Nothing
        # Function Returns: Nothing

        qs = Queries(self.__db_connection__)
        lh = Log_Helper()
        player_ids = qs.get_all_player_ids()
        total_player_ids = len(player_ids)
        start = timer()
        lh.print_progress_bar(0, total_player_ids, prefix = 'Progress:', suffix = 'Complete', length = 50)           # Initial call to print 0% progress
        for num, id in enumerate(player_ids):                           # Find the offensive stats for every player.
            self.insert_offensive_information(id[0])
            lh.print_progress_bar(num + 1, total_player_ids, prefix = 'Progress:', suffix = 'Complete', length = 50)      # Manipulate Error Bar.
        end = timer()
        print("Total processing time to create all offensive features: " + str(end - start))

def main():

    # Function Description: Create a database connection and process event files. 

    conn = connect(host="localhost", user="root", passwd="praquplDop#odlg73h?c", db="baseball_stats_db")         # The path to the pymysql connector to access the database.
    feat_creator = Offensive_Features(conn)
    feat_creator.create_all_offensive_information()                                                              # Create all the offensive features.

if __name__ == "__main__":
    main()

    ((A.Num_Hits + A.Num_Walks) / A.Num_Innings) as WHIP
#(A.Runs_From_First + A.Runs_From_Second + A.Runs_From_Third + A.Runs_From_Home) as Num_Runs_Allowed
	from (select year(game_day.Date) as Season, 
	sum(case when event_instance.Event_Type = '3' then 1 else 0 end) as Num_Strikeouts,
	sum(case when event_instance.Hit_Value > 0 then 1 else 0 end) as Num_Hits,
	sum(case when regexp_like(event_instance.Event_Text, '^W$|^IW$|^W(\\.|\\+).*$|^IW(\\.|\\+).*$') then 1 else 0 end) as Num_Walks,
	sum(case when runner_on_first_details.Runner_On_1st_Dest > 3 then 1 else 0 end) as Runs_From_First,
	sum(case when runner_on_second_details.Runner_On_2nd_Dest > 3 then 1 else 0 end) as Runs_From_Second,
	sum(case when runner_on_third_details.Runner_On_3rd_Dest > 3 then 1 else 0 end) as Runs_From_Third,
    sum(case when event_instance.Batter_Dest > 3 then 1 else 0 end) as Runs_From_Home,
    Truncate(sum((event_instance.Outs_on_Play) / 3), 2) as Num_Innings
		from event_instance
		inner join pitcher_in_event on event_instance.idEvent=pitcher_in_event.idEvent
		inner join game_day on event_instance.Game_ID=game_day.Game_ID
		inner join player_information on player_information.player_id=pitcher_in_event.Pitcher_Name
        inner join runner_on_first_details on runner_on_first_details.idEvent=event_instance.idEvent
		inner join runner_on_second_details on runner_on_second_details.idEvent=event_instance.idEvent
        inner join runner_on_third_details on runner_on_third_details.idEvent=event_instance.idEvent
			where player_information.player_id = 'hallr001'
				group by year(game_day.Date)
				order by year(game_day.Date)) as A;