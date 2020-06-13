#INSERT IGNORE INTO pitcher_player_details (player_id, Last_Name, First_Name, Player_Debut) values ('michael', 'deleteMe', 'deleteMe', '2019-04-23');
#select * from pitcher_player_details;
#delete from pitcher_player_details where player_id like 'abada001';
#delete from positional_player_details where player_id like 'abadj101event_instancegame_day'

# --------------------------------------- Respective to Positional Player ---------------------------------------- #
#select * from positional_player_details;
#INSERT IGNORE INTO positional_player_details (player_id, Last_Name, First_Name, Player_Debut) values ('michael', 'deleteMe', 'deleteMe', '2019-04-23');

select event_instance.Game_ID, Year(game_day.date) as Year, Day(game_day.date) as Day,
       Month(game_day.date) as Month, batter_in_event.Batting_Team,
       game_day.Home_Team, game_day.Visiting_Team,
	   pitcher_in_event.Pitcher_Name, pitcher_in_event.idEvent
	   from event_instance
	   inner join pitcher_in_event on pitcher_in_event.idEvent=event_instance.idEvent
	   inner join batter_in_event on batter_in_event.idEvent=event_instance.idEvent
	   inner join game_day on game_day.Game_ID=event_instance.Game_ID
       where Year(game_day.Date) = 1997 
       and (game_day.Home_Team = 'ANA' or game_day.Visiting_Team = 'ANA')
       group by game_day.Game_ID