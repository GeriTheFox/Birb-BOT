from discord.ext import tasks
import discord
import requests
import json
import string
from decouple import config

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_background_task.start()

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(client))

    @tasks.loop(seconds=config('INTERVALL'))
    async def my_background_task(self):
        channel = self.get_channel(config('CHANNEL'))
        url = "https://e621.net/posts.json?limit=1?&tags=order:random%20rating:s"
        headers = {"User-Agent": "aUserAgent"}
        response = requests.get(url, headers=headers)
        data = json.loads(response.content.decode('utf-8'))
        await channel.send("Daily vali:")
        await channel.send(data['posts'][0]['file']['url'])

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()

client = MyClient()
client.run(config('TOKEN'))