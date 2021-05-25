"""
Root file
"""
import json
import logging
import discord
from aiohttp import web
from discord.ext.commands import has_permissions
from app.config import BOT_TOKEN, TARGET_EMOJI, TARGET_CHANNEL_ID, SOURCE_CHANNEL_ID, PORT
from app.db_crud import get_project_by_github_data, create_project
from app.utils import (
    get_owner_and_repo,
    get_github_path,
    create_showcase_message,
    dm_user_webhook_info,
    get_repo_data
)

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
    if SOURCE_CHANNEL_ID is None or reaction.message.channel.id == int(SOURCE_CHANNEL_ID):
        if TARGET_EMOJI == reaction.emoji.encode("unicode-escape"):
            try:
                owner, repo = get_owner_and_repo(reaction.message.content)
                if not get_project_by_github_data(get_github_path(owner, repo)):
                    # Check if project is already in showcase
                    channel = client.get_channel(int(TARGET_CHANNEL_ID))
                    message = await channel.send(
                        create_showcase_message(
                            get_repo_data(owner, repo)
                        )
                    )
                    await dm_user_webhook_info(reaction.message.author)
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
    data = await request.post()
    payload = json.loads(data["payload"])
    repo_in_db = get_project_by_github_data(payload["repository"]["full_name"])

    msg = create_showcase_message(payload["repository"])
    channel = client.get_channel(int(TARGET_CHANNEL_ID))
    message = await channel.fetch_message(repo_in_db["message_id"])
    await message.edit(content=msg)

    return web.json_response({"message": "Hello"}, status=200, content_type='application/json')

bot_task = client.loop.create_task(client.start(BOT_TOKEN))
app = web.Application()
app.router.add_post('/', webhook_route)
web.run_app(app, port=PORT)
