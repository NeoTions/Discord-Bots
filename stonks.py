# discord bot that updates it's status with a particular stocks price
token = 'insert discord api key'

import discord
from discord.ext import commands,tasks
from discord.utils import get
from yahoo_fin import stock_info as si
import datetime
from stockTools import stockStats, currentTime
import math

cycles = 0

stock = 'GME'

# command prefix
client = commands.Bot(command_prefix = '$')

@client.command
async def help(ctx):
    embed = discord.Embed(title='User Commands')
    embed.add_field(name='$help', value='list of commands')

@client.command()       
async def display(ctx : discord.Message, newStock):
    global stock
    prevStock = stock
    stock = newStock.upper()
    print(stock)

    try:
        stockStats(stock)
        await ctx.send(f"Display stock is now '{stock}'")
    except:
        stock = prevStock
        await ctx.send('Invalid stock symbol. Search for symbols @ https://www.marketwatch.com/tools/quotes/lookup.asp')
        



@client.event
async def on_ready():
    # starts loop for tracking price
    change_activity.start()
    print('bot is ready')
    



@tasks.loop(seconds=10)
async def change_activity():


    global cycles
    global stock

    cycles = cycles + 1

    # finds the current minute, hour, and weekday
    minute, hour, day = currentTime()

    # gets quote, percent, and changes character to ▲ or ▼
    quote, perc, char = stockStats(stock)

    roundedQuote = round(quote, 2)


    # checks to see time is within trading hours and sets status to idle or online
    if day > 4:
        print('Currently Offline (after trading hours)')
        currentStatus = discord.Status.idle
    elif hour < 10 and minute < 30 or hour > 16:
        print('Currently Offline (after trading hours)')
        currentStatus = discord.Status.idle
    else:
        print('Currently Online (trading hours)')
        currentStatus = discord.Status.online





    print('Current Display Stock: ' + str(roundedQuote))
    print('Quote: ' + str(roundedQuote))
    print('Change since last close: ' + str(perc) + char + '% ')
    print(f'Running for {cycles} cycles')
    print(' ')
    print(' ')


    await client.change_presence(status=currentStatus,activity=discord.Activity(type=discord.ActivityType.watching, name=stock + ' ' + ': ' + str(roundedQuote) + ' ' + char + str(perc) + '%'))





# runs bot (blocking)
client.run(token)




# bot could send a message to a channel, and an event could take the message and change the bots nickname using the message context object
