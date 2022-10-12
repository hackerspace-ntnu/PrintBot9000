import os
from dotenv import load_dotenv
import discord


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

guilds = {}
guld_channels = {}

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        
        if message.content.startswith('!'):
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
                print(message.content)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = MyClient(intents=intents)
print(TOKEN)
client.run(TOKEN)


