#INSERT IGNORE INTO pitcher_player_details (player_id, Last_Name, First_Name, Player_Debut) values ('michael', 'deleteMe', 'deleteMe', '2019-04-23');
#select * from pitcher_player_details;
#delete from pitcher_player_details where player_id like 'abada001';
#delete from positional_player_details where player_id like 'abadj101event_instancegame_day'

# --------------------------------------- Respective to Positional Player ---------------------------------------- #
#select * from positional_player_details;
#INSERT IGNORE INTO positional_player_details (player_id, Last_Name, First_Name, Player_Debut) values ('michael', 'deleteMe', 'deleteMe', '2019-04-23');

/*                                
select pitching_features.Game_ID, pitching_features.player_id,
Ten_Rolling_Ks, Ten_Rolling_WHIP, Ten_Rolling_RA from pitching_features inner join
game_day on game_day.Game_ID=pitching_features.Game_ID
where pitching_features.player_id = 'hartm002'
order by game_day.Date Asc;
*/
#delete from pitching_features;

# Query to aquire the results of a team in a specific window.
select game_day.Visiting_Team, game_day.Home_Team, game_day.Date,
(case when event_instance.Vis_Score > event_instance.Home_Score then 1 else 0 end) as Home_Win
	from event_instance
	inner join game_day on event_instance.Game_ID=game_day.Game_ID
	where game_day.Date > '1990-09-02' and
	(game_day.Visiting_Team = 'BAL' or game_day.Home_Team = 'BAL') and 
	game_day.Date < '1990-10-02' and
    event_instance.End_Game_Flag = 'T'
    order by game_day.Date desc;