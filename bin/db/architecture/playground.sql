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
#select count(*) from pitching_features;
#select * from pitching_features where player_id = 'astap001';
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
		where player_information.player_id = 'bookc001'
	group by game_day.Game_ID) as A) as B
where B.Ten_Rolling_Ks is not null
and B.Ten_Rolling_WHIP is not null
and B.Ten_Rolling_RA is not null;

