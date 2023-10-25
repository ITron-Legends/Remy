import discord
from discord.ext import commands
import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Function to create a command list embed with descriptions
    def create_command_list(self):
        embed = discord.Embed(
            title="Command List",
            color=discord.Color.blue()
        )
        return embed

    @commands.hybrid_command(name="help", description="Help command.")
    async def help(self, ctx: commands.Context):
        # Create the command list embed
        embed = self.create_command_list()
        
        # Add fields for each category with descriptions
        embed.add_field(
            name="「 🛠️ 」Moderation commands",
            value="• `!find`: Get Roblox user's information.\n• `!rep`: Automated reporting to Trello!\n• `!who`: Get's any users discord information! Even works for users outside the server!\n• `!trlist (page number) / !trlist recent`:                               Get's Pending list of Exploiters.\n• `!loc`: Funni, dont use.",
            inline=False
        )
        
        embed.add_field(
            name="「 🎉 」Fun commands",
            value="• `!ball`: Magic 8-ball.\n• `!meme`: Get a random meme.\n• `!ping`: Pong! Shows the latency of the Bot response.\n• `!insult`: Insult a user.\n• `!apod`: Astronomy Picture of the Day.\n• `!color r g b`: Sends a random color / specified color.\n• `!f1`: Information about the latest F1 race",
            inline=False
        )

        
        # You can add more fields and descriptions here as needed

        # Send the embed
        await ctx.send(embed=embed )

# Cog defining the command to main.py. 
async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))