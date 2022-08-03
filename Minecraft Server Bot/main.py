from asyncio.windows_events import NULL
from logging import NullHandler
from asyncio.exceptions import SendfileNotAvailableError
import discord
from discord import channel
from discord import message
from discord import member
from discord.ext import commands,tasks
from discord.ext.commands import bot
from discord.utils import get
from halo import Halo
import json
from mcipc.query import Client
import mcipc.rcon.je.commands 
import os
import subprocess
import time

# init ######################################################################################################

global is_running
global server_obj

is_running = False

with open('bot/config.json') as json_file:
    data = json.load(json_file)
    TOKEN = data['token']

client = commands.Bot(command_prefix = ">")

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# function ####################################################################################################

def connect():

    with open('bot/config.json') as json_file:
        data = json.load(json_file)
        PORT = data["port"]
        PW = data['pw']
        IP = data['ip']
    global is_running
    print(' ')
    try:
        with Client(IP, PORT, passwd=PW) as server:
            print(f'connected to server on {IP}')
            is_running = True
            return True
    except:
        print('unable to connect to server')
        return False

# events ######################################################################################################

@client.event
async def on_ready():

    print('values loaded \n')

    print(' ')
    spinner = Halo(text='MC Bot is online', spinner='dots', color='green')
    print(' ')
    spinner.start()

# commands ######################################################################################################

@client.command()
@commands.has_role('Minecrafters')
async def server_stop(ctx):

    global server_obj
    global is_running

    if ctx.author == client.user:
        return

    with open('bot/config.json') as json_file:
        data = json.load(json_file)
        PORT = data["port"]
        PW = data['pw']
        IP = data['ip']
        
    try:
        with Client(IP, PORT, passwd=PW) as server:
            server.stop()
            server_obj.terminate()
        await ctx.send('server stopped')
    except:
        await ctx.send('error stopping server')

@client.command()
@commands.has_role('Minecrafters')
async def start(ctx):

    global server_obj
    
    if ctx.author == client.user:
        return

    global is_running

    try:
        server_obj = subprocess.Popen([r'run.bat'])
        is_running = True
        time.sleep(12)
        connect()
        await ctx.send('server started')
    except:
        await ctx.send('error with batch file')

@client.command()
@commands.has_any_role('Minecrafters')
async def info(ctx):
    with open('bot/config.json') as json_file:
        data = json.load(json_file)
        PORT = data["port"]
        IP = data['ip']
    
    with Client(IP, PORT) as client:
        full_stats = client.stats(full=True)

        full_stats_as_json = dict(full_stats)
        print(full_stats_as_json)
        embed = discord.Embed(title='Stats', description='info')
        await ctx.send(embed=embed)


        full_stats_as_json = dict(full_stats)
        print(full_stats_as_json)



# blocking ######################################################################################################

client.run(TOKEN)

# https://mcipc.readthedocs.io/en/latest/