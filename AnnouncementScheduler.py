import discord
import asyncio
import datetime
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
        if(command == "/schedule" and message.channel.id in [763838177189560351,767930560433356800]):
            await self.schedule(message)
            


    async def schedule(self,message):
        command = message.content.split()
        if(len(command) < 3):
            await message.channel.send("Invalid usage. Valid usage:```/schedule hh:mm description```Please make sure you use 24 Hour time!")
            return

        time = datetime.datetime.strptime(command[1],"%H:%M")

        while(not self.open):
            pass
        self.open = False
        file = open("data/announcements.txt",'a')
        try:
            file.write(str([time," ".join(command[2:])])+", ")
            await message.channel.send("Announcement successfully set!")
        except UnicodeEncodeError:
            await message.channel.send("Unfortunately, due to an encoding error, I cannot support Unicode Emojis in Announcements.")
        file.close()
        self.open = True

        
        

            
        

    async def on_ready(self): #This command will be called whenever the bot is first created and is ready to recieve input. This is different from being connected to Discord's servers.
        self.khe = self.get_guild(755074904155488296)
        self.open = True
        while(not self.is_closed()):
            time = datetime.datetime.now()
            file = open("data/announcements.txt",'r')
            data = "["+file.read()+"]"
            if(data == "[]"):
                await asyncio.sleep(15)
                continue
            print(data)
            data = eval(data)
            file.close()
            remove = []
            for event in data:
                print("EVE:",event)
                if(time.hour == event[0].hour and time.minute == event[0].minute):
                    await self.get_channel(763838177189560351).send(event[1])
                    remove.append(event)
            for event in remove:
                data.remove(event)
            while(not self.open):
                pass
            self.open = False
            file = open("data/announcements.txt",'w')
            for event in data:
                file.write(str(event)+",")
            file.close()
            self.open = True
            await asyncio.sleep(15)
        

    #CONNECTION
    async def on_connect(self):
        print("Bot has connected to server at time:",datetime.datetime.now())
    
    #DISCONNECTION
    async def on_disconnect(self):
        print("Bot has disconnected from server at time:",datetime.datetime.now())



print("Announcements")
bot = MyClient()
file = open("config.json",'r')
TOKEN = eval(file.read())["token"]
file.close()
#print(TOKEN)
bot.run(TOKEN)
