import asyncio
import glob
import os
import re
import webbrowser

import discord
from pynput.keyboard import Key, Controller

keyboard = Controller()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
running = False


# Log when bot has come online
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    # Search for Chegg links in messages
    url_list = re.findall(r'chegg\.com/homework-help/\S+', message.content)
    if len(url_list) > 0:
        # Check if bot is already chegging
        global running
        if running:
            await message.reply("Please resend the link to get a response")
            return

        await message.add_reaction('\U0001F504')
        running = True

        # Send images for every url
        print(f' Chegging {url_list}')
        for url in url_list:
            # Open Chegg link
            webbrowser.open(f'https://{url}')
            await asyncio.sleep(12)

            # Trigger the screenshot extension
            with keyboard.pressed(Key.alt), keyboard.pressed(Key.shift):
                keyboard.press('p')
                keyboard.release('p')

            # Get the file of the image by finding the newest one
            path = "C:/Users/[YOUR USERNAME]/Downloads/screenshots/*.jpg"

            # Continually check folder for a new image (assumes empty before)
            for i in range(20):
                print(f"Checking files {i}")
                files = glob.glob(path, recursive=True)
                if len(files) > 0:
                    file_loc = max(files, key=os.path.getmtime)
                    break

                await asyncio.sleep(1)
            else:
                print("Failed to find the image. Try checking the path.")
                await message.add_reaction('\U0000274C')
                running = False
                return

            # Close the Chegg window
            with keyboard.pressed(Key.ctrl):
                keyboard.press('w')
                keyboard.release('w')

            # Send the image
            file = [discord.File(file_loc)]
            await message.channel.send(files=file)

            # Delete the image
            os.remove(file_loc)
        await message.add_reaction('\U00002705')
        running = False


# Run the bot
with open('key.txt') as f:
    key = f.read().strip()
client.run(key)
