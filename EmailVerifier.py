import discord
import asyncio
from datetime import *
import requests

file = open("data/emails.txt",'r')
EMAILS = eval("{"+file.read()+"}")
file.close()


class MyClient(discord.Client):

    
    #ON MESSAGE
    async def on_message(self,message):
        global EMAILS
        if(message.channel.id == 751154150871531701):
            if(message.content == "/verify"):
                if(message.guild.get_role(751154695602569317) in message.author.roles):
                    await message.delete(delay=1.0)
                    return
                try:
                    await message.author.send("Welcome to Kent Hack Enogugh 2020!")
                    await message.delete(delay=1)
                except discord.errors.Forbidden:
                    await message.channel.send("I can't DM you "+message.author.mention+"! Please make sure you have enabled DM's from this server.",delete_after=10)
                    await message.delete(delay=1)
                    return
                await message.author.send("In order to gain access to the server, you must provide the email that you registered to the event with. By verifying your email to gain access, you also agree to the Terms and Conditions of KHE, and that you have read and understand them.\n\nTo verify, please respond with the email that you used to register for the event (A timeout of 1 minute is put place).")

                def check(msg):
                    return type(msg.channel) == discord.DMChannel and msg.author == message.author
                try:
                    msg = await self.wait_for('message',check=check,timeout=60.0)
                except asyncio.TimeoutError:
                    await message.author.send("Sorry, you took too long! To try again, return to the KHE Discord and type `/verify`.")
                    return

                verify = requests.get("https://api.khe.io/v1.0/verify/email/"+msg.content.replace("/","")).json()
                if(verify['email'] in EMAILS):
                    await message.author.send("We're sorry, that email has already been used to join the Server. If you believe this is a mistake, please contact KHE Staff.")
                elif(verify['valid']):
                    await message.author.send("Success! Welcome to KHE 2020!")
                    await message.author.add_roles(message.guild.get_role(751154695602569317),atomic=True)
                    EMAILS[verify['email']] = message.author.id
                    file = open("data/emails.txt",'a')
                    file.write("'"+verify['email']+"':"+str(message.author.id)+",\n")
                    file.close()
                else:
                    await message.author.send("Apologies, but we do not have that email in our system. If you entered the email in wrong, please return to the KHE Discord and use `/verify` again. If you believe I have made a mistake, please contact KHE Staff.")
            elif(message.author.id != 737741291944673402):
                await message.delete(delay=1.0)
            
    #ON MEMBER JOIN
    #async def on_member_join(self,member):
    #    try:
    #        await member.send("Test")

    #ON REACTION ADD
    #async 


    #PROCESS COMMANDS
    async def process_commands(self,message):
        command = message.content.split()[0].lower()
        #Command List Here


    #WHEN READY
    async def on_ready(self):
        pass
                
            


    #CONNECTION
    async def on_connect(self):
        print("Bot has connected to server at time:",datetime.now())
    
    #DISCONNECTION
    async def on_disconnect(self):
        print("Bot has disconnected from server at time:",datetime.now())



print("Starting KHE Verification")
bot = MyClient()
file = open("config.json",'r')
TOKEN = eval(file.read())["token"]
#print(TOKEN)
bot.run(TOKEN)
