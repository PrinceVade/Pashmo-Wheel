

# Discord.py imports
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import CommandNotFound

# Python libraries
import logging
import random
from os import listdir, getenv
from dotenv import load_dotenv
from Levenshtein import distance
from datetime import datetime as dt

# Local imports
import constants
import databaseAPI as db

def isDebugEnvironment():
    envString = getenv('DEBUG', '')

    return (envString == '1' or envString.lower() == 'true')

# Some globals that change time to time
DEBUG = isDebugEnvironment()
TOKEN = getenv('BOT_TOKEN')
description = '''I am the Phasmo-Bot! Designed to make Phasmophobia a more terrible and amazing experience!

To use, you should have a channel dedicated to Phasmophobia where everyone playing can see messages.
There, use the !newgame command in order to print a random map, gamemode, and difficulty.
If you are unfamiliar with the gamemode presented, use the "!rules <gamemode>" commands to print the rules.
Follow the instructions and have fun. Good luck!'''


# Discord objects that probably never change
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(
    name='rules',
    description='Prints the rules of the specified gamemode.',
)
async def rules(interaction: discord.Integration, gamemode: str):
    gamemode = db.FetchGamemode()
    logging.info(f'Fetching rules for gamemode: {gamemode}')

    interaction.response.send_message('```' + gamemode[constants.DB_NAME_KEY] + ' Rules:\n' + gamemode[constants.DB_DESCRIPTIONS_KEY] + '```')