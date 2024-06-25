

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
from Table import Table, Row

def isDebugEnvironment():
    envString = getenv('DEBUG', '')
    return (envString == '1' or envString.lower() == 'true')

# Some globals that *could* change time to time
load_dotenv()
discord.utils.setup_logging()
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

def getItemFromTable(table: Table, predetermined_item: str = ''):
    if predetermined_item == '':
        return random.choice(table)
    
    return table.find(predetermined_item)

@bot.tree.command(
    name='newgame',
    description='Randomly chooses a map, gamemode, and difficulty to play.'
)
async def newgame(interaction: discord.Integration):
    map = getItemFromTable(db.ListMaps())
    gamemode = getItemFromTable(db.ListGamemodes())
    difficulty = getItemFromTable(db.ListDifficulties())

    await interaction.response.send_message(f'```Map:\t\t {map}\nGamemode:\t\t {gamemode}\nDifficulty:\t\t {difficulty}```')

@bot.tree.command(
    name='spin',
    description='Randomly chooses a trait and compatible map for the specified gamemode.'
)
async def spin(interaction: discord.Integration, requested_mode: str):
    trait = getItemFromTable(db.FetchTraitsForGamemode(gamemodeName=requested_mode))
    item = getItemFromTable(db.FetchItemsForTrait(traitName=trait))

    await interaction.response.send_message(f'```Trait:\t\t {trait}\nItem:\t\t {item}```')

@bot.tree.command(
    name='item',
    description='Randomly chooses an item to be used with the specified trait.'
)
async def item(interaction: discord.Integration, requested_trait: str):
    item = getItemFromTable(db.FetchItemsForTrait(traitName=requested_trait))
    await interaction.response.send_message('```' + item + '```')

@bot.tree.command(
    name='trait',
    description='Randomly chooses and prints a trait to play with the specified gamemode.',
)
async def trait(interaction: discord.Integration, requested_mode: str):
    traits = db.FetchTraitsForGamemode(gamemodeName=requested_mode)
    logging.info(f'command.name=trait: Fetching traits for gamemode {requested_mode}.')

    trait = getItemFromTable(traits)
    logging.info(f'command.name=trait: Randomly selected trait: {trait}')

    await interaction.response.send_message('```' + '\n'.join([str(i).replace(r'\n', '\n') for i in trait.values()]) +'```')

@bot.tree.command(
    name='difficulty',
    description='Randomly chooses and prints a difficulty to play.'
)
async def diff(interaction: discord.Integration):
    result = getItemFromTable(db.ListDifficulties())
    await interaction.response.send_message('```' + result[db.NAME_KEY] + '```')

@bot.tree.command(
    name='mode',
    description='Randomly chooses and prints a gamemode to play.'
)
async def mode(interaction: discord.Integration):
    gamemode = getItemFromTable(db.ListGamemodes())
    await interaction.response.send_message('```' + gamemode[db.NAME_KEY] + '```')

@bot.tree.command(
    name='rules',
    description='Prints the rules of the specified gamemode.'
)
async def rules(interaction: discord.Integration, requested_name: str):
    gamemode = db.FetchGameModeByName(gamemodeName=requested_name)
    logging.info(f'command.name=rules: fetching gamemode by user input: {requested_name}. Results: {gamemode}')

    await interaction.response.send_message('```' + gamemode[db.NAME_KEY] + ' Rules:\n' + gamemode[db.DESCRIPTION_KEY] + '```')

# region: Election!

electionGroup = app_commands.Group(
    name='election',
    description='Manage elections.'
)
@electionGroup.command(
    name='start',
    description='Starts an election with the specified parameters.'
)
async def startElection(interaction: discord.Interaction, votes: int, purpose: str):
    electionID = db.CreateElection(interaction.guild.id, votes, DEBUG, purpose)[0]['@ElectionID']
    await interaction.response.send_message(f'Election has begun. Election ID: {electionID}.')

@electionGroup.command(
    name='end',
    description='Ends the election with the specified ID.'
)
async def endElection(interaction: discord.Interaction, id: int):
    await interaction.response.send_message('```Ending election...```')

# endregion: Election!

# region: Give

giveGroup = app_commands.Group(
    name='give',
    description='Retrieves the specified data from the specified category'
)
@giveGroup.command(
    name='trait',
    description='Retrieves the specified trait from the specified category.'
)
async def giveTrait(interaction: discord.Interaction, trait_name: str):
    trait = getItemFromTable(db.ListTraits(), trait_name)
    await interaction.response.send_message('```' + trait + '```')

@giveGroup.command(
    name='difficulty',
    description='Retrieves the specified difficulty from the specified category.'
)
async def giveDifficulty(interaction: discord.Interaction, difficulty_name: str):
    difficulty = getItemFromTable(db.ListDifficulties(), difficulty_name)
    await interaction.response.send_message('```' + difficulty + '```')

@giveGroup.command(
    name='item',
    description='Retrieves the specified item from the specified category.'
)
async def giveItem(interaction: discord.Interaction, item_name: str):
    item = getItemFromTable(db.ListItems(), item_name)
    await interaction.response.send_message('```' + item + '```')

@giveGroup.command(
    name='gamemode',
    description='Retrieves the specified gamemode from the specified category.'
)
async def giveGamemode(interaction: discord.Interaction, gamemode_name: str):
    gamemode = getItemFromTable(db.ListGamemodes(), gamemode_name)
    await interaction.response.send_message('```' + gamemode + '```')

# endregion: Give

@bot.event
async def on_ready():
    bot.tree.add_command(electionGroup)
    bot.tree.add_command(giveGroup)
    #bot.tree.copy_global_to()
    #bot.tree.clear_commands(guild=None)
    print(await bot.tree.sync())
    print(f'Logged in as {bot.user} with id {bot.user.id}')

bot.run(TOKEN)