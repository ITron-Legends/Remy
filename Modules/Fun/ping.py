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
class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", description="Pong")
    async def ping(self, ctx: commands.Context):
        latency = round(self.bot.latency * 1000)  # Calculate the latency in milliseconds
        embed = discord.Embed(title="Ping", description=f"Pong! Latency: `{latency}ms`", color=0x00ff00)
        await ctx.send(embed=embed)
    
# Cog defining the command to main.py. 
async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))
