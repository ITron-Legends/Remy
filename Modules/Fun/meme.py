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
class Meme(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.hybrid_command(name="meme", description="Random meme")
    async def meme(self, ctx: commands.Context):
        try:
            response = requests.get('https://meme-api.com/gimme')
            meme_data = response.json()

            meme_embed = discord.Embed(
                title='Random Meme',
                color=discord.Color.orange()
            )
            meme_embed.set_image(url=meme_data['url'])

            await ctx.send(embed=meme_embed)
            
            # Like here as an example?  await ctx.send(embed=meme_embed , ephemeral=True)

        except Exception as e:
            print(e)
            await ctx.send('Sorry, I cannot fetch a meme right now.')
        
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Meme(bot))
