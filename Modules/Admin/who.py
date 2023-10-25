import requests
from datetime import datetime
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import time
import random 
import json

# Defining cog class.
class Who(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.command()
    async def who(self, ctx, user_info):
        # Check if the input is a mention (e.g., @username)
        if ctx.message.mentions:
            user_id = ctx.message.mentions[0].id
        else:
            # Try to parse the input as a user ID
            try:
                user_id = int(user_info)
            except ValueError:
                await ctx.send("Invalid user mention or ID.")
                return

        try:
            # Fetch user information using the bot's HTTP client
            user = await self.bot.fetch_user(user_id)

            embed = discord.Embed(title=f"Username: {user.name}", color=discord.Color.blue())
            embed.add_field(name="ID:", value=user.id, inline=False)
            embed.add_field(name="Account created at:", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
            
            # Format the profile picture link as bold text with a clickable link
            profile_picture_link = f"**[PROFILE PICTURE]({user.avatar.url})**"
            embed.add_field(name="Profile picture link:", value=profile_picture_link, inline=False)

            if ctx.guild:
                member = ctx.guild.get_member(user.id)
                if member:
                    embed.add_field(name="Display name:", value=member.display_name, inline=False)
                    embed.add_field(name="Joined this server at:", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
                    # Check if the user has Nitro for banner
                    if member.premium_since is not None:
                        embed.add_field(name="Banner link (Nitro only):", value=user.banner.url, inline=False)

            roles = [role.mention for role in member.roles if role != ctx.guild.default_role] if member else []
            roles = ", ".join(roles) or "None"
            embed.add_field(name="Roles:", value=roles, inline=False)

            # Set thumbnail for both cases
            embed.set_thumbnail(url=user.avatar.url)

            await ctx.send(embed=embed)
        except discord.NotFound:
            await ctx.send("User not found.")

# Cog defining the command to main.py.
async def setup(bot: commands.Bot):
    await bot.add_cog(Who(bot))