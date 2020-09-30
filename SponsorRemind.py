import discord
import asyncio
from datetime import *


class MyClient(discord.Client):

    
    #ON MESSAGE
    async def on_message(self,message):
        if(message.content.startswith("/")):
            await self.process_commands(message)



    #PROCESS COMMANDS
    async def process_commands(self,message):
        command = message.content.split()[0].lower()
        #Command List Here


    #WHEN READY
    async def on_ready(self):
        self.TIME_MINUTES = 60 # 60 is the maximum value allowed right now
        #await self.change_presence(activity=discord.Game(name = "game"))
        #print("Successfully set Bot's game status")
        file = open("data/thankyous.txt")
        sponsors = eval(file.read())
        file.close()
        crnt = 0
        MAX = len(sponsors)
        last_hour_minute = (None,None)
        while(not self.is_closed()):
            time = datetime.now()
            print((time.hour,time.minute),last_hour_minute)
            if(time.minute % self.TIME_MINUTES == 0 and (time.hour,time.minute) != last_hour_minute):
                await self.get_channel(743227401085124649).send(sponsors[crnt])
                crnt = (crnt + 1) % MAX
                last_hour_minute = (time.hour,time.minute)
                print("SENT!")
            await asyncio.sleep(30)
                
            


    #CONNECTION
    async def on_connect(self):
        print("Bot has connected to server at time:",datetime.now())
    
    #DISCONNECTION
    async def on_disconnect(self):
        print("Bot has disconnected from server at time:",datetime.now())



print("Starting KHE Sponsor Thank You Manager")
bot = MyClient()
file = open("config.json",'r')
TOKEN = eval(file.read())["token"]
#print(TOKEN)
bot.run(TOKEN)
