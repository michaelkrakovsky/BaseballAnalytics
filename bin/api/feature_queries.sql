# Script Description: The SQL script contains the queries to pull important information that are features within are owm models.

        
#delete from offensive_features;
#SET SQL_SAFE_UPDATES = 1;
# Calculate the RA / 9 Innings, WHIP, and Strikeouts

select A.Season, A.Num_Strikeouts, 
((A.Num_Hits + A.Num_Walks) / A.Num_Innings) as WHIP,
(Runs_From_First + Runs_From_Second + Runs_From_Third + Runs_From_Home) as Runs_Allowed
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
		left join runner_on_first_details on runner_on_first_details.idEvent=event_instance.idEvent
		left join runner_on_second_details on runner_on_second_details.idEvent=event_instance.idEvent
        left join runner_on_third_details on runner_on_third_details.idEvent=event_instance.idEvent
			where player_information.player_id = 'hallr001'
				group by year(game_day.Date)
				order by year(game_day.Date)) as A;