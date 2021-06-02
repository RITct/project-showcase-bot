"""
Handle DB
"""
import pymongo
from .config import DATABASE_URL, TARGET_EMOJI

db_client = pymongo.MongoClient(DATABASE_URL)["Showcase"]
project_collection = db_client["projects"]
server_collection = db_client["servers"]


def create_project(data: dict):
    """
    :param data -> {server_id(UNIQUE STR), github_path(STR), message_id(UNIQUE STR)}
    :return: None
    """
    results = server_collection.update(
        {"serverId": data["server_id"]},
        {"$push": {
            "githubPath": data["github_path"],
            "messageId": data["message_id"]
        }}
    )
    return results.matched_count > 0


def get_server_by_id(server_id: str):
    """
    :param server_id: Discord Server's unique ID
    :return: {
        "serverId": str,
        "sourceChannel": Optional[str],
        "targetChannel": str,
        "targetEmoji": str,
        "projects": List[{
            "messageId: str,
            "githubPath": str
        }]
    """
    return server_collection.find_one({"server_id": server_id})


def create_server(server_id: int):
    """
    :param server_id: Discord Server's unique ID
    """
    server_collection.insert_one({"server_id": server_id, "target_emoji": TARGET_EMOJI})


def get_projects_by_github_data(github_path: str):
    """
    :param github_path: Path of the github repo eg: RITct/project-discord-bot
    :return: List[ref line 29]
    """
    return server_collection.find({"projects": {"github_path": github_path}})
