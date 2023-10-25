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

# Define your Trello API key and token
api_key = os.getenv('TRELLO_API_KEY')
api_token = os.getenv('TRELLO_API_TOKEN')

# Define your Trello list ID
list_id = os.getenv('TRELLO_LIST_ID')

# Define a function to find the Roblox ID from the username
def find_roblox_id(username):
    # Use the Roblox API to find the Roblox ID
    api_url = f"https://users.roblox.com/v1/usernames/users"
    params = {"usernames": [username], "excludeBannedUsers": False}
    response = requests.post(api_url, json=params)
    data = response.json()
    # Check if the username is valid or not
    if data["data"]:
        # Return the Roblox ID
        roblox_id = data["data"][0]["id"]
        return roblox_id
    else:
        # Return None
        return None

# Create an embed for the process started message
embed_process_started = discord.Embed(title="Card Creation", description="Creating card. Please wait...", color=0x00ff00)

# Create an embed for success
embed_success = discord.Embed(title="Success!", description="Card created successfully!", color=0x00ff00)

# Create an embed for errors
embed_error = discord.Embed(title="Error", description="Failed to create card. Please try again later.", color=0xff0000)

# Create an embed for timeout
embed_timeout = discord.Embed(title="Timeout", description="You took too long to provide a ticket number. Please use the `!rep` command again.", color=0xff0000)

# Create an embed for card deletion
embed_card_deleted = discord.Embed(title="Card Deleted", description="The card was deleted due to inactivity.", color=0xff0000)

# Defining cog class.
class Rep(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Trello command
    @commands.command()
    async def rep(self, ctx, username, *attachments):
        # Check if the user's ID is in the list of allowed user IDs
        if str(ctx.author.id) not in allowed_user_ids:
            await ctx.send(embed=discord.Embed(title="Permission Denied", description="You do not have permission to use this command.", color=0xff0000))
            return

        # Find the Roblox ID from the username
        roblox_id = find_roblox_id(username)
        # Check if the Roblox ID is None or not
        if roblox_id is None:
            await ctx.send(embed=embed_error)
        else:
            # Send a message to notify that the process has started
            process_message = await ctx.send(embed=embed_process_started)

            # Define base URL for Trello API
            base_url = "https://api.trello.com/1"
            # Define common parameters for Trello API
            params = {"key": api_key, "token": api_token}
            # Define name for card
            card_name = f"{username} - {roblox_id}"
            # Define URL for creating card
            card_url = f"{base_url}/cards"
            # Define parameters for creating card
            card_params = {"idList": list_id, "name": card_name}
            # Make POST request to create card
            card_response = requests.post(card_url, params=params, data=card_params)
            # Check if card creation was successful
            if card_response.status_code == 200:
                # Log success message
                print(f"Card created successfully for {username} (Requested by {ctx.author})")

                # Attach any provided message attachments to the card
                for attachment in ctx.message.attachments:
                    # Download the attachment file
                    attachment_response = requests.get(attachment.url)
                    if attachment_response.status_code == 200:
                        # Define URL for attaching file to card
                        file_url = f"{base_url}/cards/{card_response.json()['id']}/attachments"
                        # Define parameters for attaching file to card
                        file_params = {"url": file_url}
                        # Make POST request to attach file to card
                        file_response = requests.post(file_url, params=params, data=file_params, files={"file": attachment_response.content})
                        # Check if file attachment was successful
                        if file_response.status_code == 200:
                            # Log success message
                            print(f"File attached successfully to card {card_name}")
                        else:
                            # Log error message
                            print(f"Failed to attach file to card {card_name}")
                    else:
                        # Log error message
                        print(f"Failed to download attachment for card {card_name}")

                # Check if there are any links provided in the message text
                if attachments:
                    for link in attachments:
                        # Process each link in the attachments argument
                        
                        image_attachment_params = {
                            "url": link,  # Assuming the link is an image URL
                            "name": "Link Attachment"
                        }
                        image_attachment_url = f"{base_url}/cards/{card_response.json()['id']}/attachments"
                        image_attachment_response = requests.post(image_attachment_url, params=params, data=image_attachment_params)
                        if image_attachment_response.status_code == 200:
                            pass  # Handle success as needed
                        else:
                            pass  # Handle error as needed

                # Ask the user for a ticket number
                await process_message.edit(embed=discord.Embed(title="Ticket Number", description="Please provide the ticket number as a reply to this message.", color=0x00ff00))

                try:
                    # Wait for a response for 2 minutes
                    response = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel, timeout=120)
                    ticket_number = response.content
                except asyncio.TimeoutError:
                    # Handle the timeout error
                    await ctx.send(embed=embed_timeout)

                    # Add a print statement to log the timeout
                    print("User timed out while waiting for a ticket number.")
                    
                    # Delete the card from Trello
                    card_delete_url = f"{base_url}/cards/{card_response.json()['id']}"
                    card_delete_response = requests.delete(card_delete_url, params=params)
                    if card_delete_response.status_code == 200:
                        pass  # Handle success as needed
                    else:
                        pass  # Handle error as needed

                    # Edit the message to notify that the card was deleted
                    await process_message.edit(embed=embed_card_deleted)

                # Add the ticket number, Discord username, and timestamp to the card description
                description = f"Ticket Number: {ticket_number}\nDiscord User: {ctx.author.name}\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                description_url = f"{base_url}/cards/{card_response.json()['id']}/desc"
                description_params = {"value": description}
                description_response = requests.put(description_url, params=params, data=description_params)
                if description_response.status_code == 200:
                    # Notify the user that the description was updated
                    await ctx.send(embed=discord.Embed(title="Description Updated", description=f"Description updated on card {card_name}.", color=0x00ff00))
                    print(f"Description updated successfully for card {card_name}")
                else:
                    # Notify the user of an error
                    await ctx.send(embed=embed_error)

                # Notify the user that the card and attachments were added
                await ctx.send(embed=embed_success)
            else:
                # Notify the user of an error
                await process_message.edit(embed=embed_error)
                
# Cog defining the command to main.py.
async def setup(bot: commands.Bot):
    await bot.add_cog(Rep(bot))
