import discord
import os
import string

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
    # check to make sure it only contains the words bruh
    # this is not working, so I'm doing another trick
    #lst = re.split(string.punctuation, message.content)
    lst = "".join([" " if c in {i for i in string.punctuation} else c for c in message.content]).split()

    # Checks to make sure every word is bruh
    for word in lst:
      word = word.lower()
      for i in word:
        if not i in {'b', 'r', 'u', 'h'}:
          await message.delete()
          return
    await message.channel.send("Bruh")

client.run(os.getenv("TOKEN"))