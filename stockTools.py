# extra code for stonks bot
from yahoo_fin import stock_info as si
import datetime

def stockStats(stock):

    data = si.get_quote_table(stock)
    prevClose = data['Previous Close']
    quotePrice = data['Quote Price']

    ratio = (quotePrice - prevClose) / prevClose

    if ratio > 0:
        percent = int(ratio * 100)
        character = '▲'
    else:
        percent = int(abs(ratio) * 100)
        character = '▼'
    
    return quotePrice, percent, character

def currentTime():
    minute = datetime.datetime.now().minute
    hour = datetime.datetime.now().hour
    day = datetime.datetime.today().weekday()
    return minute, hour, day