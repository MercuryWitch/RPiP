import discord
import asyncio
import requests


# The token is essentially the Bot's password for Discord, ensure it is kept safe.
TOKEN = 'YOUR TOKEN HERE'

# The Dominions 5 server's ip-address channel id. Obtained by right clicking the channel and copying ID.
CHANNEL_ID = 'YOUR CHANNEL ID HERE'


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
        channel = self.get_channel(CHANNEL_ID)  # channel ID goes here as an integer
        old_ip = requests.get('https://checkip.amazonaws.com').text.strip()

        while not self.is_closed():
            current_ip = requests.get('https://checkip.amazonaws.com').text.strip()
            if old_ip != current_ip:
                await channel.send(current_ip)
            await asyncio.sleep(300)  # task runs every 300 seconds (5 minutes)


client = RPiPClient()
client.run(TOKEN)
