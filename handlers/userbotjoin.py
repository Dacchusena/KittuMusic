import asyncio
from callsmusic.callsmusic import client as USER
from config import BOT_USERNAME, SUDO_USERS
from helpers.decorators import authorized_users_only, sudo_users_only, errors
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant


@Client.on_message(
    command(["join", f"join@{BOT_USERNAME}"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def join_group(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "• **𝗜' 𝗵𝗮𝘃𝗲𝗻'𝘁 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗶𝗼𝗻:**\n\n» ❌ __Add Users__",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "music assistant"

    try:
        await USER.join_chat(invitelink)
    except UserAlreadyParticipant:
        pass
    except Exception as e:
        print(e)
        await message.reply_text(
            f"🛑 𝗙𝗹𝗼𝗼𝗱 𝗪𝗮𝗶𝘁 𝗘𝗿𝗿𝗼𝗿 🛑 \n\n**𝗞𝗶𝘁𝘁𝘂 𝗖𝗮𝗻'𝘁 𝗷𝗼𝗶𝗻 𝘆𝗼𝘂𝗿 𝗴𝗿𝗼𝘂𝗽 𝗱𝘂𝗲 𝘁𝗼 𝗵𝗲𝗮𝘃𝘆 𝗷𝗼𝗶𝗻 𝗿𝗲𝗾𝘂𝗲𝘀𝘁𝘀**"
            "\n\n**𝗼𝗿 𝗔𝗱𝗱 𝗞𝗶𝘁𝘁𝘂 𝗺𝗮𝗻𝘂𝗮𝗹𝗹𝘆 𝘁𝗼 𝘆𝗼𝘂𝗿 𝗚𝗿𝗼𝘂𝗽 𝗮𝗻𝗱 𝘁𝗿𝘆 𝗮𝗴𝗮𝗶𝗻**",
        )
        return
    await message.reply_text(
        f"✅ **𝗞𝗶𝘁𝘁𝘂 𝗘𝗻𝘁𝗲𝗿𝗲𝗱 𝗬𝗼𝘂𝗿 𝗖𝗵𝗮𝘁 🐱**",
    )


@Client.on_message(
    command(["leave", f"leave@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
@authorized_users_only
async def leave_group(client, message):
    try:
        await USER.send_message(message.chat.id, "✅ userbot successfully left chat")
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "❌ **userbot couldn't leave your group, may be floodwaits.**\n\n**» or manually kick userbot from your group**"
        )

        return


@Client.on_message(command(["leaveall", f"leaveall@{BOT_USERNAME}"]))
@sudo_users_only
async def leave_all(client, message):
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("🔄 **𝘂𝘀𝗲𝗿𝗯𝗼𝘁** 𝗹𝗲𝗮𝘃𝗶𝗻𝗴 𝗮𝗹𝗹 𝗰𝗵𝗮𝘁𝘀 !")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝗹𝗲𝗮𝘃𝗶𝗻𝗴 𝗮𝗹𝗹 𝗴𝗿𝗼𝘂𝗽...\n\n𝗟𝗲𝗳𝘁: {left} 𝗰𝗵𝗮𝘁𝘀.\n𝗙𝗮𝗶𝗹𝗲𝗱: {failed} 𝗰𝗵𝗮𝘁𝘀."
            )
        except:
            failed += 1
            await lol.edit(
                f"𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝗹𝗲𝗮𝘃𝗶𝗻𝗴...\n\n𝗟𝗲𝗳𝘁: {left} 𝗰𝗵𝗮𝘁𝘀.\n𝗙𝗮𝗶𝗹𝗲𝗱: {failed} 𝗰𝗵𝗮𝘁𝘀."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"✅ 𝗟𝗲𝗳𝘁 𝗳𝗿𝗼𝗺: {left} 𝗰𝗵𝗮𝘁𝘀.\n❌ 𝗙𝗮𝗶𝗹𝗲𝗱 𝗶𝗻: {failed} 𝗰𝗵𝗮𝘁𝘀."
    )
