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
import aiohttp
from dateutil import parser
from dotenv import load_dotenv

load_dotenv()

allowed_user_ids = os.getenv('ALLOWED_USER_IDS').split(',')


class Find(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Define a function to find the Roblox ID from the username
    def find_roblox_id(self, username):
        api_url = f"https://users.roblox.com/v1/usernames/users"
        params = {"usernames": [username], "excludeBannedUsers": False}
        response = requests.post(api_url, json=params)
        data = response.json()
        if data["data"]:
            roblox_id = data["data"][0]["id"]
            return roblox_id
        else:
            return None

    def format_iso8601_to_datetime(self, iso8601_timestamp):
        # Try to parse the ISO 8601 timestamp using dateutil.parser
        try:
            dt = parser.isoparse(iso8601_timestamp)
        except ValueError:
            formatted_datetime = "Invalid Timestamp"
        else:
            # Format the datetime as a readable string
            formatted_datetime = dt.strftime("%B %d, %Y %I:%M %p")
        return formatted_datetime

    @commands.command(name="find")
    async def find_roblox_user(self, ctx, query: str):
        if str(ctx.author.id) not in allowed_user_ids:
            await ctx.send(embed=discord.Embed(title="Permission Denied", description="You do not have permission to use this command.", color=0xff0000))
            return
        if query.isdigit():  # Check if the query is a numeric ID
            user_id = query
        else:
            user_id = self.find_roblox_id(query)

        if user_id is None:
            await ctx.send(f"Error: Could not find a Roblox user with the username or ID '{query}'")
            return

        response = requests.get(f"https://users.roblox.com/v1/users/{user_id}")

        if response.status_code == 200:
            data = response.json()
            display_name = data.get("displayName")
            title = display_name if display_name else data["name"]
            username = data["name"]
            user_id = data["id"]
            created_time_iso8601 = data["created"]
            created_time = self.format_iso8601_to_datetime(created_time_iso8601)
            bio = data.get("description", "N/A")  
            if not bio or not bio.strip():  # Check if bio is empty or only contains whitespace
                   bio = "The user does not have a bio"
            ban_status = "Banned" if data.get("isBanned") else "Not Banned"

            title = f"~~{title}~~" if data.get("isBanned") else title

            created_time_code_block = f"{created_time}"
            bio_code = f"```{bio}```"
            ban_status_code = f"```{ban_status}```"
            
            thumbnail_url = None
            attempts = 0
            while attempts < 10:
                thumbnail_response = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=150x150&format=jpeg&isCircular=false")

                if thumbnail_response.status_code == 200:
                    thumbnail_data = thumbnail_response.json()
                    if "data" in thumbnail_data and thumbnail_data["data"]:
                        target_data = thumbnail_data["data"][0]
                        if target_data["state"] == "Completed":
                            thumbnail_url = target_data["imageUrl"]
                            break
                        elif target_data["state"] == "Pending":
                            time.sleep(5)
                    else:
                        break
                else:
                    break
                attempts += 1

            embed = discord.Embed(title=title, color=discord.Color.blue(), url=f"https://www.roblox.com/users/{user_id}/profile")
            embed.add_field(name="Username", value=username)
            embed.add_field(name="Account created time", value=created_time_code_block)
            embed.add_field(name="ID", value=user_id)
            embed.add_field(name="Bio", value=bio_code)
            embed.add_field(name="Ban status", value=ban_status_code)

            if thumbnail_url:
                embed.set_thumbnail(url=thumbnail_url)
            else:
                embed.set_footer(text="Image API has issues.")

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Error: Could not find Roblox user with username or ID '{query}'")

async def setup(bot: commands.Bot):
  await  bot.add_cog(Find(bot))