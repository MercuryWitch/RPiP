import discord
import asyncio
import requests


# The token is essentially the Bot's password for Discord, ensure it is kept safe.
TOKEN = 'YOUR TOKEN HERE'

# The Dominions 5 server's ip-address channel id. Obtained by right clicking the channel and copying ID.
CHANNEL_ID = 0  # YOUR CHANNEL ID HERE, it should be an integer


class RPiPClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.report_ip_background_task())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def report_ip_background_task(self):
        await self.wait_until_ready()
        channel = self.get_channel(CHANNEL_ID)
        old_ip = requests.get('https://checkip.amazonaws.com').text.strip()
        await channel.send(old_ip)
        
        while not self.is_closed():
            current_ip = requests.get('https://checkip.amazonaws.com').text.strip()
            if old_ip != current_ip:
                await channel.send(current_ip)
            await asyncio.sleep(300)  # task runs every 300 seconds (5 minutes)
    
    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('?ip'):
            await message.channel.send(requests.get('https://checkip.amazonaws.com').text.strip())


client = RPiPClient()
client.run(TOKEN)
