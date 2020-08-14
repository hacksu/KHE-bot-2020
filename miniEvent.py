# Reminder every time /miniEvent
#Reminder automatic one hour, 15 minutes, and right before
#Mini Events
# 1. Trivia 5pm
# 2. Jackbox 10pm
# 3. Bob Ross 12am
# 4. Yoga 4am
# 5. Chess 10am


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


    #await message.channel.send()

    #WHEN READY
    async def process_commands(self,message):
        # For not automatic code
        # Store variable constants for the time of the event
        # Command and parameter is the variable name, Ex. /miniEvent Trivia
        # Find the time difference from the variable stored and now [str(datetime.now())] millitary time 
        # Print difference 

        self.get_channel(737741628005154945)
        command = message.content.split()

        if command[1] == "Trivia":
            t1 = timedelta(hours=17, minutes=00)
            now = datetime.now()
            time = now - t1
            output = time.strftime("%H")
            await message.channel.send("We have" + output +"hours until Trivia. Get ready to show off your knowledge and have some fun!")
        elif command[1] == "Jackbox":
            t1 = timedelta(hours=21, minutes=00)
            now = datetime.now()
            time = now - t1
            output = time.strftime("%H")
            await message.channel.send("We have" + output +"hours until JackBox gaming starts!")
        elif command[1] == "BobRoss":
            t1 = timedelta(hours=00, minutes=00)
            now = datetime.now()
            time = now - t1
            output = time.strftime("%H")
            await message.channel.send("We have"+output+"hours until Bob Ross MS Paint. Come paint some happy little trees with us!")
        elif command[1] == "Yoga":
            t1 = timedelta(hours=4, minutes=00)
            now = datetime.now()
            time = now - t1
            output = time.strftime("%H")
            await message.channel.send("We have"+ output+"hours until we relax with some awesome yoga!")
        elif command[1] == "Chess":
            t1 = timedelta(hours=10, minutes=00)
            now = datetime.now()
            time = now - t1
            output = time.strftime("%H")
            await message.channel.send("We have" + output +"hours until the Chess tournament starts!")
        else:
            await message.channel.send("That is not a mini event at KHE this year :(")
   

    async def on_ready(self): #This command will be called whenever the bot is first created and is ready to recieve input. This is different from being connected to Discord's servers.
        await self.change_presence(activity=discord.Game(name="/miniEvent")) #This line sets the bot's game presence to say "/time"

    #CONNECTION
    async def on_connect(self):
        print("Bot has connected to server at time:",datetime.now())
    
    #DISCONNECTION
    async def on_disconnect(self):
        print("Bot has disconnected from server at time:",datetime.now())



print("Mini Event")
bot = MyClient()
file = open("config.json",'r')
TOKEN = eval(file.read())["token"]
#print(TOKEN)
bot.run(TOKEN)