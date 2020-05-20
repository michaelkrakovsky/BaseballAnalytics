# Script Description: The SQL script contains the queries to pull important information that are features within are owm models.

/* 10 Day Moving BA, 10 Day OBP, 10 Day SLG */

select A.player_id, A.Game_ID,
	avg(A.Game_Hits / A.Game_AB) over (Order by A.Date rows between 9 preceding and current row) as Ten_Day_BA,
    avg((A.Game_Hits + A.Game_Walks + A.Game_Hit_By_Pitch) / (A.Game_AB + A.Game_Walks + A.Game_Hit_By_Pitch + A.Game_SF)) 
		over (Order by A.Date rows between 9 preceding and current row) as Ten_Day_OBP, 
	avg((A.Total_Game_Bases / A.Game_AB)) over (Order by A.Date rows between 9 preceding and current row) as Ten_Day_SLG 
	from (select game_day.Game_ID, game_day.Date, player_information.player_id,
     sum(case when event_instance.AB_Flag = 'T' then 1 else 0 end) as Game_AB, 
	 sum(case when event_instance.Hit_Value > 0 then 1 else 0 end) as Game_Hits,
	 sum(case when event_instance.SF_Flag = 'T' then 1 else 0 end) as Game_SF,
     sum(event_instance.Hit_Value) as Total_Game_Bases,
     sum(case when regexp_like(event_instance.Event_Text, '^W$|^IW$|^W(\\.|\\+).*$|^IW(\\.|\\+).*$') then 1 else 0 end) as Game_Walks, 
     sum(case when regexp_like(event_instance.Event_Text, '^HP.*$') then 1 else 0 end) as Game_Hit_By_Pitch
		from player_information inner join 
		batter_in_event on batter_in_event.Batter_Name = player_information.player_id inner join
		event_instance on event_instance.idEvent = batter_in_event.idEvent inner join
		game_day on event_instance.Game_ID = game_day.Game_ID
			where player_information.First_Name = 'Jose' and 
			player_information.Last_Name = 'Bautista' and 
			player_information.Player_Debut > '2000-01-01' and
			game_day.Date > '2011-03-01' and
			game_day.Date < '2011-11-01'
			group by game_day.Game_ID) as A;
            

/*
select sum(A.Total_Game_Bases) / sum(A.Game_AB) as Slugging 
	from (select game_day.Game_ID, game_day.Date,
     sum(case when event_instance.AB_Flag = 'T' then 1 else 0 end) as Game_AB, 
	 sum(case when event_instance.Hit_Value > 0 then 1 else 0 end) as Game_Hits,
	 sum(case when event_instance.SF_Flag = 'T' then 1 else 0 end) as Game_SF,
     sum(event_instance.Hit_Value) as Total_Game_Bases,
     sum(case when regexp_like(event_instance.Event_Text, '^W$|^IW$|^W(\\.|\\+).*$|^IW(\\.|\\+).*$') then 1 else 0 end) as Game_Walks, 
     sum(case when regexp_like(event_instance.Event_Text, '^HP.*$') then 1 else 0 end) as Game_Hit_By_Pitch
		from player_information inner join 
		batter_in_event on batter_in_event.Batter_Name = player_information.player_id inner join
		event_instance on event_instance.idEvent = batter_in_event.idEvent inner join
		game_day on event_instance.Game_ID = game_day.Game_ID
			where player_information.First_Name = 'Jose' and 
			player_information.Last_Name = 'Bautista' and 
			player_information.Player_Debut > '2000-01-01' and
			game_day.Date > '2011-03-01' and
			game_day.Date < '2011-11-01') as A;
            
*/