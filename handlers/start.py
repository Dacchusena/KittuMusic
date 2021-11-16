from datetime import datetime
from sys import version_info
from time import time

from config import (
    ALIVE_IMG,
    ALIVE_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)
from handlers import __version__
from helpers.decorators import sudo_users_only
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram import __version__ as pyrover
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited
)
async def start_private(client: Client, message: Message):
    await message.reply_text(
        f"""✨ **Welcome {message.from_user.mention()} !**\n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) allows you to play music on groups through the new Telegram's voice chats!**

💡 **Find out all the Bot's commands and how they work by clicking on the » 📚 Commands button!**

🔖 **To know how to use this bot, please click on the » ❓ Basic Guide button!**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ 𝗔𝗱𝗱 𝗠𝗲 𝗧𝗼 𝗬𝗼𝘂𝗿 𝗚𝗿𝗼𝘂𝗽 ➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("❓ 𝗕𝗮𝘀𝗶𝗰 𝗚𝘂𝗶𝗱𝗲", callback_data="cbhowtouse")],
                [
                    InlineKeyboardButton("📚 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀", callback_data="cbcmds"),
                    InlineKeyboardButton("🍻 𝗗𝗼𝗻𝗮𝘁𝗲", url=f"https://t.me/{OWNER_NAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "✌️ 𝗢𝗳𝗳𝗶𝗰𝗶𝗮𝗹 𝗚𝗿𝗼𝘂𝗽", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 𝗨𝗽𝗱𝗮𝘁𝗲𝘀", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "👻 𝗢𝘄𝗻𝗲𝗿", url="https://t.me/XDacchuX"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def start_group(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✨ 𝗚𝗿𝗼𝘂𝗽", url=f"https://t.me/{GROUP_SUPPORT}"),
                InlineKeyboardButton(
                    "📣 𝗖𝗵𝗮𝗻𝗻𝗲𝗹", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
            ]
        ]
    )

    alive = f"**Hello {message.from_user.mention()}, 𝗜'𝗺 {BOT_NAME}**\n\n✨ 𝗛𝗲𝘆 𝗕𝗼𝘁 𝗜𝘀 𝗪𝗼𝗿𝗸𝗶𝗻𝗴 𝗡𝗼𝗿𝗺𝗮𝗹𝗹𝘆!\n🍀 𝗠𝘆 𝗠𝗮𝘀𝘁𝗲𝗿: [{ALIVE_NAME}](https://t.me/{OWNER_NAME})\n✨ 𝗕𝗼𝘁 𝗩𝗲𝗿𝘀𝗶𝗼𝗻: `v{__version__}`\n🍀 𝗣𝘆𝗿𝗼𝗴𝗿𝗮𝗺 𝗩𝗲𝗿𝘀𝗶𝗼𝗻: `{pyrover}`\n✨ 𝗣𝘆𝘁𝗵𝗼𝗻 𝗩𝗲𝗿𝘀𝗶𝗼𝗻: `{__python_version__}`\n🍀 𝗨𝗽𝘁𝗶𝗺𝗲 𝗦𝘁𝗮𝘁𝘂𝘀: `{uptime}`\n\n**Thanks for Adding me here, for playing music on your Group voice chat** 🔥"

    await message.reply_photo(
        photo=f"{ALIVE_IMG}",
        caption=alive,
        reply_markup=keyboard,
    )


@Client.on_message(
    command(["help", f"help@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def help(client: Client, message: Message):
    await message.reply_text(
        f"""✨ **Hello** {message.from_user.mention()} !

» **press the button below to read the explanation and see the list of available commands !**

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="❓ 𝗕𝗮𝘀𝗶𝗰 𝗚𝘂𝗶𝗱𝗲", callback_data="cbguide")]]
        ),
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 `𝗣𝗢𝗡𝗚!!`\n" f"⚡️ `{delta_ping * 1000:.3f} ms`")


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 bot status:\n"
        f"• **uptime:** `{uptime}`\n"
        f"• **start time:** `{START_TIME_ISO}`"
    )
