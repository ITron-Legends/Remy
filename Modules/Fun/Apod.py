import os
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('NASA_API_KEY')

class APOD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Define a command to get the APOD
    @commands.hybrid_command(name="apod", description="Astronomy Picture of the Day")
    async def get_apod(self, ctx: commands.Context):
        # Make a GET request to the NASA APOD API
        url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            title = data['title']
            image_url = data['url']
            explanation = data['explanation']

            # Create and send an embed with the APOD data
            embed = discord.Embed(title=title, description=explanation, color=0x00ff00)
            embed.set_image(url=image_url)
            embed.set_footer(text="Astronomy Picture of the Day")
            await ctx.send(embed=embed)
        else:
            await ctx.send('Failed to fetch APOD. Please try again later.')

# Cog defining the command to main.py.
async def setup(bot: commands.Bot):
    await bot.add_cog(APOD(bot))