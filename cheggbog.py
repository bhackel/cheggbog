import time, os, glob, re
import discord
import asyncio
import webbrowser
import keyboard


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
    if "https://www.chegg.com/homework-help/" in message.content:
        # Check if bot is already chegging
        global running
        if running:
            await message.reply("Please resend the link to get a response")
            return

        await message.add_reaction('\U0001F504')
        running = True
        # Get all Chegg homework URLs in message
        url_list = re.findall(r'(https://(?:www.)?chegg.com/homework-help/\S+)', message.content)
        
        # Send images for every url
        print(f' Chegging {url_list}')
        for url in url_list:
            # Open Chegg link
            webbrowser.open(url)
            await asyncio.sleep(8)

            # Trigger the screenshot extension
            keyboard.press_and_release('alt+shift+p')

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
            keyboard.press_and_release('ctrl+w')

            # Send the image
            file = [discord.File(file_loc)]
            await message.channel.send(files=file)

            # Delete the image
            os.remove(file_loc)
        await message.add_reaction('\U00002705')
        running = False


# Run the bot
with open('key.txt') as f:
    key = f.read()
client.run(key)
