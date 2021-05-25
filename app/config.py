"""
Load all config from environment
"""
import os
import logging
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]

SOURCE_GUILD_ID = os.environ.get("SOURCE_GUILD_ID")

TARGET_GUILD_ID = os.environ["TARGET_GUILD_ID"]

PORT = os.environ.get("PORT", 8000)

DEBUG = os.environ.get("DEBUG", "false") != "false"

DATABASE_URL = os.environ["DATABASE_URL"]

# Set your target emoji here
TARGET_EMOJI = b"\\U0001f929"

STAR_EMOJI = ":star2:"

ISSUE_EMOJI = ":rotating_light:"

FORK_EMOJI = ":alien:"

if not DEBUG and SOURCE_GUILD_ID is None:
    logging.warning("Its recommended that you provide a Source Guild ID")

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
