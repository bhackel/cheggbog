import time, os, glob, re
import discord
import asyncio
import webbrowser
import keyboard


client = discord.Client()


# Log when bot has come online
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    # Search for Chegg links in messages
    if "https://www.chegg.com/homework-help/" in message.content:
        await message.add_reaction('\U0001F504')
        # Get all Chegg homework URLs in message
        url_list = re.findall(r'(https://(?:www.)?chegg.com/homework-help/\S+)', message.content)
        
        # Send images for every url
        print(f' Chegging {url_list}')
        for url in url_list:
            # Open Chegg link
            webbrowser.open(url)
            time.sleep(5)

            # Take a screenshot using the extension
            keyboard.press_and_release('alt+shift+p')
            # Textbook pages take much longer to capture
            if "/homework-help/questions-and-answers/" in url:
                time.sleep(5)
            else:
                time.sleep(10)

            # Close the Chegg window
            keyboard.press_and_release('ctrl+w')

            # Get the file of the image by finding the newest one
            path = "C:/Users/[YOUR USERNAME]/Downloads/screenshots/*"
            file_loc = max(glob.glob(path, recursive=True), key=os.path.getmtime)

            # Send the image
            file = [discord.File(file_loc)]
            await message.channel.send(files=file)

            # Delete the image
            os.remove(file_loc)
        await message.add_reaction('\U00002705')


# Run the bot
with open('key.txt') as f:
    key = f.read()
client.run(key)
