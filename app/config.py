"""
Load all config from environment
"""
import os
import logging
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

PORT = os.environ.get("PORT", 8000)

DEBUG = os.environ.get("DEBUG", "false") != "false"

DATABASE_URL = os.environ.get("DATABASE_URL")

HOST = os.environ.get("HOST", "DUMMY")

DEFAULT_TARGET_EMOJI = 129321

STAR_EMOJI = ":star2:"

ISSUE_EMOJI = ":rotating_light:"

FORK_EMOJI = ":fork_and_knife:"

if not DATABASE_URL:
    logging.warning("DATABASE IS MISSING")
if not BOT_TOKEN:
    logging.warning("BOT_TOKEN IS MISSING")

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
    if HOST:
        logging.warning("HOST is empty")
