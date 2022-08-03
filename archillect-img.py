# TOKEN d3544dc6-ef21-4d3e-a3c1-f96ce043f77d

token = "insert discord api token"

import extcolors
import requests
import json
import shutil
import discord
from discord.ext import tasks
import asyncio
import time
import os
import colorgram
from PIL import Image, ImageDraw, ImagePalette

def gatherIMG():

    response = requests.get('https://archillect.com/api/last/1?token=d3544dc6-ef21-4d3e-a3c1-f96ce043f77d')

    dictObj = json.loads(response.content)

    link = dictObj[0]['image']['original']

    filename = 'archillect.jpg' # writes to this file name

    r = requests.get(link, stream = True) # gets photo from link provided by 

    if r.status_code == 200:    # checks if the image was retrieved successfully

        r.raw.decode_content = True   # set decode_content value to True, otherwise the downloaded image file's size will be zero.
        
        with open(filename,'wb') as f:   #opens a local file with wb ( write binary ) permission.
            shutil.copyfileobj(r.raw, f)
            
        print('Image sucessfully Downloaded: ',filename)
    else:
        print('Image Couldn\'t be retreived')

# open target image
def createPalette():   
    start = time.time()
    im = Image.open('archillect.jpg')
    print('image aquired')
    for range in (0,2):
        print('...')

    # extract pallete from image
    print('extracting image...')
    colors = colorgram.extract(im, 5)
    print('extraction complete')

    # priming color objects

    color1 = colors[0]
    color2 = colors[1]
    color3 = colors[2]
    color4 = colors[3]
    color5 = colors[4]

    #create image for palette

    pallete = Image.new("RGB",(500, 100), (255, 255, 255))

    d = ImageDraw.Draw(pallete)

    #color1
    d.rectangle([(0, 0), (100, 100)],color1.rgb)

    #color2
    d.rectangle([(100, 0), (200, 100)],color2.rgb)

    #color3
    d.rectangle([(200, 0), (300, 100)],color3.rgb)

    #color4
    d.rectangle([(300, 0), (400, 100)],color4.rgb)

    #color5
    d.rectangle([(400, 0), (500, 100)],color5.rgb)

    pallete.show()

    end = time.time()

    for range in (0,2):
        print('...')

    print(f'completed in {end - start} seconds')

#######  DISCORD API  #######

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())



    async def my_background_task(self):
        await self.wait_until_ready()
        counter = 0
        channel = self.get_channel(790397696006946816) # channel ID goes here
        while not self.is_closed():
            counter += 1
            gatherIMG()
            createPalette()
            #extractPalette()
            #colors, pixel_count = extcolors.extract_from_path("archillect.jpg")
            await channel.send(file=discord.File("archillect.jpg"))
                

            await asyncio.sleep(900) # task runs every 60 seconds


client = MyClient()
client.run(token)

#   python desktop\bot.py


    

