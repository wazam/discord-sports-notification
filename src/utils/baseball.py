# Used to get environment variables
from os import environ
# Used to load web pages
from requests import get

class MLBGamesChecker():
    def __init__(self):
        # Create new dictionary on startup to save all the Games which have sent out notifications
        self.notified_games = {}
        # Set config variables from environment variables on startup
        self.config = {
            # Set the earliest inning that a notification can activate for, innings less than value are ignored
            'MLB_INNING': int(environ.get('MLB_INNING', 9)),
            # Set the highest score-difference-between-teams that a notification can activate for, scores-differentials higher than value are ignored
            'MLB_RUN_DIFFERENTIAL': int(environ.get('MLB_RUN_DIFFERENTIAL', 1)),
            # Set the minimum amount of baserunners that a notification can activate for, situations with less man on base than the value are ignored
            'MLB_BASERUNNERS': environ.get('MLB_BASERUNNERS', 'RISP')
        }

    def update_config(self, config):
        # Update config value to replace environment variable value
        self.config = config

    def get_config(self):
        # Returns config value (either environment variable value or updated replacement)
        return self.config

    def get_games(self):
        # Load web page of today's games and their data
        todays_games_resp = get('http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1')
        # Create index with JSON parsing of web page
        todays_games_data = todays_games_resp.json()
        # Return index of today's games and their data
        return todays_games_data

    def check_games(self):
        # Get index of today's games and their data
        todays_games_data = self.get_games()
        # Get number of today's total games
        total_games = int(todays_games_data['totalGames'])
        # Create new list to save games and their data to
        indiv_todays_games_data = []
        # Loop through all games
        for j in range(total_games):
            resp = get("http://statsapi.mlb.com" + todays_games_data['dates'][0]['games'][j]['link'])
            # Create list with JSON parsing of each individual games' full details from individual URL
            indiv_todays_games_data.append(resp.json())
        # Create index of today's Games to notify for in the current requested check of all Games
        games_to_notify = []
        # Loop through all the number of games
        for j in range(total_games):
            # Find Games in progress
            if str(indiv_todays_games_data[j]['gameData']['status']['detailedState']) == "In Progress":
                # Find Games at least past the minimum inning threshold
                if int(indiv_todays_games_data[j]['liveData']['plays']['currentPlay']['about']['inning']) >= self.config['MLB_INNING']:
                    # Find Games with score differentials lower than the maximum scoring threshold
                    if abs(int(indiv_todays_games_data[j]['liveData']['plays']['currentPlay']['result']['awayScore']) - int(indiv_todays_games_data[j]['liveData']['plays']['currentPlay']['result']['homeScore'])) <= self.config['MLB_RUN_DIFFERENTIAL']:
                        # Set value to check baserunners situations which are inherently superseded by other conditions
                        MLB_BASERUNNERS_my_text = self.config['MLB_BASERUNNERS']
                        # Convert text to numerical ranking
                        if MLB_BASERUNNERS_my_text == "RISP":
                            MLB_BASERUNNERS_my_val = 2
                        elif MLB_BASERUNNERS_my_text == "Men_On":
                            MLB_BASERUNNERS_my_val = 1
                        elif MLB_BASERUNNERS_my_text == "Empty":
                            MLB_BASERUNNERS_my_val = 0
                        # Set value to check baserunners situations which are inherently superseded by other conditions
                        MLB_BASERUNNERS_game_text = str(indiv_todays_games_data[j]['liveData']['plays']['currentPlay']['matchup']['splits']['menOnBase'])
                        # Convert text to numerical ranking
                        if MLB_BASERUNNERS_game_text == "RISP":
                            MLB_BASERUNNERS_game_val = 2
                        elif MLB_BASERUNNERS_game_text == "Men_On":
                            MLB_BASERUNNERS_game_val = 1
                        elif MLB_BASERUNNERS_game_text == "Empty":
                            MLB_BASERUNNERS_game_val = 0
                        # Find Games with at least the minimum baserunners
                        if MLB_BASERUNNERS_game_val >= MLB_BASERUNNERS_my_val:
                            # Find individual Game's MLB API ID in index of Games notifications have already been sent out for
                            found_game = self.notified_games.get(indiv_todays_games_data[j]['gamePk'])
                            # Find Games with no notifications already sent
                            if found_game is None:
                                # Find current half of the current inning
                                time_left = str(indiv_todays_games_data[j]['liveData']['linescore']['inningHalf']) + ' of the ' + str(indiv_todays_games_data[j]['liveData']['linescore']['currentInningOrdinal'])
                                # Find home team's current score
                                home_text = str(indiv_todays_games_data[j]['gameData']['teams']['home']['abbreviation']) + ' ' + str(indiv_todays_games_data[j]['liveData']['plays']['currentPlay']['result']['homeScore'])
                                # Find away team's current score
                                away_text = str(indiv_todays_games_data[j]['gameData']['teams']['away']['abbreviation']) + ' ' + str(indiv_todays_games_data[j]['liveData']['plays']['currentPlay']['result']['awayScore'])
                                # Add Game's MLB API ID and date in index of notified Games
                                self.notified_games[indiv_todays_games_data[j]['gamePk']] = indiv_todays_games_data[j]['gameData']['datetime']['officialDate']
                                # Add current Game data to index of today's Games to notify for
                                games_to_notify.append({ "home_text": home_text, "away_text": away_text, "time_left": time_left })
                            # Find Games with a notification for the daily game already sent
                            else:
                                # Skip sending a new notifcation
                                continue
        # Return index of Games and their data
        return games_to_notify

# Used for executing directly when testing
if __name__ == "__main__":
    games_to_notify = MLBGamesChecker().check_games()
    for game in games_to_notify:
        print(f'{game["home_text"]} - {game["away_text"]} - {game["time_left"]}', flush=True)
