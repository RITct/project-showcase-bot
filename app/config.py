"""
Load all config from environment
"""
import os
import logging
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]

GUILD_ID = os.environ.get("GUILD_ID")

DEBUG = os.environ.get("DEBUG", "false") != "false"

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

if not GUILD_ID and DEBUG:
    logging.warning("GUILD_ID shouldn't be empty in debug mode")
