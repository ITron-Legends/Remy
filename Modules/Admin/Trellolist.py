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

allowed_user_ids = os.getenv('ALLOWED_USER_IDS').split(',')

# Define your Trello API key and token
api_key = os.getenv('TRELLO_API_KEY')
api_token = os.getenv('TRELLO_API_TOKEN')

# Define your Trello list ID
list_id = os.getenv('TRELLO_LIST_ID')

# Define the URL for getting all the cards in a list
urltrlist = f"https://api.trello.com/1/lists/{list_id}/cards"

# Defining cog class.
class TrList(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    # trlist command 

    # Number of cards to display per page
    cards_per_page = 15

    # Define a command called trlist
    @commands.command()
    async def trlist(self, ctx, page_or_recent="1"):
        if str(ctx.author.id) not in allowed_user_ids:
            await ctx.send(embed=discord.Embed(title="Permission Denied", description="You do not have permission to use this command.", color=0xff0000))
            return

        # Define the query parameters for authentication
        params = {"key": api_key, "token": api_token}

        # Make a GET request to the URL with the query parameters
        response = requests.get(urltrlist, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response as JSON
            data = response.json()

            # Check if there are any cards in the list
            if not data:
                await ctx.send("There are no cards in the Trello list.")
                return

            # Check if the user requested the "recent" option
            if page_or_recent.lower() == "recent":
                # Show the last 5 added cards
                data = data[-5:]  # Get the last 5 cards

            else:
                # Calculate the start and end indices based on the page number
                if page_or_recent.isdigit():
                    page_number = int(page_or_recent)
                    start_index = (page_number - 1) * TrList.cards_per_page
                    end_index = start_index + TrList.cards_per_page
                    data = data[start_index:end_index]
                else:
                    await ctx.send("Invalid page number. Please use a valid page number or 'recent'.")

            # Create an embed for the selected cards with the page number information
            embed = discord.Embed(
                title=f"Trello Reports", color=0x00ff00
            )

            for card in data:
                embed.add_field(name=card["name"], value=card["desc"] or "No description", inline=False)

            # Add the footer
            embed.set_footer(text="To be used with the !rep command after making a ticket.")

            await ctx.send(embed=embed)

        else:
            await ctx.send(f"Request failed with status code {response.status_code}: {response.text}")

# Cog defining the command to main.py.
async def setup(bot: commands.Bot):
    await bot.add_cog(TrList(bot))