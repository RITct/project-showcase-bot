"""
Handle DB
"""
from typing import List

import pymongo
from .config import DATABASE_URL, DEFAULT_TARGET_EMOJI

db_client = pymongo.MongoClient(DATABASE_URL)["Showcase"]
server_collection = db_client["servers"]


def create_project(data: dict) -> bool:
    """
    :param data: {server_id(UNIQUE STR), github_path(STR), message_id(UNIQUE STR)}
    :return: success: bool
    """
    results = server_collection.update(
        {"serverId": data["serverId"]},
        {"$push": {
            "projects": {
                "githubPath": data["githubPath"],
                "messageId": data["messageId"]
            }
        }}
    )
    return results.get("matched_count", 0) > 0


def get_server_by_id(server_id: int) -> dict:
    """
    :param server_id: Discord Server's unique ID
    :return: {
        "serverId": int,
        "targetChannel": str,
        "targetEmoji": str,
        "projects": List[{
            "messageId: str,
            "githubPath": str
        }]
    """
    return server_collection.find_one({"serverId": server_id})


def create_server(server_id: int) -> None:
    """
    :param server_id: Discord Server's unique ID
    """
    if not get_server_by_id(server_id):
        server_collection.insert_one({
            "serverId": server_id,
            "targetEmoji": DEFAULT_TARGET_EMOJI
        })


def get_projects_by_github_data(github_path: str) -> List[dict]:
    """
    :param github_path: Path of the github repo eg: RITct/project-discord-bot
    :return: List[Server]
    """
    return server_collection.find({"projects": {"github_path": github_path}})


def update_server_data(server_id: int, updated_data: dict) -> None:
    """
    :param server_id: Discord Server's unique ID
    :param updated_data: {
        "targetChannel": Optional[int],
        "targetEmoji": Optional[str],
    }
    :return:
    """
    target_keys = ("targetChannel", "targetEmoji")
    verified_data = {"$set": {key: val for key, val in updated_data.items() if key in target_keys}}
    server_collection.update_one({"serverId": server_id}, verified_data, upsert=False)
