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

DEBUG = os.environ.get("DEBUG", "false") != "false"

# Set your target emoji here
TARGET_EMOJI = b"\\U0001f929"

if not DEBUG and SOURCE_GUILD_ID is None:
    logging.warning("Its recommended that you provide a Source Guild ID")

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
