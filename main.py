import discord
import requests
import json
import string
from decouple import config

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("avali.hu")
    await client.change_presence(status=discord.Status.idle, activity=game)

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('>birb'):
        url = "https://e621.net/posts.json?limit=1?&tags=order:random%20rating:s%20avali%20-vore%20-luvashi"
        headers = {"User-Agent": "aUserAgent"}
        response = requests.get(url, headers=headers)
        data = json.loads(response.content.decode('utf-8'))
        await message.channel.send(data['posts'][0]['file']['url'])


    elif message.content.startswith('>e6'):
        try:
            if message.channel.is_nsfw():
                msg = message.content
                msg = msg.replace(">e6", "")
                url = "https://e621.net/posts.json?limit=1?&tags=order:random%20rating:e%20" + msg
                headers = {"User-Agent": "aUserAgent"}
                response = requests.get(url, headers=headers)
                data = json.loads(response.content.decode('utf-8'))
                await message.channel.send(data['posts'][0]['file']['url'])
            else:
                await message.channel.send('sorry but only for NSFW cahnnels')
        except:
            await message.channel.send('Something went wrong.....')


    elif message.content.startswith('>info'):
        await message.channel.send("Birb BOT 2.1 by Geri#1337 | https://github.com/GeriTheFox")

client.run(config('TOKEN'))