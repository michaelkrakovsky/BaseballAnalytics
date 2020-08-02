# Script Description: The script will prepare all the features related to offensive. The data will queried and then stored in the database
#    to prevent work being re-executed. The intent will be that all players will have there features calculated starting with the first record.
# Script Notes: To date there are three features that will be used related specific to offensive:
#    1. On Base Percentage
#    2. Slugging Percentage
# Related to Pitchers, there are three features that have been choosen to begin.
#    1. Strikeouts
#    2. WHIP
#    3. Approx. Runs Allowed
# Script Creator: Michael Krakovsky
# Script Version: 2.0

from sys import path
path.extend('../../../')                                                 # Import the entire project to be found.
from timeit import default_timer as timer
from BaseballAnalytics.bin.app_utils.common_help import Log_Helper
from BaseballAnalytics.bin.app_utils.queries import Queries
from pymysql import connect
from generic_creator import Generic_Features

class Offensive_Features(Generic_Features):

    def __init__(self, db_connection):

        """ Class Description: The class will direct the queries in creating the stats and inputting them into the database. To be exact, 
        #    I will create the tables prior to executing the queries. The tables can be found in the schema diagram.
        # Class Instantiators: db_connection (pymysql.connections.Connection: The connection to the database.) """

        Generic_Features.__init__(self, db_connection)

    def insert_offensive_information(self, player_id):

        """ Function Description: The query will insert all the necessary offensive information (the basis at least) into the database.
        # Function Parameters: player_id (String: The player for who's values you wish to retrieve.)
        # Function Throws: Nothing
        # Function Returns: Nothing """

        # 10 Day Moving BA, 10 Day OBP, 10 Day SLG
        offensive_query = """insert into offensive_features(Game_ID, player_id, Ten_Rolling_BA, Ten_Rolling_OBP, Ten_Rolling_SLG)
                            select B.Game_ID, B.player_id, B.Ten_Day_BA, B.Ten_Day_OBP, B.Ten_Day_SLG
                                from
                                (select A.Game_ID, A.player_id,
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
                                            where player_information.player_id = """ + '\'' + player_id + '\'' + """\ngroup by game_day.Game_ID) as A) as B
                                where B.Ten_Day_BA is not null
                                and B.Ten_Day_OBP is not null
                                and B.Ten_Day_SLG is not null;"""
        return self.execute_query(offensive_query)

    def create_all_offensive_information(self):

        """ Function Description: The orchestration function which fills the offensive features with all information for each player.\
        # Function Parameters: Nothing
        # Function Throws: Nothing
        # Function Returns: Nothing """

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

class Pitcher_Features(Generic_Features):

    def __init__(self, db_connection):

        """# Class Description: The class will direct the queries in creating the stats related to Pitchers. Assume that the 
        #    tables will be created prior to the insertion of the stats.
        # Class Instantiators: db_connection (pymysql.connections.Connection: The connection to the database.)"""

        Generic_Features.__init__(self, db_connection)

    def insert_pitcher_information(self, player_id):

        """# Function Description: The query will insert all the necessary pitching information (the basis at least) into the database.
        # Function Parameters: player_id (The player for who's values you wish to retrieve.)
        # Function Throws: Nothing
        # Function Returns: Nothing"""

        # 10 Day Ks, 10 Day WHIP, 10 Day RA        
        pitching_query = """
                            insert into pitching_features(Game_ID, player_id, Ten_Rolling_Ks, Ten_Rolling_WHIP, Ten_Rolling_RA)
                            select B.Game_ID, B.player_id, B.Ten_Rolling_Ks, B.Ten_Rolling_WHIP, B.Ten_Rolling_RA
                            from (select A.Game_ID, A.player_id,
                            round(avg(A.Num_Strikeouts) over (Order by A.Date rows between 9 preceding and current row), 3) as Ten_Rolling_Ks,
                            round(avg((A.Num_Hits + A.Num_Walks) / A.Num_Innings) over (Order by A.Date rows between 9 preceding and current row), 3) as Ten_Rolling_WHIP, 
                            round(avg((A.Runs_From_First + A.Runs_From_Second + A.Runs_From_Third + A.Runs_From_Home)) over (Order by A.Date rows between 9 preceding and current row), 3) as Ten_Rolling_RA 
                            from (select game_day.Game_ID, game_day.Date, player_information.player_id,
                            sum(case when event_instance.Event_Type = '3' then 1 else 0 end) as Num_Strikeouts,
                            sum(case when event_instance.Hit_Value > 0 then 1 else 0 end) as Num_Hits,
                            sum(case when regexp_like(event_instance.Event_Text, '^W$|^IW$|^W(\\\\.|\\\\+).*$|^IW(\\\\.|\\\\+).*$') then 1 else 0 end) as Num_Walks,
                            sum(case when runner_on_first_details.Runner_On_1st_Dest > 3 then 1 else 0 end) as Runs_From_First,
                            sum(case when runner_on_second_details.Runner_On_2nd_Dest > 3  then 1 else 0 end) as Runs_From_Second,
                            sum(case when runner_on_third_details.Runner_On_3rd_Dest > 3 then 1 else 0 end) as Runs_From_Third,
                            sum(case when event_instance.Batter_Dest > 3 then 1 else 0 end) as Runs_From_Home,
                            Truncate(sum((event_instance.Outs_on_Play) / 3), 2) as Num_Innings
                                from event_instance
                                inner join pitcher_in_event on event_instance.idEvent=pitcher_in_event.idEvent
                                inner join game_day on event_instance.Game_ID=game_day.Game_ID
                                inner join player_information on player_information.player_id=pitcher_in_event.Pitcher_Name
                                left join runner_on_first_details on runner_on_first_details.idEvent=event_instance.idEvent
                                left join runner_on_second_details on runner_on_second_details.idEvent=event_instance.idEvent
                                left join runner_on_third_details on runner_on_third_details.idEvent=event_instance.idEvent
                                    where player_information.player_id = """ + '\'' + player_id + '\' ' + """
                                group by game_day.Game_ID) as A) as B
                            where B.Ten_Rolling_Ks is not null
                            and B.Ten_Rolling_WHIP is not null
                            and B.Ten_Rolling_RA is not null;"""        
        return self.execute_query(pitching_query)

    def create_all_pitcher_information(self):

        """# Function Description: The orchestration function which fills the pitching features with all information for each player.
        # Function Parameters: Nothing
        # Function Throws: Nothing
        # Function Returns: Nothing"""

        qs = Queries(self.__db_connection__)
        lh = Log_Helper()
        player_ids = qs.get_all_player_ids()
        total_player_ids = len(player_ids)
        log_file = lh.create_log_file(self.log_folder, 'feature_creator_vTwo')
        start = timer()
        lh.print_progress_bar(0, total_player_ids, prefix = 'Progress:', suffix = 'Complete', length = 50)           # Initial call to print 0% progress
        for num, id in enumerate(player_ids):                                # Find the offensive stats for every player.
            status = self.insert_pitcher_information(id[0])
            if status == False:                                              # Log errors.
                lh.log_error_in_file(log_file, "\nFailed at id: " + str(id[0]))
            lh.print_progress_bar(num + 1, total_player_ids, prefix = 'Progress:', suffix = 'Complete', length = 50)      # Manipulate Error Bar.
        end = timer()
        print("Total processing time to create all pitching features: " + str(end - start))

def main():

    """ #Function Description: Create a database connection and process event files."""

    conn = connect(host="localhost", user="root", passwd="praquplDop#odlg73h?c", db="baseball_stats_db")         # The path to the pymysql connector to access the database.
    #off_feat_creator = Offensive_Features(conn)
    #off_feat_creator.create_all_offensive_information()                                                          # Create all the offensive and pitcher features.
    pitch_feat_creator = Pitcher_Features(conn)
    pitch_feat_creator.create_all_pitcher_information()

if __name__ == "__main__":
    main()

