"""
Root file
"""
import logging
import discord
from discord.ext.commands import has_permissions
from app.config import BOT_TOKEN, TARGET_EMOJI, TARGET_GUILD_ID, SOURCE_GUILD_ID
from app.utils import get_description, get_owner_and_repo

client = discord.Client()


@client.event
async def on_ready():
    """On Login"""
    logging.info("Logged in as %s", client.user)


@client.event
@has_permissions(administrator=True)
async def on_reaction_add(reaction, _):
    """on reaction event"""
    if SOURCE_GUILD_ID is None or reaction.message.channel.id == int(SOURCE_GUILD_ID):
        if TARGET_EMOJI == reaction.emoji.encode("unicode-escape"):
            try:
                owner, repo = get_owner_and_repo(reaction.message.content)
                desc = get_description(owner, repo)
                channel = client.get_channel(int(TARGET_GUILD_ID))
                await channel.send("%s\n%s" % (desc, reaction.message.content))
            except (IndexError, ValueError):
                logging.debug("Not a github url")

client.run(BOT_TOKEN)
