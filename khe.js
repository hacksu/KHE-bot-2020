const Discord = require('discord.js');
const client = new Discord.Client();
const { token } = require("./config.json");

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});


/* if (msg.content == "/stuff") {
    msg.reply("you asked me to do stuff, here's a math problem: 2 + 2 = 4")
  }
*/

client.on('message', msg => {
  if (msg.content === 'ping') {
    msg.reply('pong');
  }
});

client.login(token);