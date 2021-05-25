"""
Root file
"""
import logging
import discord
from aiohttp import web
from discord.ext.commands import has_permissions
from app.config import BOT_TOKEN, TARGET_EMOJI, TARGET_GUILD_ID, SOURCE_GUILD_ID, PORT
from app.db_crud import get_project_by_github_data, create_project
from app.utils import get_owner_and_repo, get_github_path, create_showcase_message
import aiohttp.web_request
client = discord.Client()


@client.event
async def on_ready():
    """On Login"""
    logging.info("Logged in as %s", client.user)


@client.event
@has_permissions(administrator=True)
async def on_reaction_add(reaction, _):
    """on reaction event"""
    logging.debug("Event")
    if SOURCE_GUILD_ID is None or reaction.message.channel.id == int(SOURCE_GUILD_ID):
        if TARGET_EMOJI == reaction.emoji.encode("unicode-escape"):
            try:
                owner, repo = get_owner_and_repo(reaction.message.content)
                if not get_project_by_github_data(get_github_path(owner, repo)):
                    # Check if project is already in showcase
                    channel = client.get_channel(int(TARGET_GUILD_ID))
                    message = await channel.send(create_showcase_message(owner, repo))
                    create_project({
                        "message_id": message.id,
                        "github_path": get_github_path(owner, repo)}
                    )
            except (IndexError, ValueError):
                logging.debug("Not a github url")


async def webhook_route(request):
    """
    :param request: -> aiohttp.web_request.Request
    :return: aiohttp.web_response.Response
    """
    logging.debug(await request.text())
    return web.json_response({"message": "Hello"}, status=200, content_type='application/json')

bot_task = client.loop.create_task(client.start(BOT_TOKEN))
app = web.Application()
app.router.add_post('/', webhook_route)
web.run_app(app, port=PORT)
