from os import getenv
from requests import get
from urllib.request import urlopen

class MLBGamesChecker():
    def __init__(self):
        self.notified_games = {}
        self.config = {
            'min_inning': int(getenv('MLB_MINIMUM_INNING')),
            'score_diff': int(getenv('MLB_MAXIMUM_SCORE_DIFFERENTIAL')),
            'men_on_base': getenv('MLB_THRESHOLD_MEN_ON_BASE')
        }

    def update_config(self, config):
        self.config = config

    def get_config(self):
        return self.config

    def get_games(self):
        todays_games_resp = get('http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1')
        todays_games_data = todays_games_resp.json()
        return todays_games_data

    def get_streams(self,home_team,away_team):
        url = "https://redditmlbstreams.live/"
        page = urlopen(url)
        html = page.read().decode("utf-8")
        start_index = html.find("<a rel=\"\" target=\"_self\" href=\"") + len("<a rel=\"\" target=\"_self\" href=\"")
        end_index_search = "\"><span style=\"min-height:35px\" class=\"competition-cell-table\"><span class=\"competition-cell-table-cell competition-cell-side1\"><span class=\"name\"> <!-- -->" + str(home_team)
        end_index = html.find({end_index_search})
        if end_index == 0:
            end_index_search = "\"><span style=\"min-height:35px\" class=\"competition-cell-table\"><span class=\"competition-cell-table-cell competition-cell-side1\"><span class=\"name\"> <!-- -->" + str(away_team)
            end_index = html.find({end_index_search})
        stream_link_path = html[start_index:end_index]
        stream_link = "https://redditmlbstreams.live" + stream_link_path
        return stream_link

    def check_games(self):
        todays_games_data = self.get_games()
        total_games = todays_games_data['totalGames']

        indiv_todays_games_arry = [], indiv_todays_games_resp = [], indiv_todays_games_data = []
        for i in range(total_games):
            indiv_todays_games_arry[i] = todays_games_data['dates']['0']['games'][i]['link']
            indiv_todays_games_resp[i] = get("http://statsapi.mlb.com" + indiv_todays_games_arry[i])
            indiv_todays_games_data[i] = indiv_todays_games_resp[i].json()

        games_to_notify = []
        for j in range(total_games):
            if str(indiv_todays_games_data[j]['gameData']['satus']['detailedState']) == "In Progress":
                if int(indiv_todays_games_data[j]['liveData']['plays']['currentPlay']['about']['inning']) >= self.config['min_inning']:
                    if abs(int(indiv_todays_games_data[j]['liveData']['plays']['currentPlay']['result']['awayScore']) - int(indiv_todays_games_data[j]['liveData']['plays']['currentPlay']['result']['homeScore'])) <= self.config['score_diff']:
                        if str(indiv_todays_games_data[j]['liveData']['plays']['currentPlay']['matchup']['splits']['menOnBase']) == self.config['men_on_base']:
                            found_game = self.notified_games.get(indiv_todays_games_data[j]['gamePk'])

                            if found_game == None:
                                time_left = str(indiv_todays_games_data[j]['liveData']['linescore']['inningHalf']) + ' of the ' + str(indiv_todays_games_data[j]['liveData']['linescore']['currentInningOrdinal'])

                                home_text = str(indiv_todays_games_data[j]['gameData']['teams']['home']['abbreviation']) + ' ' + str(indiv_todays_games_data[j]['liveData']['plays']['currentPlay']['result']['homeScore'])
                                away_text = str(indiv_todays_games_data[j]['gameData']['teams']['away']['abbreviation']) + ' ' + str(indiv_todays_games_data[j]['liveData']['plays']['currentPlay']['result']['awayScore'])

                                stream_link = self.get_streams(str(indiv_todays_games_data[j]['gameData']['teams']['home']['name']),str(indiv_todays_games_data[j]['gameData']['teams']['away']['name']))

                                self.notified_games[indiv_todays_games_data[j]['gamePk']] = indiv_todays_games_data[j]['gameData']['datetime']['officialDate']
                                games_to_notify.append({ "home_text": home_text, "away_text": away_text, "time_left": time_left, "stream_link": stream_link })
                            else:
                                continue

        return games_to_notify

    async def notify_games(self, channel):
        games_to_notify = self.check_games()

        for game in games_to_notify:
            await channel.send(f'{game["home_text"]}-{game["away_text"]}-{game["time_left"]}-{game["stream_link"]}')