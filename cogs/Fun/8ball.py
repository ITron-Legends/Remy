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


# Defining cog class. 
class Ball(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Define the 8ball command
    @commands.hybrid_command(name="ball", description="Ask a question to the Magic 8Ball.")
    async def ball(self, ctx: commands.Context, *, question):
        """Ask a question to the Magic 8Ball.
        
        Parameters
        ---------------------
        question
                  Input the question
        """
        # Replace spaces in the question with '%20' for the URL
        formatted_question = question.replace(" ", "%20")

        # Construct the API URL with the formatted question
        api_url = f"https://www.eightballapi.com/api?question={formatted_question}&lucky=true"
        
        # Send a GET request to the API
        response = requests.get(api_url)
        
        if response.status_code == 200:
            ball_data = response.json()
            response_text = ball_data.get("reading", "Unable to get a response from the 8-ball.")

            # Create an embed for the 8-ball response
            embed = discord.Embed(title="Magic 8-Ball", description=response_text, color=0x00ff00)

            # Send the embed as a response
            await ctx.send(embed=embed)
        else:
            # Create an error embed
            error_embed = discord.Embed(title="Error", description="Oops! Something went wrong while consulting the 8-ball.", color=0xff0000)

            # Send the error embed as a response
            await ctx.send(embed=error_embed)
        
# Cog defining the command to main.py. 
async def setup(bot: commands.Bot):
    await bot.add_cog(Ball(bot))
