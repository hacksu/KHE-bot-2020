import discord
import asyncio
from datetime import *
import random


class MyClient(discord.Client):

    
    #ON MESSAGE
    async def on_message(self,message):
        if(message.content.startswith("/")):
            await self.process_commands(message)


    #PROCESS COMMANDS
    async def process_commands(self,message):
        command = message.content.split()[0].lower()
        #Command List Here
        if(command == "/create_team"):
            await self.create_team(message)

    async def create_team(self,message):
        teams_cat = self.get_channel(763785871278211082)
        team_num = 0
        for channel in text_channels:
            team_num = int(channel.name.split(" - ")[0].replace("Team ",""))
        team_num += 1
        print("Creating Team",team_num)
        
        


    async def on_ready(self): #This command will be called whenever the bot is first created and is ready to recieve input. This is different from being connected to Discord's servers.
        #await self.change_presence(activity=discord.Game(name="/build_team"))
        pass

    #CONNECTION
    async def on_connect(self):
        print("Bot has connected to server at time:",datetime.now())
    
    #DISCONNECTION
    async def on_disconnect(self):
        print("Bot has disconnected from server at time:",datetime.now())



print("Team Building")
bot = MyClient()
file = open("config.json",'r')
TOKEN = eval(file.read())["token"]
file.close()
#print(TOKEN)
bot.run(TOKEN)
