"""
Root file
"""
import json
import logging
import re
from aiohttp import web
from discord import Intents
from discord.ext import commands
from discord.ext.commands import has_permissions
from app.config import BOT_TOKEN, PORT
from app.db_crud import create_project, create_server, update_server_data, get_server_by_id, get_projects_by_github_data
from app.utils import (
    get_owner_and_repo,
    get_github_path,
    create_showcase_message,
    dm_user_webhook_info,
    get_repo_data,
    is_project_in_server, get_emoji_code
)

intents = Intents.default()
intents.presences = True
intents.reactions = True
client = commands.Bot(command_prefix="$", intents=intents)


@client.event
async def on_ready():
    """On Login"""
    logging.info("Logged in as %s", client.user)


@client.event
async def on_guild_join(guild):
    logging.debug("JOIN TRIGGERED")
    create_server(guild.id)


@client.command()
async def set_target_channel(ctx, arg):
    """
    Set Target Channel Discord Command
    """
    channel_id = int(re.findall("<#(.+?)>", arg).pop())
    channel = await client.fetch_channel(channel_id)
    if channel is None:
        await ctx.send("Invalid channel")
    else:
        update_server_data(ctx.guild.id, {"targetChannel": channel_id})
        await ctx.send("Target channel set to <#%s>" % channel_id)


@client.event
@has_permissions(administrator=True)
async def on_raw_reaction_add(reaction):
    """on reaction event"""
    logging.debug("Event")

    this_channel = await client.fetch_channel(reaction.channel_id)
    message = await this_channel.fetch_message(reaction.message_id)

    try:
        owner, repo = get_owner_and_repo(message.content)
    except (IndexError, ValueError):
        logging.debug("Not a github url")
        return

    server_info = get_server_by_id(this_channel.guild.id)
    logging.debug(ord(str(reaction.emoji)))
    if server_info["targetEmoji"] == get_emoji_code(reaction.emoji):

        github_path = get_github_path(owner, repo)

        if not is_project_in_server(server=server_info, github_path=github_path):
            # Check if project is already in showcase
            if not server_info.get("targetChannel"):
                await this_channel.send(
                    "Target channel is not configured, use $set_target_channel <channel_link> to set channel"
                )
            target_channel = client.get_channel(server_info["targetChannel"])
            target_message = await target_channel.send(
                create_showcase_message(
                    get_repo_data(owner, repo)
                )
            )
            await dm_user_webhook_info(message.author)
            create_project({
                "serverId": server_info["serverId"],
                "messageId": target_message.id,
                "githubPath": github_path
            })


async def webhook_route(request):
    """
    :param request: -> aiohttp.web_request.Request
    :return: aiohttp.web_response.Response
    """
    data = await request.post()
    payload = json.loads(data["payload"])
    servers_containing_project = \
        get_projects_by_github_data(payload["repository"]["full_name"])

    msg = create_showcase_message(payload["repository"])

    for server in servers_containing_project:
        channel = client.get_channel(int(server["targetChannel"]))
        project_in_server = [project for project in server.get("projects") if project["githubPath"] ==
                             payload["repository"]["full_name"]][0]

        message = await channel.fetch_message(project_in_server["messageId"])
        await message.edit(content=msg)

    return web.json_response({"message": "Hello"}, status=200, content_type='application/json')

bot_task = client.loop.create_task(client.start(BOT_TOKEN))
app = web.Application()
app.router.add_post('/', webhook_route)
web.run_app(app, port=PORT)
