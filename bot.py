import nextcord

from authtoken import *
from NewsRSS import *

import nextcord as discord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption

import logging
import feedparser
import random
from random import randint



intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)

# Displays a ready message when bot begins to run
@client.event
async def on_ready():
    print(f'{client.user} has begun operation')
    print('------')

# Creates a slash command to give a list of commands
@client.slash_command(name="help", description="Receive a list of commands available")
async def helper(interaction: Interaction):
    await interaction.response.send_message('Hello ' + f'{interaction.user.display_name}, please consult the following for basic commands:')

# Creates a slash command to choose between different news outlets
@client.slash_command(name="article", description="Chose a news outlet to receive the latest article")
async def article(interaction: Interaction,
                  outlet: str = SlashOption(
                      name="outlet",
                      description="Enter the news outlet",
                      required=True)):
    # RSS provided by choice
    try:
        outlet = outlet.lower()
        feed = feedparser.parse(rss[outlet])
    except:
        print("That is not a valid news outlet.")

    # Obtains the most recent entry
    latest = feed.entries[0]
    title = latest.title
    link = latest.link

    # Displays the most recent news article w/ the title and the link
    await interaction.response.send_message(f"Latest news: {title}\nRead more: {link}")

# Creates a slash command to generate random articles
@client.slash_command(name="randomarticle", description="Chooses a random news article")
async def random_article(interaction: nextcord.Interaction):
    # Randomly selected outlet
    outlet = random.choice(list(rss.keys()))
    feed = feedparser.parse(rss[outlet])

    # Randomly selects an article between the most recent article up to the 20th
    latest = feed.entries[randint(0, 50)]
    title = latest.title
    link = latest.link

    # Displays the most recent news article w/ the title and the link
    await interaction.response.send_message(f"Latest news: {title}\nRead more: {link}")



# Creates a log based on previous actions performed by the bot
logger = logging.getLogger('nextcord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client.run(token)
