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
  if message.channel.name == "test":
    # if the message requests a comic, give a comic
    if message.content.lower() == "!comic":
      await get_comic(message)
      return

    # check to make sure it only contains the words bruh
    for i in message.content:
      i = i.lower()
      if not i in {'b', 'r', 'u', 'h'} | {j for j in string.punctuation}:
        await message.delete()
        return
    await message.channel.send("Bruh")


async def get_comic(message):
  """Gets a comic from XKCD

  :param message: the message to send
  """
  # Special thanks to Krithik for this part
  url = requests.get('https://xkcd.com/{0}/info.0.json'.format(random.randint(0,2419)))
  website = url.json()
  await message.channel.send(website["img"])


# Run the discord bot
client.run(os.getenv("TOKEN"))
