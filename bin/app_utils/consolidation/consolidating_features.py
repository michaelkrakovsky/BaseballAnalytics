# Script Description: Give the players and their features, the script will consolidate everything together
#     into a list ready to be modelled.
# Script Version: 1.0

from re import search

class Feature_Consolidater():

    def __init__(self):

        """Class Description: The script will consilidate all the necessary elements into a list readied to be modelled."""

        pass

    def get_starting_batters(self, batting_players, game_id, team_batting):

        """# Function Description: Givin all the batting events in a game, extract the starting the lineup.
        # Function Parameters: batting_players (Dict: The dictionary containing all the events from all games.), 
        #    game_id (String: The game id you wish to extract the betting lineup.), team_batting (String: The batting team: The Visting Team is 0, the Home Team is 1.)
        # Function Throws: Nothing
        # Function Returns: List: The list of players in the batting lineup."""
                                                        
        filter_team = [(g_id, team, e_id) for g_id, team, e_id in batting_players[game_id] if team == team_batting] 
        filter_team.sort(key=lambda x: int(search(r'\d+', x[2][:3]).group()))      # Sort the string by the leading numbers of each id.
        player_count = 0                                                           # Add the first unique 9 players found in the event lineup.
        player_lineup = []
        for tup in filter_team:
            if tup[0] not in player_lineup: 
                player_lineup.append(tup[0])
                player_count += 1
            if player_count >= 9: break                     # Exit the loop when you have all the players.
        return player_lineup

    def get_starting_pitcher(self, starting_pitchers, game_id, pitcher_team):

        """# Function Description: Extract the starting pitcher of the game.
        # Function Parameters: starting_pitchers (The dictionary containing all the games with their starters.), 
        #    game_id (The game id you wish to extract the betting lineup.), pitcher_team (The team of the pitcher who plays on the team.)
        # Function Throws: Nothing
        # Function Returns: The starting pitcher."""

        return starting_pitchers[game_id][pitcher_team]

    def get_offensive_features(self, offensive_features, player_id, game_id):

            """# Function Description: Retrieve the features of a given player prior to entering the new game. The features are available from the previous game.
            # Function Parameters: player_id (The player id associated in which we wish to retrieve the data.), game_id (The game id needed to look backwards.)
            # Function Throws: Nothing
            # Function Returns: A list containing the offensive features. The amount of features was determined in previous queries but does not matter in this function.
            #    If the player does not have much data, I will be returning -1 to signal the prescence of a new player."""

            player_stats = offensive_features[player_id]
            if len(player_stats) < 4:                          # Not enough games played to create reasonable stats.
                return [-1, -1]
            for idx, games in enumerate(player_stats):
                if games[0] == game_id:                        # NOTE: Can this be optimised with using numpy arrays?
                    return player_stats[idx - 1][1:]           # Return the stats from the day before. Should we particularily focus on a seaosn? Should things get a rest?
        
    def sub_offensive_features(self, offensive_features, batters, game_id):

        """# Function Description: Substitute the batters ids provided with the batting features. The features will be returned in the same order the names are provided.
        # Function Parameters: offensive_features (The dictionary containing the player ids that are tied to the offensive features.) 
        #    batters (The player id we wish to retrieve the data for.), game_id (The game id needed to look backwards.) 
        # Function Throws: Nothing
        # Function Returns: A complete list of the featues to be inputted into the model. The list will vary depending on the number of players and features for each player."""

        game_offensive_features = []
        for batter in batters:
            game_offensive_features += self.get_offensive_features(offensive_features, batter, game_id)
        return game_offensive_features

    def get_relief_pitchers(self, all_pitchers, relief_pitchers, game_id, pitcher_team, year):

        """# Function Description: Extract the relief pitchers within the game.
        # Function Parameters: all_pitchers (The dictionary containing all the games in which every pitcher participated.)
        #    relief_pitchers (The dictionary containing all the games with their relievers.), 
        #    game_id (The game id you wish to extract the batting lineup.), pitcher_team (The team of the pitcher who plays on the team.)
        # Function Throws: Nothing
        # Function Returns: A list containing the relief pitcher."""

        try:
            return relief_pitchers[game_id][pitcher_team]
        except KeyError:                                    # We would incur this error if the game is not found in the dictionary which is an anticipation of mine.
            season_games = [game_id_backup for game_id_backup in all_pitchers[pitcher_team][year]]       # Get all the games in the season.
            for id in season_games:                                                                      # Attempt to find a game within the season and use that starting pitcher.
                try:
                    return relief_pitchers[id][pitcher_team]
                except KeyError: 
                    pass
            raise KeyError("We were unable to find relief pitchers for this game.")                      # If we get here, throw an error.

    def get_pitchers_features(self, pitching_features, player_id, game_id):

        """# Function Description: Retrieve the features of a given player prior to entering the new game. The features are available from the previous game.
        # Function Parameters: pitching_features (The pitching features used to indicate the pitchers performance.)
        #    player_id (The player id associated in which we wish to retrieve the data.), game_id (The game id needed to look backwards.)
        # Function Throws: Nothing
        # Function Returns: A list containing the offensive features. The amount of features was determined in previous queries but does not matter in this function.
        #    If the player does not have much data, I will be returning -1 to signal the prescence of a new player."""

        player_stats = pitching_features[player_id]
        if len(player_stats) < 3:                          # Not enough games played to create reasonable stats.
            return [-1, -1, -1]
        for idx, games in enumerate(player_stats):
            if games[0] == game_id:                        # NOTE: Can this be optimised with using numpy arrays?
                return player_stats[idx - 1][1:]           # Return the stats from the day before. Should we particularily focus on a seaosn? Should things get a rest?

    def get_relief_pitchers_features(self, pitching_features, pitcher_id, game_id):

        """# Function Description: Given the current architecture, the game id provided by the client may not be in the list of game ids provided.KeyError
        #    To handle this problem, I will return the previous game id that is one date before the current game id.
        # Function Parameters: #    all_pitchers (The dictionary containing all the pitchers who participated in every game.),
        #    pitcher_Id (The pitcher id you wish to extract the information from.), 
        #    game_id (The game id you wish to get the features from.)
        # Function Throws: Nothing
        # Function Returns: The list of features for the pitcher."""

        if pitcher_id not in pitching_features:
            return [-1, -1, -1]
        player_stats = pitching_features[pitcher_id]       # NOTE: Can this be optimised with using numpy arrays?
        if len(player_stats) < 3:                          # Not enough games played to create reasonable stats.
            return [-1, -1, -1]
        for idx, games in enumerate(player_stats):
            if games[0][3:-1] > game_id[0][3:-1]:          # Return when the game date is greater than the current game. (This means we are in the future.)
                return player_stats[idx - 1][1:]           # Return the stats from the day before. Should we particularily focus on a seaosn? Should things get a rest?

    def sub_relief_pitching_features(self, pitching_features, pitchers, game_id):

        """# Function Description: Substitute the pitcher ids provided with the pitching features. The features will be returned in the same order the names are provided.
        # Function Parameters: pitching_features (The pitching features used to indicate the pitchers performance.),
        #    pitchers (The player ids we wish to retrieve the data for.), game_id (The game id needed to look backwards.) 
        # Function Throws: Nothing
        # Function Returns: A complete list of the featues to be inputted into the model. The list will vary depending on the number of players and features for each player."""

        pitcher_features = []                # NOTE: Can I convert this into a list comprehension?
        for pitcher in pitchers:
            pitcher_features += self.get_relief_pitchers_features(pitching_features, pitcher, game_id)
        return [float(feat) for feat in pitcher_features]

    def sub_pitching_features(self, pitching_features, pitchers, game_id):

        """# Function Description: Substitute the pitcher ids provided with the pitching features. The features will be returned in the same order the names are provided.
        # Function Parameters: pitching_features (The pitching features used to indicate the pitchers performance.),
        #    pitchers (The player ids we wish to retrieve the data for.), game_id (The game id needed to look backwards.) 
        # Function Throws: Nothing
        # Function Returns: A complete list of the featues to be inputted into the model. The list will vary depending on the number of players and features for each player."""

        pitcher_features = []
        for pitcher in pitchers:
            pitcher_features += self.get_pitchers_features(pitching_features, pitcher, game_id)
        return [float(feat) for feat in pitcher_features]

    def normalise_list(self, features, num_feats):

        """# Function Description: Given a list of stats, normalise the contents within the list.
        # Function Parameters: features (The features.), num_feats (The number of features to segregate.)
        # Function Throws: Nothing
        # Function Returns: The normalised values."""
        
        final_features = []
        seg_features = [[features[i] for i in range(num, len(features), num_feats)] for num in range(0, num_feats)]
        norm_features = [[float(i)/sum(li) for i in li] for li in seg_features]
        for li in norm_features:
            for i in li:
                final_features.append(i)
        return final_features

    def get_game_features_normalise(self, all_batters, offensive_features, all_pitchers, starting_pitchers, relief_pitchers, pitching_features, game_stats):

        """# Function Description: Get all the features for a given game id. This involves getting the players who played in the game and then retrieving their associated features.
        #    The values will be normalised including both home teams and visitors.
        # Function Parameters: all_batters (All of the batters information.), 
        #    offensive_features (All of the offensive features that are used to predict outcome.), 
        #    all_pitchers (The dictionary containing all the pitchers who participated in every game.),
        #    starting_pitchers (The starting pitchers in all the games.), 
        #    relief_pitchers (The relief pitchers in all the games.), 
        #    pitching_features (The pitching features in all the games. (Both relievers and starters.)),
        #    game_stats (The game id with all pertinent information.)
        # Function Throws: ValueError (Thrown when the incorrect number of features are returned.)
        # Function Returns: A single list containing the features of the game.""" 

        # Get Batting Features on both sides.
        batting_feat = self.sub_offensive_features(offensive_features, self.get_starting_batters(all_batters, game_stats[0], 1), game_stats[0])
        batting_feat += self.sub_offensive_features(offensive_features, self.get_starting_batters(all_batters, game_stats[0], 0), game_stats[0])
        game_features = self.normalise_list(batting_feat, 2)
        # Get Pitching Features on both sides.
        pitching_feat = self.sub_pitching_features(pitching_features, [self.get_starting_pitcher(starting_pitchers, game_stats[0], game_stats[6])], game_stats[0])
        pitching_feat += self.sub_relief_pitching_features(pitching_features, self.get_relief_pitchers(all_pitchers, relief_pitchers, game_stats[0], game_stats[6], game_stats[1]), game_stats[0])
        pitching_feat += self.sub_pitching_features(pitching_features, [self.get_starting_pitcher(starting_pitchers, game_stats[0], game_stats[7])], game_stats[0])
        pitching_feat += self.sub_relief_pitching_features(pitching_features, self.get_relief_pitchers(all_pitchers, relief_pitchers, game_stats[0], game_stats[7], game_stats[1]), game_stats[0])
        game_features += self.normalise_list(pitching_feat, 3)
        if len(game_features) != 60: raise ValueError("The correct number of features was not returned.")
        return game_features

    def get_game_features(self, all_batters, offensive_features, all_pitchers, starting_pitchers, relief_pitchers, pitching_features, game_stats):

        """# Function Description: Get all the features for a given game id. This involves getting the players who played in the game and then retrieving their associated features.
        # Function Parameters: all_batters (All of the batters information.), 
        #    offensive_features (All of the offensive features that are used to predict outcome.), 
        #    all_pitchers (The dictionary containing all the pitchers who participated in every game.),
        #    starting_pitchers (The starting pitchers in all the games.), 
        #    relief_pitchers (The relief pitchers in all the games.), 
        #    pitching_features (The pitching features in all the games. (Both relievers and starters.)),
        #    game_stats (The game id with all pertinent information.)
        # Function Throws: ValueError (Thrown when the incorrect number of features are returned.)
        # Function Returns: A single list containing the features of the game."""

        game_features = []
        # Acquire Home Stats
        game_features += self.sub_pitching_features(pitching_features, [self.get_starting_pitcher(starting_pitchers, game_stats[0], game_stats[6])], game_stats[0])       # The location of the home team within the games list.
        game_features += self.sub_offensive_features(offensive_features, self.get_starting_batters(all_batters, game_stats[0], 1), game_stats[0])
        game_features += self.sub_relief_pitching_features(pitching_features, self.get_relief_pitchers(all_pitchers, relief_pitchers, game_stats[0], game_stats[6], game_stats[1]), game_stats[0])
        # Acquire Away Stats
        game_features += self.sub_pitching_features(pitching_features, [self.get_starting_pitcher(starting_pitchers, game_stats[0], game_stats[7])], game_stats[0])
        game_features += self.sub_offensive_features(offensive_features, self.get_starting_batters(all_batters, game_stats[0], 0), game_stats[0])
        game_features += self.sub_relief_pitching_features(pitching_features, self.get_relief_pitchers(all_pitchers, relief_pitchers, game_stats[0], game_stats[7], game_stats[1]), game_stats[0])
        if len(game_features) != 60: raise ValueError("The correct number of features was not returned.")
        return game_features

