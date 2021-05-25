"""
Handle DB
"""
import pymongo
from .config import DATABASE_URL

db_client = pymongo.MongoClient(DATABASE_URL)["Showcase"]
project_collection = db_client["projects"]


def create_project(data: dict):
    """
    :param data -> {github_path(UNIQUE STR), message_id(UNIQUE STR)}
    :return: None
    """
    project_collection.insert_one(data)


def get_project_by_github_data(github_path: str):
    """
    :param github_path -> repo_owner/repo_name
    :return: dict -> {"github_path": str, "message_id": str}
    """
    return project_collection.find_one({"github_path": github_path})
