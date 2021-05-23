import discord
import logging
from app.config import BOT_TOKEN

client = discord.Client()


@client.event
async def on_ready():
    logging.info("Logged in as %s" % client.user)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

client.run(BOT_TOKEN)
