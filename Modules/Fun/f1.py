import discord
from discord.ext import commands
import requests
import json

class F1Info(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="f1", description="Gets information about the latest race.")
    async def f1(self, ctx: commands.Context) -> None:
        response = requests.get('https://ergast.com/api/f1/current/last/results.json')
        data = response.json()

        # Extract race information
        race_name = data['MRData']['RaceTable']['Races'][0]['raceName']
        round = data['MRData']['RaceTable']['Races'][0]['round']
        date = data['MRData']['RaceTable']['Races'][0]['date']
        circuit = data['MRData']['RaceTable']['Races'][0]['Circuit']['circuitName']
        location = data['MRData']['RaceTable']['Races'][0]['Circuit']['Location']['locality']
        country = data['MRData']['RaceTable']['Races'][0]['Circuit']['Location']['country']

        # Create an embed object
        embed = discord.Embed(
            title=f"Last Formula 1 Race: {race_name}",
            color=discord.Color.red()
        )

        # Set thumbnail image in the top right corner
        thumbnail_url = "https://logosarchive.com/wp-content/uploads/2021/06/F1-icon-square.png"
        embed.set_thumbnail(url=thumbnail_url)

        # Add race information to the embed
        embed.add_field(name="Round", value=round, inline=True)
        embed.add_field(name="Date", value=date, inline=True)
        embed.add_field(name="Circuit", value=circuit, inline=True)
        embed.add_field(name="Location", value=f"{location}, {country}", inline=True)

        # Create a separate field for racer information
        results = data['MRData']['RaceTable']['Races'][0]['Results']
        for i, result in enumerate(results, start=1):
            position = result['position']
            laps = result['laps']
            racer_name = f"{result['Driver']['givenName']} {result['Driver']['familyName']}"
            constructor = result['Constructor']['name']
            status = result['status']
            wikipedia_url = result['Driver']['url']

            # Check if 'FastestLap' data is available
            if 'FastestLap' in result:
                fastest_lap_time = result['FastestLap']['Time']['time']
                average_speed = result['FastestLap']['AverageSpeed']['speed']
            else:
                fastest_lap_time = "N/A"
                average_speed = "N/A"

            # Add the racer details with Wikipedia link, fastest lap, average lap time, and status
            racer_info = f"Racer name: {racer_name}\nLaps: {laps}\nConstructor: {constructor}\nFastest Lap: {fastest_lap_time}\nAverage Speed: {average_speed} km/h\nStatus: {status}"

            # Add the racer information to the embed
            embed.add_field(name=f"Position {position}", value=racer_info, inline=False)

        # Send the embed in the Discord channel
        await ctx.send(embed=embed)

# Cog defining the command to main.py. 
async def setup(bot: commands.Bot):
    await bot.add_cog(F1Info(bot))
