import discord
import asyncio

muteCommand = "/mute"
unMuteCommand = "/unmute"
authRoles = ["Organizer","Sponsor","Staff"]

def isAuth(roles):
    for role in roles:
        if str(role) in authRoles:
            return True
    return False

class MyClient(discord.Client):

    async def on_message(self, message):
        if(message.channel.id not in [763838177189560351,767930560433356800]):
            return
        command = message.content.split()
        if command[0] == muteCommand and isAuth(message.author.roles) and len(command) == 1:
            for member in message.author.voice.channel.members:
                if not member == message.author:
                    await member.edit(mute = True)
        elif command[0] == muteCommand and isAuth(message.author.roles) and len(command) >= 2:
            mentioned = message.mentions
            for member in message.author.voice.channel.members:
                if not member == message.author and member in mentioned:
                    await member.edit(mute = True)
        elif command[0] == unMuteCommand and isAuth(message.author.roles) and len(command) == 1: # Unmute everyone
            for member in message.author.voice.channel.members:
                await member.edit(mute = False)
        elif command[0] == unMuteCommand and isAuth(message.author.roles) and len(command) >= 2: # Unmute everyone
            mentioned = message.mentions
            for member in message.author.voice.channel.members:
                if member in mentioned:
                    await member.edit(mute = False)
            

bot = MyClient()
file = open("config.json",'r')
TOKEN = eval(file.read())["token"]
bot.run(TOKEN)
