"""
Common utils
"""
import json
import logging
import re
from urllib import request


def get_owner_and_repo(message):
    """Get owner and repo name from url"""
    logging.debug(message)
    return re.findall("^https://github\\.com/(.+?)/(.+)", message)[0]


def get_description(owner, repo):
    """Get description of a github repo"""
    req = request.Request("https://api.github.com/repos/%s/%s" % (owner, repo))
    req.add_header("Accept", "application/vnd.github.v3+json")
    response = request.urlopen(req).read()
    description = json.loads(response)["description"]
    if description is not None:
        return description
    return ""
