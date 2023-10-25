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

# Defining cog class.
class Loc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def loc(self, ctx, input_value):
        try:
            # Check if the user's ID is in the list of allowed user IDs
            if str(ctx.author.id) not in allowed_user_ids:
                embed = discord.Embed(title="Permission Denied", description="You do not have permission to use this command.", color=0xff0000)
                await ctx.send(embed=embed)
                return

            # Confirm with the user before proceeding
            confirmation_embed = discord.Embed(title="Confirmation", description=f"Are you sure you want to search for information on {input_value}?", color=0x00ff00)
            await ctx.send(embed=confirmation_embed)

            def check(msg):
                return msg.author == ctx.author and msg.content.lower() == 'yes'

            try:
                # Wait for the user's confirmation
                await self.bot.wait_for('message', check=check, timeout=30)
            except asyncio.TimeoutError:
                timeout_embed = discord.Embed(title="Command Timed Out", description="Please try again if you want to search.", color=0xff0000)
                await ctx.send(embed=timeout_embed)

            # Function to get IP address from a domain name
            def get_ip_address(domain):
                try:
                    ip_address = socket.gethostbyname(domain)
                    return ip_address
                except socket.gaierror:
                    return None

            # Function to check if the input is an IP address
            def is_ip_address(input_value):
                ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
                return bool(ip_pattern.match(input_value))

            # Check if the input is an IP address or a domain name
            if is_ip_address(input_value):
                ip_address = input_value
            else:
                # Resolve domain name to IP address
                ip_address = get_ip_address(input_value)
                if ip_address is None:
                    resolution_failed_embed = discord.Embed(title="Domain Resolution Failed", description=f"Failed to resolve domain '{input_value}' to an IP address.", color=0xff0000)
                    await ctx.send(embed=resolution_failed_embed)
                    return

            # Send a request to ip-api.com with the specified fields
            response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=66846719")
            data = response.json()

            # Check if the response status is 'success'
            if data["status"] == "success":
                # Create a Discord embed for the location information with the title as the input_value
                location_embed = discord.Embed(title=input_value, color=0x00ff00)
                location_embed.add_field(name="IP/Website", value=data.get("query", "N/A"), inline=False)
                location_embed.add_field(name="Status", value=data.get("status", "N/A"))
                location_embed.add_field(name="Continent", value=data.get("continent", "N/A"))
                location_embed.add_field(name="Continent Code", value=data.get("continentCode", "N/A"))
                location_embed.add_field(name="Country", value=data.get("country", "N/A"))
                location_embed.add_field(name="Country Code", value=data.get("countryCode", "N/A"))
                location_embed.add_field(name="Region", value=data.get("region", "N/A"))
                location_embed.add_field(name="Region Name", value=data.get("regionName", "N/A"))
                location_embed.add_field(name="City", value=data.get("city", "N/A"))
                location_embed.add_field(name="District", value=data.get("district", "N/A"))
                location_embed.add_field(name="Zip Code", value=data.get("zip", "N/A"))
                location_embed.add_field(name="Latitude", value=data.get("lat", "N/A"))
                location_embed.add_field(name="Longitude", value=data.get("lon", "N/A"))
                location_embed.add_field(name="Timezone", value=data.get("timezone", "N/A"))
                location_embed.add_field(name="Offset", value=data.get("offset", "N/A"))
                location_embed.add_field(name="Currency", value=data.get("currency", "N/A"))
                location_embed.add_field(name="ISP", value=data.get("isp", "N/A"))
                location_embed.add_field(name="Organization", value=data.get("org", "N/A"))
                location_embed.add_field(name="AS Number", value=data.get("as", "N/A"))
                location_embed.add_field(name="AS Name", value=data.get("asname", "N/A"))
                location_embed.add_field(name="Is Mobile", value=data.get("mobile", "N/A"))
                location_embed.add_field(name="Is Proxy", value=data.get("proxy", "N/A"))
                location_embed.add_field(name="Is Hosting", value=data.get("hosting", "N/A"))

                # Send the embed as the location information
                await ctx.send(embed=location_embed)
            else:
                retrieval_failed_embed = discord.Embed(title="Location Information Retrieval Failed", description="An error occurred while retrieving location information.", color=0xff0000)
                await ctx.send(embed=retrieval_failed_embed)

        except Exception as e:
            error_embed_loc = discord.Embed(title="An error occurred", description=str(e), color=0xff0000)
            await ctx.send(embed=error_embed_loc)

# Cog defining the command to main.py.
async def setup(bot: commands.Bot):
    await bot.add_cog(Loc(bot))
