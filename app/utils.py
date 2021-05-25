"""
Common utils
"""
import json
import logging
import re
from urllib import request

from app.config import STAR_EMOJI, ISSUE_EMOJI, FORK_EMOJI


def get_owner_and_repo(message: str) -> str:
    """Get owner and repo name from url"""
    logging.debug(message)
    return re.findall("^https://github\\.com/(.+?)/(.+)", message)[0]


def get_repo_data(owner: str, repo: str) -> dict:
    """
    Get details like stars, forks, issues, description, website
    of a github repo
    """
    req = request.Request("https://api.github.com/repos/%s/%s" % (owner, repo))
    req.add_header("Accept", "application/vnd.github.v3+json")
    response = request.urlopen(req).read()
    return json.loads(response)


def create_showcase_message(owner: str, repo: str) -> str:
    """
    Create the discord message using repo parameters
    """
    repo_data = get_repo_data(owner, repo)
    msg = ""
    if repo_data["description"]:
        msg += repo_data["description"] + "\n\n"
    if repo_data["homepage"]:
        msg += "Website: " + repo_data["homepage"] + "\n\n"
    msg += "https://github.com/%s\n\n" % get_github_path(owner, repo)
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
