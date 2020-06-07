import discord
import asyncio
import requests
from discord.ext import commands


# The token is essentially the Bot's password for Discord, ensure it is kept safe.
TOKEN = 'YOUR TOKEN HERE'

# The Dominions 5 server's ip-address channel id. Obtained by right clicking the channel and copying ID.
CHANNEL_ID = 'YOUR CHANNEL ID HERE'

description = '''RPiP in Python: Reports the IP of the device as a channel message on Discord.'''
bot = commands.Bot(command_prefix='?', description=description)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def hello(ctx):
    """Says world"""
    await ctx.send("world")


@bot.command()
async def report_ip(self):
    await self.wait_until_ready()
    channel = self.get_channel(CHANNEL_ID)  # channel ID goes here.
    old_ip = requests.get('https://checkip.amazonaws.com').text.strip()

    while not self.is_closed():
        current_ip = requests.get('https://checkip.amazonaws.com').text.strip()
        if old_ip != current_ip:
            await channel.send(current_ip)
        await asyncio.sleep(300)  # task runs every 300 seconds (5 minutes)


bot.run(TOKEN)
