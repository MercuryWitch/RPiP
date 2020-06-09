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
        
        # Try to initialize the ip address.
        try:
            self.my_ip = requests.get('https://checkip.amazonaws.com').text.strip()
        except:
            print('Something seems to have gone wrong.')
            await channel.send("Oh dear, I think something went wrong, sorry.")
        
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
        await channel.send(self.my_ip)
        
        while not self.is_closed():
            try:
                current_ip = requests.get('https://checkip.amazonaws.com').text.strip()
            except:
                current_ip = self.my_ip
                print("Heads up, the bot had an exception when it tried to check the current ip")
            if self.my_ip != current_ip:
                await channel.send(current_ip)
                self.my_ip = current_ip
            await asyncio.sleep(300)  # task runs every 300 seconds (5 minutes)
    
    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('?ip'):
            try:
                await message.channel.send(requests.get('https://checkip.amazonaws.com').text.strip())
            except:
                await message.channel.send("Looks like there was a problem with getting the ip address, try again later.")


client = RPiPClient()
client.run(TOKEN)
