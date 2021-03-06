"""
Common utils
"""
import json
import logging
import re
from urllib import request

from app.config import STAR_EMOJI, ISSUE_EMOJI, FORK_EMOJI, HOST


def get_owner_and_repo(message: str) -> str:
    """Get owner and repo name from url"""
    logging.debug(message)
    return re.findall("https://github\\.com/(.+?)/(.+)", message)[0]


def get_repo_data(owner: str, repo: str) -> dict:
    """
    Get details like stars, forks, issues, description, website
    of a github repo
    """
    req = request.Request("https://api.github.com/repos/%s/%s" % (owner, repo))
    req.add_header("Accept", "application/vnd.github.v3+json")
    response = request.urlopen(req).read()
    return json.loads(response)


def create_showcase_message(repo_data: dict) -> str:
    """
    Create the discord message using repo parameters
    """
    msg = "**%s**" % repo_data["name"] + "\n"
    if repo_data["description"]:
        msg += repo_data["description"] + "\n\n"
    if repo_data["homepage"]:
        msg += "Website: " + repo_data["homepage"] + "\n\n"
    msg += "Github Link: https://github.com/%s\n\n" % repo_data["full_name"]
    msg += "%s: %d\t%s: %d\t%s: %d" % (
        STAR_EMOJI,
        repo_data["stargazers_count"],
        ISSUE_EMOJI,
        repo_data["open_issues"],
        FORK_EMOJI,
        repo_data["forks"]
    )
    return msg


def get_github_path(owner: str, repo: str) -> str:
    """Get github path from owner and repo name"""
    return "%s/%s" % (owner, repo)


def is_project_in_server(server: dict, github_path: str) -> bool:
    """Check if project is in server"""
    # pylint: disable=use-a-generator
    return any(
        [project.get("githubPath") == github_path for project in server.get("projects", {})])


def get_emoji_code(raw_emoji: str):
    """
    :param raw_emoji: The raw str emoji
    :return: ascii code of emoji
    """
    return ord(str(raw_emoji))


async def send_target_channel_missing_error(channel):
    """ Send Target Channel Not Set Error Message """
    await channel.send(
        "Target channel is not configured, use $set_target_channel <channel_link> to set channel"
    )


async def dm_user_webhook_info(user) -> None:
    """
    :param user: UserId
    Send a dm to the user, to integrate webhooks
    """
    msg = """
Congrats on getting your project showcased....
If you want to update us about the wonderful journey of your project,
Add this webhook %s
to your repo with with issues, stars, forks, pull requests events.
If you have more queries about webhook, visit https://docs.github.com/en/developers/webhooks-and-events/webhooks.

**I'm a bot, don't reply** 
    """ % HOST
    await user.send(msg)
