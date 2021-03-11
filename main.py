"""Main program of the discord bot."""


import os
import string
import random
import requests
import discord
import asyncio


# Opens the client
client = discord.Client()


# channel name
channel = "bruh"


@client.event
# If there's a message sent
async def on_message(message):
    """
    Handle the messages from the discord.

    :param message: the message sent
    """
    # make sure it's not the bot
    if message.author == client.user:
        return

    # if it's in the bruh channel
    if message.channel.name == channel:
        # if the message requests a comic, give a comic
        if message.content.lower() == "!comic":
            await get_comic(message)
            return

        if message.content.lower() == "!joke":
            await get_joke(message)
            return

        if message.content.lower() == "!meme":
            await get_meme(message)
            return

        if message.content.lower() == "!help":
            await get_help(message)
            return

        # check to make sure it only contains the words bruh
        lst = {'b', 'r', 'u', 'h'} | set(string.punctuation) | {' '}
        for i in message.content:
            i = i.lower()
            if i not in lst:
                await message.delete()
                return
        await message.channel.send("Bruh")


@client.event
async def on_message_edit(before, after):
    if before.author == client.user:
        return
    if before.channel.name == channel:
        await before.channel.send("Don't abuse me:cry:")
        await after.delete()

async def get_comic(message):
    """
    Get a comic from XKCD.

    :param message: the message sent
    """
    headers = {'User-Agent': 'Mozilla/5.0 \
      (Windows NT 6.2; Win64; x64) AppleWebKit/537.36\
      (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    # Special thanks to Krithik for this part
    url = 'https://xkcd.com/{0}/info.0.json'.format(random.randint(0, 2419))
    url = requests.get(url, headers=headers)
    website = url.json()
    await message.channel.send(website["img"])


async def get_joke(message):
    """
    Get a joke from reddit.com/r/dadjokes.

    :param message: the message sent
    """
    # Get the website
    headers = {'User-Agent': 'Mozilla/5.0 \
      (Windows NT 6.2; Win64; x64) AppleWebKit/537.36\
      (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    url = 'https://www.reddit.com/r/dadjokes/.json'
    url = requests.get(url, headers=headers)
    website = url.json()
    sum_over_18 = 0
    for i in website['data']['children']:
        if i['data']['over_18']:
            sum_over_18 += 1

    # if there are 23 over-18 posts, you can't find a under 18 joke
    if sum_over_18 >= 23:
        content = "Sorry, but I cannot find a good joke right now"
        await message.channel.send(content)
        return

    # Hacked do-while loop
    while True:
        post = random.randint(2, 24)
        if not website['data']['children'][post]['data']['over_18']:
            post_str = website['data']['children'][post]['data']['title']
            content_str = website['data']['children'][post]['data']['selftext']
            await message.channel.send(post_str + '\n||' + content_str + '||')
            return


async def get_meme(message):
    """
    Get a joke from reddit.com/r/memes.

    :param message: the message sent
    """
    # Get the website
    headers = {'User-Agent': 'Mozilla/5.0 \
      (Windows NT 6.2; Win64; x64) AppleWebKit/537.36\
      (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    url = requests.get('https://www.reddit.com/r/memes/.json', headers=headers)
    website = url.json()
    sum_allowed = 0
    for i in website['data']['children']:
        if not i['data']['over_18'] and 'post_hint' in i['data']\
           and i['data']['post_hint'] == 'image':
            sum_allowed += 1

    # If there are over 2 allowed posts, continue
    if sum_allowed <= 2:
        content = "Sorry, but I cannot find a good meme right now"
        await message.channel.send(content)
        return

    # Hacked do-while loop
    while True:
        post = website['data']['children'][random.randint(2, 24)]['data']
        if not post['over_18'] and 'post_hint' in post\
           and post['post_hint'] == 'image':
            post_str = post['title']
            content_str = post['preview']['images'][0]['resolutions'][-1]
            content_str = content_str['url'].replace('&amp;', '&')
            await message.channel.send(post_str + '\n' + content_str)
            return


async def get_help(message):
    """
    Print the help statement.

    :param message: the message sent
    """
    await message.channel.send("Hi! I'm a bot that allows only \
combinations of b,r,u,h in the #bruh channel.\n\
Commands:\n\
        !help (shows this text)\n\
        !joke (gets a joke from r/dadjokes)\n\
        !comic (gets a random comic from xkcd)\n\
        !meme (gets a meme from r/memes)")


# Run the discord bot
client.run(os.getenv("TOKEN"))
