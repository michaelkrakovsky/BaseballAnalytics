# Flow
# 1. Game Features - Game Id = BOS199004090


select Distinct game_day.Game_ID, batter_in_event.Batting_Team, pitcher_in_event.Pitcher_Name,       
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
	where event_instance.Game_ID = '{}' order by batter_in_event.batting_team, CHAR_LENGTH(event_instance.idEvent), event_instance.idEvent;

