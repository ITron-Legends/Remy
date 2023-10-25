import discord
from discord.ext import commands
import requests
import random

class ColorInfo(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="color", description="Random color")
    async def color(self, ctx: commands.Context, red: int, green: int, blue: int):
        """Random color
        
        Parameters
        --------------------
        red: int 
           Input the red value from RGB
        green: int
           Input the green value from RGB
        blue: int
           Input the blue value from RGB
           
        """
        # Check if the RGB values are in range
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            await ctx.send('Please enter valid RGB values between 0 and 255.')
            return

        # Construct the API url with the RGB values
        api_url = f'https://www.thecolorapi.com/id?rgb={red},{green},{blue}&format=json'

        # Make a GET request to the API and get the JSON response
        response = requests.get(api_url).json()

        # Extract the information from the response
        color_name = response['name']['value']
        hex_number = response['hex']['value']
        rgb_values = response['rgb']['value']
        hsv_values = response['hsv']['value']
        hsl_values = response['hsl']['value']

        # Construct the image url with the hex number
        image_url = f'https://singlecolorimage.com/get/{hex_number[1:]}/400x400.png'

        # Construct the html url with the RGB values
        html_url = f'https://www.thecolorapi.com/id?rgb={red},{green},{blue}&format=html'

        # Create an embed object with the color information and a clickable title
        embed = discord.Embed(title=color_name, url=html_url, color=discord.Color.from_rgb(red, green, blue))
        embed.add_field(name='Hex', value=hex_number, inline=True)
        embed.add_field(name='RGB', value=rgb_values, inline=True)
        embed.add_field(name='HSV', value=hsv_values, inline=True)
        embed.add_field(name='HSL', value=hsl_values, inline=True)
        embed.set_thumbnail(url=image_url)

        # Send the embed to the channel
        await ctx.send(embed=embed)

    @color.error
    async def color_error(self, ctx, error):
        # If the user does not provide any arguments, generate random values and call the color command again
        
        embed_error = discord.Embed(title="Wrong Input!", description="Please enter valid RGB values between 0 and 255.", color=0x00ff00)
        
        if isinstance(error, commands.MissingRequiredArgument):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            await self.color(ctx, r, g, b)
        # If the user provides invalid arguments that cannot be converted to integers, send an error message
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=embed_error ,ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(ColorInfo(bot))
