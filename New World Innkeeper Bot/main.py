from asyncio.windows_events import NULL
from logging import NullHandler
import discord
from discord import channel
from discord import message
from discord import member
from discord.ext import commands,tasks
from discord.ext.commands import bot
from discord.utils import get
from halo import Halo
import pickle

# init ######################################################################################################

class server:
    def __init__(self,id):
        self.id = id
        self.total = 0
        self.role_id = NULL

    def add_total(self, input):
        self.total = self.total + input
        pickle.dump(serverlist,open('save.dat','wb'))

# token
token = 'insert discord api token'

# init bot
client = commands.Bot(command_prefix = "$")
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
 
# events ######################################################################################################

@client.event
async def on_ready():
    global serverlist
    
    try:
        serverlist = pickle.load(open('save.dat', 'rb'))
    except:
        serverlist = []
        print('save data not found')
    
    print(' ')
    spinner = Halo(text='Innkeeper is online', spinner='dots', color='green')
    print(' ')
    spinner.start()

@client.event
async def on_message(message):
    
    global serverlist
    
    if message.author == client.user:
        return

    if (message.content.startswith('$')):
        await client.process_commands(message)
    else:
        for i in serverlist:
            if i.id == message.channel.id:
                try:
                    i.add_total(round(float(message.content),2))

                    embed = discord.Embed(title='Treasury', description=f'<@{message.author.id}> added {message.content}, new total = {i.total}')

                    await message.channel.send(embed=embed)
                except:
                    await message.channel.send('invalid input, enter a postive or negative number')

@client.event
async def on_raw_reaction_add(payload):

    try:
        
        message_id = payload.message_id
        print('message recieved')

        if message_id == 898276229256466503:
            
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

            print(payload.emoji.name)

            if payload.emoji.name == '⚔️':
                print('dps')
                role = discord.utils.get(guild.roles, name='DPS')

            if payload.emoji.name == '🩹':
                print('healer')
                role = discord.utils.get(guild.roles, name='Healer')

            if payload.emoji.name == '🏹':
                print('ranged')
                role = discord.utils.get(guild.roles, name='Ranged')

            if payload.emoji.name == '🛡️':
                print('tank')
                role = discord.utils.get(guild.roles, name='Tank')
            
            if role is not None:
                
                member = payload.member
                
                if member is not None:
                    await member.add_roles(role)
                else:
                    print('member not found')
            else:
                print('role not found')
    except:
        print('error with role assignment')


# commands ######################################################################################################

@client.command()
async def bank(ctx):

    global serverlist

    m = ctx.message
    s = server(m.channel.id)
    serverlist.append(s)
    pickle.dump(serverlist,open('save.dat','wb'))

    embed = discord.Embed(title='Treasury Active', description=f'Channel marked for treasury logging. Enter positive or negative numbers to adjust total.')
    await ctx.send(embed=embed)

@client.command()
async def update(ctx,input):

    global serverlist

    m = ctx.message

    for i in serverlist:
        if i.id == m.channel.id:
            try:
                i.total = float(input)

                pickle.dump(serverlist,open('save.dat','wb'))

                embed = discord.Embed(title='Treasury', description=f'<@{m.author.id}> updated the total to {i.total}')
                await ctx.send(embed=embed)
            except:
                await m.channel.send('invalid input, enter a postive or negative number')


# blocking ######################################################################################################

client.run(token)
