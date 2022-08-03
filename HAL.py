# discord server management bot
import discord
from discord.ext import commands
from discord.utils import get
from PyDictionary import PyDictionary
import urbandict as ud

client = commands.Bot(command_prefix = ".")

dictionary=PyDictionary()

async def connection():

    await client.connect()

token = 'insert discord api key'

# when bot is ready (console)
@client.event
async def on_ready():
    print('ready')

# prints ping to chat where command is given
@client.command()
async def ping(ctx):
    await ctx.send(f'ping {round(client.latency * 1000)}ms')
    

@client.command()
async def hello(ctx : discord.Message):
    await ctx.send(f"hello <@{ctx.author.id}>")


@client.command()
async def define(ctx : discord.Message, word):
    
    
    try:
        response = dictionary.meaning(word)
        for i in response:
            wordClass = i

        data = response[wordClass]

        define = data[0]

        define = define[0].upper() + define[1:]



        #print(define)

        # Initial character upper case 
        word = word[0].upper() + word[1:] 
        
        embed = discord.Embed(title=word, description='*' + wordClass + '*' + ' — ' + define)
        
        await ctx.send(embed=embed)
    except:
        print(word) 
        wordType = type(word)
        await ctx.send('Unknown word, verify spelling is correct or use ".urbandict"')
        #await ctx.send(word + '///////' + str(wordType))


@client.command()
async def urbandict(ctx : discord.Message, word):
    
    try:
        response = ud.define(word)
        
        data = response[0]

        define = data['def']
        #print(define)

        # Initial character upper case 
        word = word[0].upper() + word[1:] 
        
        embed = discord.Embed(title=word, description='From Urban Dictionary — ' + define)
        
        await ctx.send(embed=embed)
    except:
        print(word) 
        wordType = type(word)
        await ctx.send("Unknown word. If it ain't here it doesn't exist")
        #await ctx.send(word + '///////' + str(wordType))

@client.command()
async def name(ctx : discord.Message):
    await ctx.send(f"hello <@{ctx.author.id}>")

# blocking
client.run(token)








