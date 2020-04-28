#INSERT IGNORE INTO pitcher_player_details (player_id, Last_Name, First_Name, Player_Debut) values ('michael', 'deleteMe', 'deleteMe', '2019-04-23');
#select * from pitcher_player_details;
#delete from pitcher_player_details where player_id like 'abada001';
#delete from positional_player_details where player_id like 'abadj101event_instancegame_day'

# --------------------------------------- Respective to Positional Player ---------------------------------------- #
#select * from positional_player_details;
#INSERT IGNORE INTO positional_player_details (player_id, Last_Name, First_Name, Player_Debut) values ('michael', 'deleteMe', 'deleteMe', '2019-04-23');

# --------------------------------------- Respective to Game Day ---------------------------------------- #
#select * from game_day;
#INSERT IGNORE INTO game_day (Visiting_Team, Home_Team, Date, Game_ID, NumGameInDay) Values ('SEA', 'TEX', '2015-12-22', 'TEX201504290', '1');
# --------------------------------------- Respective to Event ---------------------------------------- #
#select * from event_instance
#INSERT INTO event_instance (idEvent, Game_ID, Inning, Batting_Team, Outs, Balls, Strikes, Pitch_Sequence, Vis_Score, Home_Score, Batter_Name, Batter_Hand, Pitcher_Name, Pitcher_Hand, Event_Text, Leadoff_Flag, Pinch_Hit_Flag, Defensive_Position, Lineup_Position, Event_Type, Batter_Event_Flag, AB_Flag, Hit_Value, SH_Flag, SF_Flag, Outs_on_Play, Double_Play_Flag, Triple_Play_Flag, RBI_On_Play, Wild_Pitch_Flag, Passed_Ball_Flag, Fielded_By, Batted_Ball_Type, Bunt_Flag, Foul_Flag, Hit_Location, Num_Errors, Batter_Dest, Play_on_Batter, New_Game_Flag, End_Game_Flag, Position_of_Batter_removed_for_Pinch_Hitter) Values ('5e40d66476fc4d5d594c7d226aab04e95a91eb736c7576f4eebead92', 'TEX201504290', 1, 0, 0, 0, 0, 'X', 0, 0, 'michael', 'R', 'sdfgh', 'L', 'S8/G', 'T', 'F', 4, 1, 20, 'T', 'T', 1, 'F', 'F', 0, 'F', 'F', 0, 'F', 'F', 8, 'G', 'F', 'F', '', 0, 1, '', 'T', 'F', 0);

# --------------------------------------- Respective to Error Informational Positional ---------------------------------------- #
#SET SQL_SAFE_UPDATES = 0;           # Set to unsfe know
#select * from game_day;
#DELETE From game_day;
#select * from event_instance;
#select * from player_information;

select count(*) from event_instance;

