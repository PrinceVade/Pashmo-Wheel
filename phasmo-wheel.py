

# Discord.py imports
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Bot, CommandNotFound, when_mentioned_or

# Python libraries
import logging
import random
from os import listdir, getenv
from dotenv import load_dotenv
from Levenshtein import distance
from datetime import datetime as dt

# Local imports
import databaseAPI as db

def isDebugEnvironment():
    envString = getenv('DEBUG', '')
    return (envString == '1' or envString.lower() == 'true')

# Some globals that change time to time
load_dotenv()
DEBUG = isDebugEnvironment()
TOKEN = getenv('BOT_TOKEN')
description = '''I am the Phasmo-Bot! Designed to make Phasmophobia a more terrible and amazing experience!

To use, you should have a channel dedicated to Phasmophobia where everyone playing can see messages.
There, use the !newgame command in order to print a random map, gamemode, and difficulty.
If you are unfamiliar with the gamemode presented, use the "!rules <gamemode>" commands to print the rules.
Follow the instructions and have fun. Good luck!'''

# Discord objects that probably never change
intents = discord.Intents.default()
bot = commands.Bot(command_prefix=when_mentioned_or('/'), description=description, intents=intents)

@bot.tree.command(
    name='trait',
    description='Randomly chooses and prints a trait to play with the specified gamemode.',
)
async def trait(interaction: discord.Integration, requested_mode: str):
    traits = db.FetchTraitsForGamemode(gamemodeName=requested_mode)
    logging.info(f'command.name=trait: Fetching traits for gamemode {requested_mode}.')

    trait = random.choice(traits)
    logging.info(f'command.name=trait: Randomly selected trait: {trait}')

    await interaction.response.send_message('```' + trait[db.TRAIT_NAME_KEY] + '\n\n' + trait[db.TRAIT_DESCRIPTION_KEY] +'```')

@bot.tree.command(
    name='mode',
    description='Randomly chooses and prints a gamemode to play.'
)
async def mode(interaction: discord.Integration):
    gamemodes = db.ListGamemodes()
    logging.info(f'command.name=mode: Fetching gamemodes.')

    gamemode = random.choice(gamemodes)
    logging.info(f'command.name=mode: Randomly selected gamemode: {gamemode}')

    await interaction.response.send_message('```' + gamemode[db.GAMEMODE_NAME_KEY] + '```')

@bot.tree.command(
    name='rules',
    description='Prints the rules of the specified gamemode.',
)
async def rules(interaction: discord.Integration, requested_name: str):
    gamemode = db.FetchGameModeByName(gamemodeName=requested_name)
    logging.info(f'command.name=rules: fetching gamemode by user input: {requested_name}. Results: {gamemode}')

    await interaction.response.send_message('```' + gamemode[db.GAMEMODE_NAME_KEY] + ' Rules:\n' + gamemode[db.GAMEMODE_DESCRIPTION_KEY] + '```')

@bot.event
async def on_ready():
    bot.tree.copy_global_to(guild=discord.Object(id=445050849387872267))
    print(await bot.tree.sync(guild=discord.Object(id=445050849387872267)))
    print(f'Logged in as {bot.user} with id {bot.user.id}')

bot.run(TOKEN)