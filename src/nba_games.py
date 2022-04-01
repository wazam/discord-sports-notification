from os import getenv
from requests import get

class NBAGamesChecker():
    def __init__(self):
        self.notified_games = {}
        self.config = {
            'pt_differential': int(getenv('NBA_PT_DIFFERENTIAL')),
            'mins_left': int(getenv('NBA_MINS_LEFT')),
            'period': int(getenv('NBA_PERIOD'))
        }
    
    def update_config(self, config):
        self.config = config

    def get_config(self):
        return self.config

    def get_games(self):
        resp = get('https://data.nba.net/10s/prod/v2/today.json')
        data = resp.json()
        scoreboard_endpoint = data['links']['todayScoreboard']
        todays_games_resp = get("https://data.nba.net/10s" + scoreboard_endpoint)
        todays_games_data = todays_games_resp.json()
        return todays_games_data

    def check_games(self):
        todays_games_data = self.get_games()
        todays_games = todays_games_data['games']

        games_to_notify = []

        for game in todays_games:
            home = game['hTeam']
            away = game['vTeam']

            if game['isGameActivated'] and game['period']['current'] >= self.config['period']:
                clock = game['clock'].split(':')
                
                if len(clock) < 2:
                    minutes = 0
                else:
                    minutes = int(clock[0])

                pts_difference = abs(int(home['score']) - int(away['score']))

                current_period = game['period']['current']
                period = ""
                if current_period > 4:
                    period = (str(current_period % 4) + 'OT')
                else:
                    period = str(current_period) + 'Q'

                if minutes <= self.config['mins_left'] and pts_difference <= self.config['pt_differential']:
                    found_game = self.notified_games.get(game['gameId'])

                    if found_game == None:
                        time_left = period + ' ' + game['clock']

                        home_text = home['triCode'] + ' ' + str(home['score'])
                        away_text = away['triCode'] + ' ' + str(away['score'])

                        self.notified_games[game['gameId']] = game['homeStartDate']
                        games_to_notify.append({ "home_text": home_text, "away_text": away_text, "time_left": time_left })
                    else:
                        continue

        return games_to_notify

    async def notify_games(self, channel):
        games_to_notify = self.check_games()

        for game in games_to_notify:
            await channel.send(f'{game["home_text"]}-{game["away_text"]}-{game["time_left"]}')