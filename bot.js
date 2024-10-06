const Discord = require('discord.js');
const { Intents } = require('discord.js');
const dotenv = require('dotenv');
const CalendarAssistant = require('./calendar_assistant');

dotenv.config();

const client = new Discord.Client({
  intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES]
});

const calendarAssistant = new CalendarAssistant();

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

client.on('messageCreate', async (message) => {
  if (message.content.startsWith('!calendar')) {
    const query = message.content.slice('!calendar'.length).trim();
    try {
      const response = await calendarAssistant.processQuery(query);
      message.channel.send(response);
    } catch (error) {
      console.error('Error processing calendar query:', error);
      message.channel.send('An error occurred while processing your request.');
    }
  }
});

client.login(process.env.DISCORD_TOKEN);