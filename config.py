import os
from os import getenv
from dotenv import load_dotenv
from helpers.uptools import fetch_heroku_git_url

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
que = {}
admins = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME", "Veez Music")
BG_IMAGE = getenv("BG_IMAGE", "https://telegra.ph/file/8628c642a266a22effd8c.png")
THUMB_IMG = getenv("THUMB_IMG", "https://telegra.ph/file/0c8034d90eb46a221fa98.jpg")
AUD_IMG = getenv("AUD_IMG", "https://telegra.ph/file/9f3cf13c56d6f0cedb096.jpg")
QUE_IMG = getenv("QUE_IMG", "https://telegra.ph/file/3f75b385538d6057023f2.jpg")
CMD_IMG = getenv("CMD_IMG", "https://telegra.ph/file/5ca02029c4ab436d0aef4.jpg")
ALIVE_IMG = getenv("ALIVE_IMG", "https://telegra.ph/file/52669f3f6798e635a26a4.jpg")
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_USERNAME = getenv("BOT_USERNAME", "KittuMusicBot")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "CuteKittu")
GROUP_SUPPORT = getenv("GROUP_SUPPORT", "RazeFriendsZone")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "RazeBots")
# isi dengan username kamu tanpa simbol @
OWNER_NAME = getenv("OWNER_NAME", "dlwrml")
# fill with your nickname
ALIVE_NAME = getenv("ALIVE_NAME", "Cute kittu")
# fill with your id as the owner of the bot
OWNER_ID = int(os.environ.get("OWNER_ID"))
DATABASE_URL = os.environ.get("DATABASE_URL")  # fill with your mongodb url
# make a private channel and get the channel id
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL"))
# just fill with True or False (optional)
BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", "False"))
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "60"))
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
# UPDATER CONFIG
U_BRANCH = "main"
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
UPSTREAM_REPO = os.environ.get(
    "UPSTREAM_REPO", "https://github.com/levina-lab/VeezMusic"
)
HEROKU_URL = fetch_heroku_git_url(HEROKU_API_KEY, HEROKU_APP_NAME)
