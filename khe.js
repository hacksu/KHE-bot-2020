const Discord = require('discord.js');
const client = new Discord.Client();
const { token } = require("./config.json");
global.client = client;


client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});


/* if (msg.content == "/stuff") {
    msg.reply("you asked me to do stuff, here's a math problem: 2 + 2 = 4")
  }
*/
console.log("above client.on");

client.on('message', message => {
    command = message.content.split(" ")[0];
    console.log(command);
    if (command === '/ping') {
        message.reply('pong');
    }

    if (command === '/zone') {
      (async () => {
        let name = message.content.split(' ')[1];
        let category = await message.guild.channels.create(name, {
          type: 'category',
          permissionOverwrites: [{
            id: message.guild.id,
            deny: ['MANAGE_MESSAGES'],
            allow: ['SEND_MESSAGES'],
          }],
        });
        let textChannel = await message.guild.channels.create(name, { type: 'text', });
        let voiceChannel = await message.guild.channels.create(name, { type: 'voice', });
        await textChannel.setParent(category.id);
        await voiceChannel.setParent(category.id);
        message.reply('Channels Created');
      })();
    }

    if (command === '/help') {
      message.reply(`KHE Commands: 
                 /ping - bot responds with pong 
                 /zone - creates a category with a text and voice channel based on a given name`);
    }

  }


);

client.login(token);