import os 
import requests
from datetime import datetime
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import time
import random 
import json
import re
import aiohttp
import socket
from dotenv import load_dotenv

load_dotenv()

# Create a default set of intents
intents = discord.Intents.all()

discordtoken = os.getenv('DISCO_TOKEN')
app_id = os.getenv('APPLICATONID')
# Create a default set of intents
intents = discord.Intents.all()

bot = commands.Bot(application_id=app_id, intents = intents, command_prefix="!")

# Remove the default help command
bot.remove_command('help')

# See if its logged in.
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Your Mom. Do /help to see all commands."))
    await bot.tree.sync()
    print('__________________________________________')
    print('Initializing ITron space!')
    await asyncio.sleep(2)  
    print('Connected to Space node 1')
    await asyncio.sleep(2)  
    print(f'Connected to Space as {bot.user.name}')
    print('__________________________________________')

async def load_extensions():
    # Get the list of subdirectories in ./cogs
    subdirs = [d for d in os.listdir("./cogs") if os.path.isdir(os.path.join("./cogs", d))]
    # Print the header
    print("Cogs")
    # Loop over each subdirectory
    for subdir in subdirs:
        # Print the subdirectory name with indentation
        print(f"   |")
        print(f"   ├─── {subdir}")
        # Get the list of files in the subdirectory
        files = os.listdir(os.path.join("./cogs", subdir))
        # Loop over each file
        for filename in files:
            # Check if the file is a python file
            if filename.endswith(".py"):
                # Print the filename with indentation and a line break
                print(f"   |      |")
                print(f"   |      └─── {filename}\n")
                # Load the cog using the subdirectory and filename
                await bot.load_extension(f"cogs.{subdir}.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(discordtoken)

# runnning main first.
if __name__ == "__main__":
    asyncio.run(main())