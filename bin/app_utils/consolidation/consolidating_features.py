# Script Description: Give the players and their features, the script will consolidate everything together
#     into a list ready to be modelled.
# Script Version: 1.0

from re import search

class Feature_Consolidater():

    def __init__(self):

        """Class Description: The script will consilidate all the necessary elements into a list readied to be modelled."""

        pass

    def get_starting_batters(self, batting_players, game_id, team_batting):

        # Function Description: Givin all the batting events in a game, extract the starting the lineup.
        # Function Parameters: batting_players (The dictionary containing all the events from all games.), 
        #    game_id (The game id you wish to extract the betting lineup.), team_batting (The batting team: The Visting Team is 0, the Home Team is 1.)
        # Function Throws: Nothing
        # Function Returns: The list of players in the batting lineup.
                                                        
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

        # Function Description: Extract the starting pitcher of the game.
        # Function Parameters: starting_pitchers (The dictionary containing all the games with their starting.), 
        #    game_id (The game id you wish to extract the betting lineup.), pitcher_team (The team the pitcher who plays on the team.)
        # Function Throws: Nothing
        # Function Returns: The pitcher of the starting pitcher.

        return starting_pitchers[game_id][pitcher_team]

    def get_offensive_features(self, offensive_features, player_id, game_id):

        # Function Description: Retrieve the features of a given player prior to entering the new game. The features are available from the previous game.
        # Function Parameters: player_id (The player id associated in which we wish to retrieve the data.), game_id (The game id needed to look backwards.)
        # Function Throws: Nothing
        # Function Returns: A list containing the offensive features. The amount of features was determined in previous queries but does not matter in this function.
        #    If the player does not have much data, I will be returning -1 to signal the prescence of a new player.

        player_stats = offensive_features[player_id]
        if len(player_stats) < 4:                          # Not enough games played to create reasonable stats.
            return [-1, -1]
        for idx, games in enumerate(player_stats):
            if games[0] == game_id:                        # NOTE: Can this be optimised with using numpy arrays?
                return player_stats[idx - 1][1:]           # Return the stats from the day before. Should we particularily focus on a seaosn? Should things get a rest?

    def sub_offensive_features(self, offensive_features, batters, game_id):

        # Function Description: Substitute the batters ids provided with the batting features. The features will be returned in the same order the names are provided.
        # Function Parameters: offensive_features (The dictionary containing the player ids that are tied to the offensive features.) 
        #    batters (The player id we wish to retrieve the data for.), game_id (The game id needed to look backwards.) 
        # Function Throws: Nothing
        # Function Returns: A complete list of the featues to be inputted into the model. The list will vary depending on the number of players and features for each player.

        game_offensive_features = []
        for batter in batters:
            game_offensive_features += self.get_offensive_features(offensive_features, batter, game_id)
        return game_offensive_features