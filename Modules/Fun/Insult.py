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

api_url_insult = "https://evilinsult.com/generate_insult.php?lang=en&type=json"

# Defining cog class.
class Insult(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="insult", description="Insults a user.") # Indent the command inside the class.
    async def insult(self, ctx: commands.Context, user: discord.Member):
        """Insults a user
        
        Parameters
        ----------------------
        user: discord.Member
             Select a User to Insult.
             
        """
        # Make a request to the API
        response = requests.get(api_url_insult)
        if response.status_code == 200:
            insult_data = json.loads(response.text)
            insult = insult_data['insult']

            # Send the insult without an embed
            await ctx.send(f"{user.mention}, {insult}")
        else:
            # Create an error embed
            error_embed = discord.Embed(title="Error", description="Failed to fetch an insult. Please try again later.", color=0xff0000)

            # Send the error embed as a response
            await ctx.send(embed=error_embed)

# Cog defining the command to main.py.
async def setup(bot: commands.Bot):
    await bot.add_cog(Insult(bot))