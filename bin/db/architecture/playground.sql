#INSERT IGNORE INTO pitcher_player_details (player_id, Last_Name, First_Name, Player_Debut) values ('michael', 'deleteMe', 'deleteMe', '2019-04-23');
#select * from pitcher_player_details;
#delete from pitcher_player_details where player_id like 'abada001';
#delete from positional_player_details where player_id like 'abadj101event_instancegame_day'

# --------------------------------------- Respective to Positional Player ---------------------------------------- #
#select * from positional_player_details;
#INSERT IGNORE INTO positional_player_details (player_id, Last_Name, First_Name, Player_Debut) values ('michael', 'deleteMe', 'deleteMe', '2019-04-23');

# --------------------------------------- Respective to Game Day ---------------------------------------- #
#select * from game_day;
#INSERT IGNORE INTO game_day (Visiting_Team, Home_Team, Date, Game_ID, NumGameInDay) Values ('SEA', 'TEX', '2015-12-22', 'PHI199209271', '1');
# --------------------------------------- Respective to Event ---------------------------------------- #
#select * from event_instance
#INSERT INTO event_instance (idEvent, Game_ID, Inning, Batting_Team, Outs, Balls, Strikes, Pitch_Sequence, Vis_Score, Home_Score, Batter_Name, Batter_Hand, Pitcher_Name, Pitcher_Hand, Event_Text, Leadoff_Flag, Pinch_Hit_Flag, Defensive_Position, Lineup_Position, Event_Type, Batter_Event_Flag, AB_Flag, Hit_Value, SH_Flag, SF_Flag, Outs_on_Play, Double_Play_Flag, Triple_Play_Flag, RBI_On_Play, Wild_Pitch_Flag, Passed_Ball_Flag, Fielded_By, Batted_Ball_Type, Bunt_Flag, Foul_Flag, Hit_Location, Num_Errors, Batter_Dest, Play_on_Batter, New_Game_Flag, End_Game_Flag, Position_of_Batter_removed_for_Pinch_Hitter) Values ('5e40d66476fc4d5d594c7d226aab04e95a91eb736c7576f4eebead92', 'TEX201504290', 1, 0, 0, 0, 0, 'X', 0, 0, 'michael', 'R', 'sdfgh', 'L', 'S8/G', 'T', 'F', 4, 1, 20, 'T', 'T', 1, 'F', 'F', 0, 'F', 'F', 0, 'F', 'F', 8, 'G', 'F', 'F', '', 0, 1, '', 'T', 'F', 0);

#select * from game_day;
#select count(*) from player_information;
#select count(*) from event_instance;
#select count(*) from event_instance;
#SET SQL_SAFE_UPDATES = 0;
#select count(*) from event_instance
#select count(*) from error_information
#select * from event_catcher
#select * from event_instance
#select game_id from game_day where date > '2019-08-29';
#select count(*) from pitching_features;

select Distinct game_day.Game_ID, batter_in_event.Batting_Team, pitcher_in_event.Pitcher_Name,       # Home Team equals One for Batting Team
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
    where event_instance.Game_ID = 'ANA200604070'
    order by batter_in_event.batting_team, CHAR_LENGTH(event_instance.idEvent), event_instance.idEvent;

select event_instance.Game_ID,
(case when event_instance.Vis_Score > event_instance.Home_Score then 1 else 0 end) as Home_Win
	from event_instance
	inner join game_day on event_instance.Game_ID=game_day.Game_ID 
    where event_instance.End_Game_Flag = 'T'
    order by game_day.Date;
    