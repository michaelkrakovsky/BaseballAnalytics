#INSERT IGNORE INTO pitcher_player_details (player_id, Last_Name, First_Name, Player_Debut) values ('michael', 'deleteMe', 'deleteMe', '2019-04-23');
#select * from pitcher_player_details;
#delete from pitcher_player_details where player_id like 'abada001';
#delete from positional_player_details where player_id like 'abadj101event_instancegame_day'

# --------------------------------------- Respective to Positional Player ---------------------------------------- #
#select * from positional_player_details;
#INSERT IGNORE INTO positional_player_details (player_id, Last_Name, First_Name, Player_Debut) values ('michael', 'deleteMe', 'deleteMe', '2019-04-23');

#SET SQL_SAFE_UPDATES = 0;
#select count(*) from event_instance
#select count(*) from error_information
#select * from event_catcher
#select * from event_instance
#select game_id from game_day where date > '2019-08-29';
#select count(*) from pitching_features;    

select * from event_instance where game_id = 'BOS199004090'

    
    
    
    
    
    