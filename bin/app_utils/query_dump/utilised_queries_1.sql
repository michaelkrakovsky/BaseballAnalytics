/* Query to aquire the results of a team in a specific window. */
select game_day.Visiting_Team, game_day.Home_Team, game_day.Date,
(case when event_instance.Vis_Score > event_instance.Home_Score then 1 else 0 end) as Home_Win
	from event_instance
	inner join game_day on event_instance.Game_ID=game_day.Game_ID
	where game_day.Date > '1990-09-02' and
	(game_day.Visiting_Team = 'BAL' or game_day.Home_Team = 'BAL') and 
	game_day.Date < '1990-10-02' and
    event_instance.End_Game_Flag = 'T'
    order by game_day.Date desc;