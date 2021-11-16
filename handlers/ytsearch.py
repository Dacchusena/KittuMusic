import json
import logging

from config import BOT_USERNAME
from helpers.filters import command
from pyrogram import Client
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from youtube_search import YoutubeSearch

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


@Client.on_message(command(["search", f"search@{BOT_USERNAME}"]))
async def ytsearch(_, message: Message):
    
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🗑 𝗖𝗹𝗼𝘀𝗲", callback_data="close",
                )
            ]
        ]
    )
    
    try:
        if len(message.command) < 2:
            await message.reply_text("/search **𝗻𝗲𝗲𝗱𝘀 𝗮𝗻 𝗮𝗿𝗴𝘂𝗲𝗺𝗲𝗻𝘁 !**")
            return
        query = message.text.split(None, 1)[1]
        m = await message.reply_text("🔎 **𝗦𝗲𝗮𝗿𝗰𝗵𝗶𝗻𝗴...**")
        results = YoutubeSearch(query, max_results=5).to_dict()
        i = 0
        text = ""
        while i < 5:
            text += f"🏷 **𝗡𝗮𝗺𝗲:** __{results[i]['title']}__\n"
            text += f"⏱ **𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻:** `{results[i]['duration']}`\n"
            text += f"👀 **𝗩𝗶𝗲𝘄𝘀:** `{results[i]['views']}`\n"
            text += f"📣 **𝗖𝗵𝗮𝗻𝗻𝗲𝗹:** {results[i]['channel']}\n"
            text += f"🔗: https://www.youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        await m.edit(text, reply_markup=keyboard, disable_web_page_preview=True)
    except Exception as e:
        await m.edit(str(e))
