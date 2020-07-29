require('./khe.js') // FOR TESTING
let Discord = require('discord.js');
let client = global.client;

client.on('message', (msg) => {
  if (msg.author.id != client.user.id) {
    msg.reply('moderation: ' + msg.content);
  }
});
