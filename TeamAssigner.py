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
        if(command == "/create_team" and message.channel.id in [764183043141009428, 763838177189560351]): # #bot-commands, #hacksu-bot-commands
            await self.create_team(message)
        elif(command == "/invite" and message.channel.id in [764183043141009428, 763838177189560351]): # #bot-commands, #hacksu-bot-commands
            await self.invite(message)
        elif(command == "/leave_team" and message.channel.category.id == 763785871278211082):
            await self.leave(message)
        #elif(command == "/rename" and message.channel.category.id == 763785871278211082):
        #    await self.rename(message)

    async def rename(self,message):
        print("Here")
        if(len(message.content.split(" ")) == 1):
            await message.channel.send("You need to provide a name.")
            return
        teams_cat = self.get_channel(763785871278211082)
        base = "-".join(message.channel.name.split("-")[0:2])
        await message.channel.edit(name = base+"-"+"-".join(message.content.split(" ")[1:]))
        base = base.replace("-"," ").capitalize()
        print("Here2")
        for channel in teams_cat.voice_channels:
            if(channel.name.startswith(base)):
                await channel.edit(name = base+" "+" ".join(message.content.split(" ")[1:]))
                break
        await message.channel.send("Successfully changed the channel name!")

    async def create_team(self,message):
        teams_cat = self.get_channel(763785871278211082)

        for channel in teams_cat.text_channels:
            if(channel.overwrites_for(message.author).view_channel):
                await message.channel.send(message.author.mention+" You are already in a team!")
                return
        
        team_num = 0
        for channel in teams_cat.text_channels:
            team_num = int(channel.name.split("-")[1].replace("team ",""))
        team_num += 1
        print("Creating Team",team_num)
        created = await self.khe.create_text_channel("team-"+str(team_num),category=teams_cat,overwrites={
            message.author:discord.PermissionOverwrite(view_channel=True,send_messages=True,manage_messages=True), # Author
            self.khe.get_role(755076622100463676):discord.PermissionOverwrite(send_messages=False,view_channel=True), #Staff
            self.khe.get_role(755074904155488296):discord.PermissionOverwrite(view_channel=False), #Everyone
            })
        await self.khe.create_voice_channel("Team "+str(team_num),category=teams_cat,overwrites={
            message.author:discord.PermissionOverwrite(view_channel=True), # Author
            self.khe.get_role(755076622100463676):discord.PermissionOverwrite(view_channel=True,connect=False), #Staff
            self.khe.get_role(755074904155488296):discord.PermissionOverwrite(view_channel=False) #Everyone
            })        
        
        await created.send(message.author.mention + " Welcome to your Team's Private Workspace! No other teams will be able to look in here! Make sure you invite your other teammates using the `/invite` command in "+self.get_channel(764183043141009428).mention+".")

    async def invite(self,message):
        teams_cat = self.get_channel(763785871278211082)

        for channel in teams_cat.text_channels:
            if(channel.overwrites_for(message.author).view_channel):
                break
        else:
            await message.channel.send(message.author.mention+" You are currently not in a team! Have someone invite you into theirs, or create your own team using `/create_team`")
            return
        team_channel = channel
        if(len(message.mentions) == 0):
            await message.channel.send(message.author.mention+" You didn't ask me to add anyone! Make sure you @ the person you want to invite: for example - /invite "+self.user.mention +" - You can also @ multiple people at once!")
            return
        good_list = []
        refused_list = []
        for member in message.mentions:
            if(member in good_list or member in refused_list):
                continue
            user_roles = member.roles
            #                    Hacksu                                                 Bot                                                    Sponsor                                             Judge                                                  Mentor                                                  
            if(self.khe.get_role(755076104590589952) in user_roles or self.khe.get_role(760676726392750080) in user_roles or self.khe.get_role(755077276575465582) in user_roles or self.khe.get_role(755597298431688805) in user_roles or self.khe.get_role(755597271600463942) in user_roles):
                refused_list.append(member)
                print(str(member) + " is a staff member")            
                continue
            for channel in teams_cat.text_channels:
                if(channel.overwrites_for(member).view_channel):
                    refused_list.append(member)
                    print(str(member) + " is already in a team")
                    break
            if(member in refused_list):
                continue
            good_list.append(member)

        check_list = []
        msg_list = []
        
        for person in good_list:
            try:
                check_list.append(person.id)
                msg = await person.send("Hello! You have been invited to join a team by "+str(message.author)+"! React with ✅ to accept the request, and 🛑 to reject (This invite will expire after 10 minutes).")
                msg_list.append(msg.id)
                await msg.add_reaction("✅")
                await msg.add_reaction("🛑")
            except Exception as e:
                print("Sending DM Error:",e)
                refused_list.append(person)
        await message.channel.send(message.author.mention + ("" if len(good_list) == 0 else " Your invite(s) have been sent out!") + ("" if len(refused_list) == 0 else " I couldn't invite all of the people you invited, either because they are already in a group, they had DMs turned off or because they are a staff member."))

        def check(reaction, user):
            if(user.id in check_list):
                if(type(reaction.emoji) == str and reaction.message.id in msg_list):
                    if(reaction.emoji == "✅"):
                        check_list.remove(user.id)
                        over = team_channel.overwrites
                        over[user] = discord.PermissionOverwrite(view_channel=True,send_messages=True,manage_messages=True) # Joiner
                        asyncio.get_event_loop().create_task(team_channel.edit(overwrites = over))
                        name = " ".join(team_channel.name.split("-")[0:2]).capitalize()
                        for channel in teams_cat.voice_channels:
                            if(channel.name.startswith(name)):
                                over = channel.overwrites
                                over[user] = discord.PermissionOverwrite(view_channel=True)
                                asyncio.get_event_loop().create_task(channel.edit(overwrites = over))
                                break
                        asyncio.get_event_loop().create_task(user.send("Success! You are now added to the team!"))
                    elif(reaction.emoji == "🛑"):
                        asyncio.get_event_loop().create_task(user.send("Gotcha, invitation ignored!"))
                if(len(check_list) == 0):
                    return True
            return False
        try:
            await self.wait_for("reaction_add", check=check, timeout=600)
        except asyncio.TimeoutError:
            pass

        print("DONE")

    async def leave(self,message):
        teams_cat = self.get_channel(763785871278211082)
        react_msg = await message.channel.send(message.author.mention + " Are you sure you want to leave this group? React with ✅ to confirm, and 🛑 to cancel. This wil expire in 1 minute.")
        await react_msg.add_reaction("✅")
        await react_msg.add_reaction("🛑")
        def check(reaction, user):
            print("?")
            print(user.id,message.author.id)
            if(type(reaction.emoji) == str and reaction.message.id == react_msg.id and user.id == message.author.id):
                print(1)
                if(reaction.emoji == "✅"):
                    over = message.channel.overwrites
                    del over[message.author]
                    asyncio.get_event_loop().create_task(message.channel.edit(overwrites = over))
                    name = " ".join(message.channel.name.split("-")[0:2]).capitalize()
                    for channel in teams_cat.voice_channels:
                        if(channel.name.startswith(name)):
                            over = channel.overwrites
                            del over[message.author]
                            asyncio.get_event_loop().create_task(channel.edit(overwrites = over))
                        return True
                elif(reaction.emoji == "🛑"):
                    asyncio.get_event_loop().create_task(message.channel.send("Cancelled"))
                    return True
            return False
        try:
            await self.wait_for("reaction_add",check=check,timeout=60)
        except asyncio.TimeoutError:
            return
        print("Done")

    async def on_ready(self): #This command will be called whenever the bot is first created and is ready to recieve input. This is different from being connected to Discord's servers.
        self.khe = self.get_guild(755074904155488296)

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
