import os
from os import environ
from datetime import datetime, timedelta
import requests
import discord
from discord.ext import commands, tasks

from utils.basketball import NBAGamesChecker
from utils.baseball import MLBGamesChecker
import utils.weather
# import utils.music


command_prefix = environ.get('BOT_PREFIX', '!')
intents=discord.Intents.all()  #Intents.default() ?
description = 'A Discord bot for sending sports notifications.'
activity = discord.Activity(type=discord.ActivityType.watching, name=command_prefix + 'help')
status = discord.Status.online
bot = commands.Bot(command_prefix=command_prefix, intents=intents, description=description, activity=activity, status=status, case_insensitive=True)

NBA_enabled = environ.get('NBA_ENABLED', True)
MLB_enabled = environ.get('MLB_ENABLED', True)
refresh_rate = float(environ.get('BOT_REFRESH', 300))

url_user_agent = str('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0')  #HTTP/1.1 ?

nba_checker = NBAGamesChecker()
mlb_checker = MLBGamesChecker()


@bot.event
async def on_ready():
    timestamp = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    msg = f'{bot.user.name} is online.'
    log = timestamp + ' INFO     ' + msg
    print(log, flush=True)
    notify_all_games.start()


@bot.command(name='sync', description='Syncs application commands to Discord.')
async def sync_command(ctx):
    cmd_list = await ctx.bot.tree.sync()
    msg = f'Synced {len(cmd_list)} commands.'
    await ctx.send(msg)


@bot.hybrid_command(name='ping', description='Checks Discord WebSocket protocol latency.')
async def ping_command(ctx):
    latency = round(bot.latency * 1000)
    msg = f'Pong! `{latency}ms`'
    await ctx.send(msg)


@bot.hybrid_command(name='passtheboof', aliases=['420'], description='Celebrate the holidays.')
async def passtheboof_command(ctx):
    msg = f'<:here:730885279774146611>'
    await ctx.send(msg)


@bot.hybrid_command(name='mets', aliases=['petealonso'], description='Mets game live stream.')
async def mets_command(ctx):
    msg = f'http://blabseal.org/coolbeans/'
    await ctx.send(msg)


@bot.hybrid_command(name='time', description='Checks timezone of bot.')
async def time_command(ctx):
    time_EST = datetime.today().strftime('%Y-%m-%d %H:%M:%S')  #- timedelta(hours=4)
    msg = f'{time_EST}'
    await ctx.send(msg)


@bot.hybrid_command(name='weather', description='Checks current weather of zip/post code or city/area name.')
async def weather_command(ctx, *, user_search):
    msg = utils.weather.lookup(user_search)
    await ctx.send(msg)


@bot.hybrid_command(name='games', aliases=['today'], description='Amount of sports games today.')
async def games_command(ctx):
    text = ''
    if NBA_enabled:
        num_nba_games = NBAGamesChecker().prefix_command_for_games()
        if num_nba_games > 0:
            text += str(num_nba_games)
        else:
            text += 'No'
        text += ' NBA game'
        if num_nba_games != 1:
            text += 's'
    if NBA_enabled and MLB_enabled:
        text += ' and '
    if MLB_enabled:
        todays_games_data = MLBGamesChecker().get_games()
        num_mlb_games = int(todays_games_data['totalGames'])
        if num_mlb_games > 0:
            text += str(num_mlb_games)
        else:
            text += 'No'
        text += ' MLB game'
        if num_mlb_games != 1:
            text += 's'
    if NBA_enabled or MLB_enabled:
        today_raw = datetime.today() - timedelta(hours=4)  # still needed?
        today = today_raw.strftime('%b %-d, %Y')
        text += ' today, ' + str(today) + '.'
    msg = f'{text}'
    await ctx.send(msg)


@tasks.loop(seconds=refresh_rate)
async def notify_all_games():
    channel = bot.get_channel(int(environ.get('DISCORD_CHANNEL_ID')))
    if NBA_enabled:
        nba_games_to_notify = nba_checker.check_games()
        for game in nba_games_to_notify:
            await channel.send(f':basketball: {game["home_text"]} - {game["away_text"]} - {game["time_left"]}')
    if MLB_enabled:
        mlb_games_to_notify = mlb_checker.check_games()
        for game in mlb_games_to_notify:
            await channel.send(f':baseball: {game["home_text"]} - {game["away_text"]} - {game["time_left"]}')


bot.run(environ.get('DISCORD_SECRET_TOKEN'))
