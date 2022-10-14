import os
from dotenv import load_dotenv
import discord
from os import system
import requests


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
dry_run = True

guilds = {}
guld_channels = {}

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        
        if message.content.startswith('!') and message.author.guild_permissions.administrator:
            command = message.content[1:]
            if command == 'join':
                if message.guild.id not in guilds:
                    guilds[message.guild.id] = message.guild
                    await message.channel.send('Joined server!')
                else:
                    await message.channel.send('Already joined server!')
            elif command == 'leave':
                if message.guild.id in guilds:
                    guilds.pop(message.guild.id)
                    await message.channel.send('Left server!')
                else:
                    await message.channel.send('Not in server!')
            elif command == 'listen':
                if message.guild.id in guilds:
                    if message.guild.id not in guld_channels:
                        guld_channels[message.guild.id] = message.channel
                        await message.channel.send('Listening to this channel!')
                    else:
                        await message.channel.send('Already listening to this channel!')
                else:
                    await message.channel.send('Not in server!')
            elif command == 'unlisten':
                if message.guild.id in guilds:
                    if message.guild.id in guld_channels:
                        guld_channels.pop(message.guild.id)
                        await message.channel.send('Stopped listening to this channel!')
                    else:
                        await message.channel.send('Not listening to this channel!')
                else:
                    await message.channel.send('Not in server!')
            elif command == 'print':
                for guild in guilds.values():
                    for channel in guild.channels:
                        if channel.name == 'general':
                            await channel.send('Hello world!')
                            break
            else:
                await message.channel.send('Unknown command!')
        
        if message.guild.id in guld_channels:
            if message.channel == guld_channels[message.guild.id]:
                if dry_run:
                    print(message.author)
                    print(message.content)
                    if message.attachments:
                        print(message.attachments[0].url)

                else:
                    command = f"echo {(message.author)} | lp"
                    system(command)
                    command = f"echo {(message.content)} | lp"
                    system(command)
                    if message.attachments:
                        file_extention = message.attachments[0].url.split('.')[-1]
                        filename = "meme" + "." + file_extention
                        r = requests.get(message.attachments[0].url, stream=True)
                        if r.status_code != 200:
                            print("Error getting image")
                            return
                        with open(filename, "wb") as f:
                            for chunk in r:
                                f.write(chunk)
                        command = f"lp -o fit-to-page {filename}"
                        system(command)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = MyClient(intents=intents)
print(TOKEN)
client.run(TOKEN)
