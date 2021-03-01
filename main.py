# pip install discord.py, beautifulsoup4, lxml, python-dotenv
import os

import discord
from dotenv import load_dotenv



if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')

    client = discord.Client()

    @client.event
    async def on_ready():
        guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

    @client.event
    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to my Discord server! Make yourself at home. Hop in one of our voice channels any time, we have a great community that would love for you to hop in. If you have any questions hit up a Guru for guidance.'
        )
            

    client.run(TOKEN)