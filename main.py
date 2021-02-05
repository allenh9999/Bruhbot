import discord
import os
import string
import requests
import json
import time
import random

# Opens the client
client = discord.Client()

@client.event
# If there's a message sent
async def on_message(message):
  # make sure it's not the bot
  if message.author == client.user:
    return

  # if it's in the bruh channel
  if message.channel.name == "bruh":
    # if the message requests a comic, give a comic
    if message.content.lower() == "!comic":
      await get_comic(message)
      return

    if message.content.lower() == "!joke":
      await get_joke(message)
      return

    if message.content.lower() == "!help":
      await get_help(message)
      return

    # check to make sure it only contains the words bruh
    for i in message.content:
      i = i.lower()
      if not i in {'b', 'r', 'u', 'h'} | {j for j in string.punctuation} | {' '}:
        await message.delete()
        return
    await message.channel.send("Bruh")


async def get_comic(message):
  """
  Gets a comic from XKCD

  :param message: the message sent
  """
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36\
    (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
  # Special thanks to Krithik for this part
  url = requests.get('https://xkcd.com/{0}/info.0.json'.format(random.randint(0,2419)), headers = headers)
  website = url.json()
  await message.channel.send(website["img"])


async def get_joke(message):
  """
  Gets a joke from reddit.com/r/dadjokes

  :param message: the message sent
  """
  # Get the website
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36\
    (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
  url = requests.get('https://www.reddit.com/r/dadjokes/.json', headers=headers)
  website = url.json()
  sum_over_18 = 0
  for i in website['data']['children']:
    if i['data']['over_18']:
      sum_over_18 += 1

  # if there are 23 over-18 posts, you can't find a under 18 joke
  if sum_over_18 >= 23:
    await message.channel.send("Sorry, but I cannot find a good joke right now")
    return

  # Hacked do-while loop
  while True:
    post = random.randint(2,24)
    if not website['data']['children'][post]['data']['over_18']:
      post_str = website['data']['children'][post]['data']['title']
      content_str = website['data']['children'][post]['data']['selftext']
      await message.channel.send(post_str + '\n||' + content_str + '||')
      return


async def get_help(message):
  # Print the help message
  await message.channel.send("Hi! I'm a bot that allows only combinations of b,r,u,h in the #bruh channel.\n\
Commands:\n\
      !help (shows this text)\n\
      !joke (gets a joke from r/dadjokes)\n\
      !comic (gets a random comic from xkcd)")


# Run the discord bot
client.run("ODA3MjgwNTEzMzUzNjQ2MTUw.YB1skA.HDgd1mafR3dbpQD1vkJRV-YJK0o")
