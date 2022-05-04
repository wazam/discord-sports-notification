# Used to get environment variables
from os import getenv
# Used to load web pages
from requests import get

class MLBGamesChecker():
    def __init__(self):
        # Create new dictionary on startup to save all the Games which have sent out notifications
        self.notified_games = {}
        # Set config variables from environment variables on startup
        self.config = {
            # Set the earliest inning that a notification can activate for, innings less than value are ignored
            'min_inning': int(getenv('MLB_MINIMUM_INNING')),
            # Set the highest score-difference-between-teams that a notification can activate for, scores-differentials higher than value are ignored
            'score_diff': int(getenv('MLB_MAXIMUM_SCORE_DIFFERENTIAL')),
            # Set the minimum amount of baserunners that a notification can activate for, situations with less man on base than the value are ignored
            'men_on_base': getenv('MLB_THRESHOLD_MEN_ON_BASE')
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
        total_games = todays_games_data['totalGames']
        # Create new indexes to save games and their data into
        indiv_todays_games_arry = [], indiv_todays_games_resp = [], indiv_todays_games_data = []
        # Loop through all the number of games
        for i in range(total_games):
            # Get URL link for each Game's full details
            indiv_todays_games_arry[i] = todays_games_data['dates']['0']['games'][i]['link']
            # Load web page for each Games' full details
            indiv_todays_games_resp[i] = get("http://statsapi.mlb.com" + indiv_todays_games_arry[i])
            # Create index with JSON parsing of web page
            indiv_todays_games_data[i] = indiv_todays_games_resp[i].json()
        # Create index of today's Games to notify for in the current requested check of all Games
        games_to_notify = []
        # Loop through all the number of games
        for j in range(total_games):
            # Find Games in progress
            if str(indiv_todays_games_data[j]['gameData']['satus']['detailedState']) == "In Progress":
                # Find Games at least past the minimum inning threshold
                if int(indiv_todays_games_data[j]['liveData']['plays']['currentPlay']['about']['inning']) >= self.config['min_inning']:
                    # Find Games with score differentials lower than the maximum scoring threshold
                    if abs(int(indiv_todays_games_data[j]['liveData']['plays']['currentPlay']['result']['awayScore']) - int(indiv_todays_games_data[j]['liveData']['plays']['currentPlay']['result']['homeScore'])) <= self.config['score_diff']:
                        # Find Games with at least the minimum baserunners
                        if str(indiv_todays_games_data[j]['liveData']['plays']['currentPlay']['matchup']['splits']['menOnBase']) == self.config['men_on_base']:
                            # Find individual Game's MLB API ID in index of Games notifications have already been sent out for
                            found_game = self.notified_games.get(indiv_todays_games_data[j]['gamePk'])
                            # Find Games with no notifications already sent
                            if found_game == None:
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

    async def notify_games(self, channel):
        # Get index of new games to send notifcations for by checking all games and index of list of games already notified for
        games_to_notify = self.check_games()
        # Loop through all the new Games to send notifications for
        for game in games_to_notify:
            # Send Discord message of Game's details
            await channel.send(f'{game["home_text"]}-{game["away_text"]}-{game["time_left"]}')
            