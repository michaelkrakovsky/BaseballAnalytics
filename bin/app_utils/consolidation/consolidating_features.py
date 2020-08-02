# Script Description: Give the players and their features, the script will consolidate everything together
#     into a list ready to be modelled.
# Script Version: 1.0

from re import search
from pickle import load, dump
from BaseballAnalytics.bin.app_utils.common_help import Log_Helper

class Feature_Pack():

    """ 
    Class Description: The class will hold all the necessary dictionaries from previous queries and executions. This will 
        become important when it is time to considate these features.
    """

    def __init__(self, game_outcomes, winning_pct, all_batters, offensive_features, all_pitchers, starting_pitchers, relief_pitchers, pitching_features):

        """
        Function Description: The init method to instantiate the class.
        Function Parameters: game_outcomes (List: The outcomes of each game to be modelled.), 
            winning_pct (Dict: The winning percentage of each team prior to game indicated within the key.),
            all_batters (Dict: The storage of each batter who participated in the game.), 
            offensive_features (Dict: The offensive stats of the player prior to the game.), 
            all_pitchers (Dict: The storage of each pitcher who participated in the game.), 
            starting_pitchers (Dict: The pitchers who will start in the game.), 
            relief_pitchers (Dict: The pitchers will be a reliever in the game.), 
            pitching_features (Dict: The features of the pitchers prior to the current.)
        Function Throws: Nothing
        Function Returns: Nothing
        """

        self.game_outcomes = game_outcomes
        self.winning_pct = winning_pct
        self.all_batters = all_batters 
        self.offensive_features = offensive_features 
        self.all_pitchers = all_pitchers 
        self.starting_pitchers = starting_pitchers
        self.relief_pitchers = relief_pitchers 
        self.pitching_features = pitching_features

class Feature_Consolidater():

    def __init__(self):

        """Class Description: The script will consilidate all the necessary elements into a list readied to be modelled."""

        pass

    def _calc_win_pct(self, current_record):

        """ Function Description: Calculate the win percentage of the teams within the dictionary.
        # Function Parameters: current_record (Dict: The record of the participating teams.) 
        # Function Throws: Nothing
        # Function Returns: current_record (Dict: The record of the participating teams. However, the changes will be applied.) """

        for team, record in current_record.items():
            if record[1] != 0:
                current_record[team] = record[0] / record[1]
            else:
                current_record[team] = 0.0 
        return current_record

    def _add_games(self, current_record, team, home_advantage, game_outcome):

        """ Function Description: Help insert a game into the current_record dictionary. There is some logic that is repeated and better modulated
            within a distinct function.
        # Function Parameters: current_record (Dict: The current record of both teams within the most recent event.), 
        #     team (String: The team to update.), home_advantage (Boolean: An indicator of either being home or away.), 
        #     game_outcome (Int: An indication of whether the home team has won.).
        # Function Throws: Nothing
        # Function Returns: Nothing - We are making the change of current record at the point of reference. """

        if home_advantage == True:
            if game_outcome == 0:                # Remember, a 0 indicates that the home team has won.
                current_record[team][0] += 1     # Record whether the team has won, else add that a game has been played.
                current_record[team][1] += 1
            else: 
                current_record[team][1] += 1
        else:
            if game_outcome == 0:                # Visitors will experience the opposite logic.
                current_record[team][1] += 1
            else:
                current_record[team][0] += 1 
                current_record[team][1] += 1

    def _get_last_n_games_pct(self, game_outcomes_window, num_games):

        """ Function Description: Get the winning percentage of the participating teams of the last n games.
            DO NOT INCLUDE the current game within the winning percentage since we are unaware of this outcome at
            the point of the record.
        # Function Parameters: game_outcomes_window (List: The outcomes of the up until the current game.), 
            num_games (Int: The number of games to go back.)
        # Function Throws: Nothing
        # Function Returns: (Dict: Containing the teams who participated in the game with their respective winning percentages.)"""

        most_recent_game = game_outcomes_window[-1]              # A sample record: ('BOS199004090', 1990, 9, 4, 5, 2, 'BOS', 'DET', 0)
        home_team = most_recent_game[6]
        vis_team = most_recent_game[7]
        current_record = {}
        home_games_factored = 0
        vis_games_factored = 0
        current_record[home_team] = [0, 0]                       # Ensure that the team is inserted into the dictionary.
        current_record[vis_team] = [0, 0]
        if len(game_outcomes_window) == 1:                       # There is nothing we can do at the beginning of the season.
            return {home_team: 0.0, vis_team: 0.0}
        for game in reversed(game_outcomes_window[:-1]):         # Start after the most recent game since that is what we are analysing.
            game_home_team = game[6]
            game_vis_team = game[7]
            if ((home_team == game_home_team) and (home_games_factored < num_games)):       # Check if the HOME team participated in the games past.
                self._add_games(current_record, home_team, True, game[-1])
                home_games_factored += 1                                                    # Count that the game has been factored.
            elif ((home_team == game_vis_team) and (home_games_factored < num_games)):
                self._add_games(current_record, home_team, False, game[-1])
                home_games_factored += 1
            if ((vis_team == game_home_team) and (vis_games_factored < num_games)):         # Check if the VIS team participated in the games past.
                self._add_games(current_record, vis_team, True, game[-1])
                vis_games_factored += 1
            elif ((vis_team == game_vis_team) and (vis_games_factored < num_games)):
                self._add_games(current_record, vis_team, False, game[-1])
                vis_games_factored += 1
            if ((home_games_factored >= num_games) and (vis_games_factored >= num_games)):
                return self._calc_win_pct(current_record)                                        # End when all the games are accounted for.
        return self._calc_win_pct(current_record)                                                # If reached, the team did not play n games.

    def get_win_pct(self, game_outcomes, num_games=10):

        """ Function Description: Finding the winning percentage of the participating teams for the last x games.
        # Function Parameters: game_outcomes (List: A list of tuples containing the game outcomes of each game.)
        #    num_games (Int: The number of games going back)
        # Function Throws: Nothing
        # Function Returns: (Dict: The dictionary identified by the game id and the win percentage of each team.)"""

        current_year = 1990
        game_pct_attributes = {}
        while current_year <= 2019:
            year_game_outcomes = [outcome for outcome in game_outcomes if outcome[1] == current_year]                  # Only the record of a team in the same year is relavent. (outcome[1] = game year)
            for num, outcome in enumerate(year_game_outcomes):               
                game_pct_attributes[outcome[0]] = self._get_last_n_games_pct(year_game_outcomes[: num + 1], num_games)
            current_year += 1
        return game_pct_attributes

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

    def get_offensive_features(self, offensive_features, player_id, game_id, num_features=2):

        """# Function Description: Retrieve the features of a given player prior to entering the new game. The features are available from the previous game.
        # Function Parameters: offensive_features (Dict: A dictionary containing all the offensive features of a player.), 
        #    player_id (String: The player id associated in which we wish to retrieve the data.), 
        #    game_id (String: The game id needed to look backwards.), num_features (Int: The number of features returned for a player.)
        # Function Throws: Nothing
        # Function Returns: A list containing the offensive features. The amount of features was determined in previous queries but does not matter in this function.
        #    If the player does not have much data, I will be returning -1 to signal the prescence of a new player.
        # Function Notes: If we get to the end, the game ID was not found. This occurs when the player participates in a game but does not contribute 
        # to an 'offensive feature'. For instance, the player gets a SH but nothing else. This will also cause an error when attempting to 
        # retrieve contents from the 'offensive_features' dictionary since nothing will even be inserted.""" 
        
        if player_id in offensive_features:
            player_stats = offensive_features[player_id]
        else:
            return [-1 for i in range(0, num_features)]
        if len(player_stats) < 4:                          # Not enough games played to create reasonable stats.
            return [-1 for i in range(0, num_features)]
        for idx, games in enumerate(player_stats):
            if games[0] == game_id:                        # NOTE: Can this be optimised with using numpy arrays?
                return player_stats[idx - 1][1:]           # Return the stats from the day before. Should we particularily focus on a seaosn? Should things get a rest?
        return [-1 for i in range(0, num_features)]                                    
        
    def sub_offensive_features(self, offensive_features, batters, game_id):

        """ Function Description: Substitute the batters ids provided with the batting features. The features will be returned in the same order the names are provided.
        # Function Parameters: offensive_features (Dict: The dictionary containing the player ids that are tied to the offensive features.) 
        #    batters (List: The player ids we wish to retrieve the data for.), game_id (String: The game id needed to look backwards.) 
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

        """ Function Description: Given a list of stats, normalise the contents within the list.
        # Function Parameters: features (List: The features.), num_feats (Int: The number of features to segregate.)
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

    def get_game_features(self, all_batters, offensive_features, all_pitchers, starting_pitchers, relief_pitchers, pitching_features, winning_pct, game_stats):

        """# Function Description: Get all the features for a given game id. This involves getting the players who played in the game and then retrieving their associated features.
        # Function Parameters: all_batters (Dict: All of the batters information.), 
        #    offensive_features (Dict: All of the offensive features that are used to predict outcome.), 
        #    all_pitchers (Dict: The dictionary containing all the pitchers who participated in every game.),
        #    starting_pitchers (Dict: The starting pitchers in all the games.), 
        #    relief_pitchers (Dict: The relief pitchers in all the games.), 
        #    pitching_features (Dict: The pitching features in all the games. (Both relievers and starters.)),
        #    game_stats (Dict: The game id with all pertinent information.), 
        #    winning_pct (Dict: The n game rolling winning percentage.)
        # Function Throws: ValueError (Thrown when the incorrect number of features are returned.)
        # Function Returns: A single list containing the features of the game."""

        game_features = []
        game_id = game_stats[0]
        home_team = game_stats[6]
        vis_team = game_stats[7]
        # Acquire Home Stats
        game_features += self.sub_pitching_features(pitching_features, [self.get_starting_pitcher(starting_pitchers, game_stats[0], game_stats[6])], game_stats[0])       # The location of the home team within the games list.
        game_features += self.sub_offensive_features(offensive_features, self.get_starting_batters(all_batters, game_stats[0], 1), game_stats[0])
        game_features += self.sub_relief_pitching_features(pitching_features, self.get_relief_pitchers(all_pitchers, relief_pitchers, game_stats[0], game_stats[6], game_stats[1]), game_stats[0])
        game_features.append(winning_pct[game_id][home_team])
        # Acquire Away Stats
        game_features += self.sub_pitching_features(pitching_features, [self.get_starting_pitcher(starting_pitchers, game_stats[0], game_stats[7])], game_stats[0])
        game_features += self.sub_offensive_features(offensive_features, self.get_starting_batters(all_batters, game_stats[0], 0), game_stats[0])
        game_features += self.sub_relief_pitching_features(pitching_features, self.get_relief_pitchers(all_pitchers, relief_pitchers, game_stats[0], game_stats[7], game_stats[1]), game_stats[0])
        game_features.append(winning_pct[game_id][vis_team]) 
        if len(game_features) != 62: raise ValueError("The correct number of features was not returned.")
        return game_features

    def _compile_game_features(self, fp):

        """ Function Description: Gather all the features from every game and separate them into X and Y.
        # Function Parameters: fp (Feature_Pack: The containmnet of all features into one object for better organisation.)
        # Function Throws: Nothing
        # Function Returns: X, Y (List: The containment of all features.), (List: The outcomes of every game.)
        """
        lh = Log_Helper()
        X = []
        Y = []
        num_games = len(fp.game_outcomes)
        lh.print_progress_bar(0, num_games, prefix = 'Progress:', suffix = 'Complete', length = 50)    # Initial call to print 0% progress
        for num, game_stats in enumerate(fp.game_outcomes):
            try:
                X.append(self.get_game_features(fp.all_batters, fp.offensive_features, fp.all_pitchers, fp.starting_pitchers, fp.relief_pitchers, fp.pitching_features, fp.winning_pct, game_stats))
                Y.append(game_stats[8])
            except Exception as e:
                print("An error as occurred at {}. The error: {}".format(game_stats[0], str(e)))
            lh.print_progress_bar(num + 1, num_games, prefix = 'Progress:', suffix = 'Complete', length = 50)
        return X, Y

    def get_all_game_features(self, fp, query_loc, get_again_flag=False):

        """ Function Description: Retrieve the features for every single game and return it has a list.
        # Function Parameters: fp (Feature_Pack: All the features in one object.)
        #    query_loc (String: The location of results of previous queries.), 
        #    get_again_flag (Boolean: The function will call the database overwriting the results. (CI))
        # Function Throws: Nothing
        # Function Returns: X, Y (List: The containment of all features.), (List: The outcomes of every game.) 
        """

        if get_again_flag == False:                                                    # Use the information already provided.
            with open(query_loc, 'rb') as f:
                return load(f), [game_stats[8] for game_stats in fp.game_outcomes]     # Returning X, Y. Y does not need to be stored since it is quick to derive.
        X, Y = self._compile_game_features(fp)   
        with open(query_loc, 'wb') as f: dump(X, f)
        return X, Y