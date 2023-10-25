import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

allowed_user_ids = os.getenv('ALLOWED_USER_IDS').split(',')

class AllowedUsers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def al(self, ctx):
        # Check if the user who invoked the command is in the allowed user IDs list
        if str(ctx.author.id) not in allowed_user_ids:
            await ctx.send(embed=discord.Embed(title="Permission Denied", description="You do not have permission to use this command.", color=0xff0000))
            return
        # Create an embed
        embed = discord.Embed(title="Allowed Users")
        
        for user_id in allowed_user_ids:
            try:
                # Fetch user information using the Discord API
                user = await self.bot.fetch_user(int(user_id))
                if user:
                    embed.add_field(name=user.name, value=f"User ID: {user.id}", inline=False)
            except discord.NotFound:
                # Handle the case where a user ID is invalid or not found
                pass
        
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
  await  bot.add_cog(AllowedUsers(bot))
