#INSERT IGNORE INTO pitcher_player_details (player_id, Last_Name, First_Name, Player_Debut) values ('michael', 'deleteMe', 'deleteMe', '2019-04-23');
#select * from pitcher_player_details;
#delete from pitcher_player_details where player_id like 'abada001';
#delete from positional_player_details where player_id like 'abadj101event_instancegame_day'

# --------------------------------------- Respective to Positional Player ---------------------------------------- #
#select * from positional_player_details;
#INSERT IGNORE INTO positional_player_details (player_id, Last_Name, First_Name, Player_Debut) values ('michael', 'deleteMe', 'deleteMe', '2019-04-23');

select offensive_features.Game_ID, offensive_features.player_id, 
Ten_Rolling_BA, Ten_Rolling_OBP, Ten_Rolling_SLG from offensive_features inner join
game_day on game_day.Game_ID=offensive_features.Game_ID
order by game_day.Date asc
                                
                                
                                