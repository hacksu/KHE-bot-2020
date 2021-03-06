import discord
import asyncio
from datetime import *
import random


class MyClient(discord.Client):

    
    #ON MESSAGE
    async def on_message(self,message):
        if(message.content.startswith("/")):
            if(message.content.split()[0] == "/build_team"):
                await self.add_user_to_team_building(message)
            elif(message.content.split()[0] == "/sort"):
                await self.sort(message)


    #PROCESS COMMANDS
    async def process_commands(self,message):
        command = message.content.split()[0].lower()
        #Command List Here
        print(command == "/sort")
        if(command == "/build_team"):
            await self.add_user_to_team_building(message)
        elif(command == "/sort"):
            await self.sort(message)

    async def sort(self,message):
        TEAM_SIZE = 3
        connections = {}
##        for x in self.people:
##            connections[x] = {}
##            for y in self.people:
##                if x == y:
##                    continue
##                connections[x][y] = 0
##                for key in self.people[y]:
##                    if(key in self.people[x]):
##                        connections[x][y] += 1
##        print(connections)
##        group_num = len(self.people) // TEAM_SIZE
        for x in self.people:
            for item in self.people[x]:
                if item not in connections:
                    connections[item] = [x]
                else:
                    connections[item].append(x)
        print(connections)
        if(len(self.people) % TEAM_SIZE == 0):
            group_num = len(self.people) // TEAM_SIZE
        else:
            group_num = (len(self.people) // TEAM_SIZE) - 1
        groups = []
        while(len(groups) < group_num):
            groups.append([])
            while(len(groups[-1]) != TEAM_SIZE):
                print(connections)
                maxGroup = connections[max(connections, key=lambda group: len(connections[group]))]
                #print("max",maxGroup)
                if(len(maxGroup) == 0):
                    break
                groups[-1].append(random.choice(maxGroup))
                for group in connections:
                    if(groups[-1][-1] in connections[group]):
                        connections[group].remove(groups[-1][-1])
        #print(groups)
        msg = "The made teams are:```\n"
        cnt = 1
        for team in groups:
            msg += "Team " + str(cnt) + "\n"
            for user in team:
                msg += "\t" + str(user) + " :: " + str(self.people[user]) + "\n"
            cnt += 1
        msg += "```"
        await message.channel.send(msg)
            
        
        

        



    async def add_user_to_team_building(self,message):
        if(message.author.id in self.people):
            await message.channel.send("You are already registered for Team Building!")
            return
        try:
            await message.author.send("Hello! In order to join the Team Building Activity, I need at least 1 and at most 5 technologies or skills that you have, so I can attempt to match you with similarly skilled people! Send at most 5 different words or phrases, and I'll register you! (If you don't want to do 5 things, type `done` to end early)")
            await message.channel.send(message.author.mention + " check your DM's for further instructions!")
        except discord.errors.Forbidden:
            await message.channel.send(message.author.mention + " I need to be able to DM you to add you to the Team Building Activity. Please right click on the server icon, select \"Privacy Settings\", and check the \"Allow direct messages from server members\"")
            return
        def check(msg):
            return type(msg.channel) == discord.DMChannel and msg.author == message.author
        terms = []
        for x in range(5):
            try:
                respons = await self.wait_for('message',check=check,timeout=60.0)
            except asyncio.TimeoutError:
                await message.author.send("Sorry, you took too long! If you still want to register, start the process again.")
                return
            if(respons.content == "done"):
                break
            else:
                terms.append(respons.content.lower())
                await message.author.send("`"+respons.content.lower()+"` added. "+str(4-x)+" left!")
        if(x == 0):
            await message.author.send("I need at least 1 term! It can be something minor! Please start the process over.")
            return
        self.people[message.author.id] = terms
        try:
            file = open("data/team_building_storage.txt",'w')
            file.write(str(self.people))
            file.close()
            await message.author.send("Great! I've successfully added you to the Team Building Event! You'll be added to a group when the activity begins.")
        except:
            await message.author.send("An unknown error occured. Please alert KHE Staff and then try again.")

    #WHEN READY
    async def process_commands(self,message):
        command = message.content.split()
   
    async def on_ready(self): #This command will be called whenever the bot is first created and is ready to recieve input. This is different from being connected to Discord's servers.
        await self.change_presence(activity=discord.Game(name="/build_team"))
        file = open("data/team_building_storage.txt",'r')
        self.people = eval(file.read())
        file.close()

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
