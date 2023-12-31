from authtoken import *
import discord
import logging
import feedparser



intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Displays a ready message when bot begins to run
@client.event
async def on_ready():
    print(f'{client.user} has begun operation')
    print('------')

# Creates a response message to specific commands
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    match message.content:
        case '/help':
            await message.channel.send('Hello ' + f'{message.author}, please consult the following for basic commands:')
        # Handles posting articles
        case '/article':
            # RSS provided by CNN
            rss = 'http://rss.cnn.com/rss/cnn_latest.rss'
            feed = feedparser.parse(rss)

            # Obtains the most recent entry
            latest = feed.entries[0]
            title = latest.title
            link = latest.link

            # Displays the most recent news article w/ the title and the link
            await message.channel.send(f"Latest news: {title}\nRead more: {link}")

# Creates a log based on previous actions performed by the bot
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
client.run(token, log_handler=handler)
