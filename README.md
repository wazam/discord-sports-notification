# [Sports Now!!!](https://github.com/wazam/discord-sports-notification)

A Discord bot for sending sports notifications, made in [Python](https://www.python.org/). A message is sent notifying users in a channel when an almost-completed sports game has a close score between the teams. 98% umpball-free. The last 2% is the hardest to get. That's why they leave it in the milk.

## Installation

### Manual

1. Install [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), [docker-compose](https://docs.docker.com/compose/install/), and [docker](https://docs.docker.com/engine/install/) if needed.
2. [Clone](https://git-scm.com/docs/git-clone) the repo.
```sh
git clone https://github.com/wazam/discord-sports-notification.git
```
3. Change to the current working directory.
```sh
cd ./discord-sports-notification
```
4. Copy the `.env.example` file and rename it to `.env`.
5. Add your Discord secret_token and channel_ID from [discord.com](https://discord.com/developers/applications) to the `.env` file.
6. Enable additional bot settings. ![](docs/additional-discord-bot-settings.jpg)
7. Add the bot to your server.
7. [Run](https://docs.docker.com/compose/reference/up/) the ```docker-compose.yml``` file to build and run the app.
```sh
docker-compose up -d
```

### Docker-compose
```sh
---
version: "3.9"
services:
  bot:
    image: ghcr.io/wazam/discord-sports-notification:main
    environment:
      - DISCORD_SECRET_TOKEN={YOUR_VALUE}
      - DISCORD_CHANNEL_ID={YOUR_VALUE}
```

### Docker
```sh
docker run -d \
  -e DISCORD_SECRET_TOKEN={YOUR_VALUE} \
  -e DISCORD_CHANNEL_ID={YOUR_VALUE} \
  ghcr.io/wazam/discord-sports-notification:main
```

## Example

![](docs/example-discord-notifcations.jpg)

## Bot Commands

- ```help``` displays all commands.
- ```games``` or ```today``` displays amount of games today.

## Supported Sports

| League | Available |
| :----: | :----: |
| [NBA (National Basketball Association)](https://data.nba.net/10s/prod/v2/today.json) | ✅ |
| [MLB (Major League Baseball)](http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1) | ✅ |
| [NFL (National Football League)](http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard) | ❌ |
| [NHL (National Hockey League)](https://statsapi.web.nhl.com/api/v1/schedule) | ❌ |
| [NCAA Men's Baseball](https://site.api.espn.com/apis/site/v2/sports/baseball/college-baseball/scoreboard) | ❌ |
| [NCAA Men's Basketball](http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard) | ❌ |
| [NCAA Football](http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard) | ❌ |
| [MLS (Major League Soccer)](http://site.api.espn.com/apis/site/v2/sports/soccer/usa.1/scoreboard) | ❌ |
| [EPL (English Premier League)](http://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard) | ❌ |

## Disclaimers

- [NBA Terms of Use](https://www.nba.com/termsofuse)
- [MLB Terms of Use](https://www.mlb.com/official-information/terms-of-use)
- [MLB Copyright](https://gdx.mlb.com/components/copyright.txt)
- [NHL Terms of Service](https://www.nhl.com/info/terms-of-service)
- [ESPN Terms of Use](https://web.archive.org/web/20220409030827/http://www.espn.com/apis/devcenter/terms.html)
- [Disney Terms of Use](https://disneytermsofuse.com/english/)
- [Discord Terms of Service](https://discord.com/terms)
- [Discord Community Guidelines](https://discord.com/guidelines)
- [OpenWeatherMap Terms of Use](https://openweather.co.uk/storage/app/media/Terms/Openweather_website_terms_and_conditions_of_use.pdf)
