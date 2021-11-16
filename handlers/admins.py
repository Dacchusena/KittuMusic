# Copyright (C) 2021 VeezMusicProject

from asyncio import QueueEmpty

from callsmusic import callsmusic
from callsmusic.queues import queues
from config import BOT_USERNAME, que
from cache.admins import admins
from helpers.channelmusic import get_chat_id
from helpers.dbtools import delcmd_is_on, delcmd_off, delcmd_on, handle_user_status
from helpers.decorators import authorized_users_only, errors
from helpers.filters import command, other_filters
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream
from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


@Client.on_message()
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)


# Back Button
BACK_BUTTON = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🔙 𝗚𝗼 𝗕𝗮𝗰𝗸", callback_data="cbback")]]
)

# @Client.on_message(filters.text & ~filters.private)
# async def delcmd(_, message: Message):
#    if await delcmd_is_on(message.chat.id) and message.text.startswith("/") or message.text.startswith("!") or message.text.startswith("."):
#        await message.delete()
#    await message.continue_propagation()

# remove the ( # ) if you want the auto del cmd feature is on


@Client.on_message(command(["reload", f"reload@{BOT_USERNAME}"]) & other_filters)
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "✅ 𝗕𝗼𝘁 **𝗿𝗲𝗹𝗼𝗮𝗱𝗲𝗱 𝗰𝗼𝗿𝗿𝗲𝗰𝘁𝗹𝘆 !**\n✅ **𝗔𝗱𝗺𝗶𝗻 𝗹𝗶𝘀𝘁** 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 **𝘂𝗽𝗱𝗮𝘁𝗲𝗱 !**"
    )


# Control Menu Of Player
@Client.on_message(command(["control", f"control@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def controlset(_, message: Message):
    await message.reply_text(
        "💡 **𝗵𝗲𝗿𝗲 𝗶𝘀 𝘁𝗵𝗲 𝗰𝗼𝗻𝘁𝗿𝗼𝗹 𝗺𝗲𝗻𝘂 𝗼𝗳 𝗯𝗼𝘁 :**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏸ 𝗽𝗮𝘂𝘀𝗲", callback_data="cbpause"),
                    InlineKeyboardButton("▶️ 𝗿𝗲𝘀𝘂𝗺𝗲", callback_data="cbresume"),
                ],
                [
                    InlineKeyboardButton("⏩ 𝘀𝗸𝗶𝗽", callback_data="cbskip"),
                    InlineKeyboardButton("⏹ 𝘀𝘁𝗼𝗽", callback_data="cbend"),
                ],
                [InlineKeyboardButton("⛔ 𝗮𝗻𝘁𝗶 𝗰𝗺𝗱", callback_data="cbdelcmds")],
                [InlineKeyboardButton("🗑 𝗰𝗹𝗼𝘀𝗲", callback_data="close")],
            ]
        ),
    )


@Client.on_message(command(["pause", f"pause@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    chat_id = get_chat_id(message.chat)
    ACTV_CALL = []
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALL.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALL:
        await message.reply_text("❌ **𝗻𝗼 𝗺𝘂𝘀𝗶𝗰 𝗶𝘀 𝗰𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝗽𝗹𝗮𝘆𝗶𝗻𝗴**")
    else:
        await callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text(
            "⏸ **𝗧𝗿𝗮𝗰𝗸 𝗽𝗮𝘂𝘀𝗲𝗱.**\n\n• **𝗧𝗼 𝗿𝗲𝘀𝘂𝗺𝗲 𝘁𝗵𝗲 𝗽𝗹𝗮𝘆𝗯𝗮𝗰𝗸, 𝘂𝘀𝗲 𝘁𝗵𝗲**\n» /resume 𝗰𝗼𝗺𝗺𝗮𝗻𝗱."
        )


@Client.on_message(command(["resume", f"resume@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    chat_id = get_chat_id(message.chat)
    ACTV_CALL = []
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALL.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALL:
        await message.reply_text("❌ **𝗻𝗼 𝗺𝘂𝘀𝗶𝗰 𝗶𝘀 𝗽𝗮𝘂𝘀𝗲𝗱**")
    else:
        await callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text(
            "▶️ **𝗧𝗿𝗮𝗰𝗸 𝗿𝗲𝘀𝘂𝗺𝗲𝗱.**\n\n• **𝗧𝗼 𝗽𝗮𝘂𝘀𝗲 𝘁𝗵𝗲 𝗽𝗹𝗮𝘆𝗯𝗮𝗰𝗸, 𝘂𝘀𝗲 𝘁𝗵𝗲**\n» /pause 𝗰𝗼𝗺𝗺𝗮𝗻𝗱."
        )


@Client.on_message(command(["end", f"end@{BOT_USERNAME}", "stop", f"end@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    ACTV_CALL = []
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALL.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALL:
        await message.reply_text("❌ **𝗻𝗼 𝗺𝘂𝘀𝗶𝗰 𝗶𝘀 𝗰𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝗽𝗹𝗮𝘆𝗶𝗻𝗴**")
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass
        await callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("✅ **𝗺𝘂𝘀𝗶𝗰 𝗽𝗹𝗮𝘆𝗯𝗮𝗰𝗸 𝗵𝗮𝗱 𝗲𝗻𝗱𝗲𝗱**")


@Client.on_message(command(["skip", f"skip@{BOT_USERNAME}", "next", f"next@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = message.chat.id
    ACTV_CALLS = []
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("❌ **𝗻𝗼 𝗺𝘂𝘀𝗶𝗰 𝗶𝘀 𝗰𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝗽𝗹𝗮𝘆𝗶𝗻𝗴**")
    else:
        queues.task_done(chat_id)
        
        if queues.is_empty(chat_id):
            await callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            await callsmusic.pytgcalls.change_stream(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        callsmusic.queues.get(chat_id)["file"],
                    ),
                ),
            )
                
    qeue = que.get(chat_id)
    if qeue:
        qeue.pop(0)
    if not qeue:
        return
    await message.reply_text("⏭ **𝗬𝗼𝘂'𝘃𝗲 𝘀𝗸𝗶𝗽𝗽𝗲𝗱 𝘁𝗼 𝘁𝗵𝗲 𝗻𝗲𝘅𝘁 𝘀𝗼𝗻𝗴.**")


@Client.on_message(command(["auth", f"auth@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def authenticate(client, message):
    global admins
    if not message.reply_to_message:
        return await message.reply("💡 𝗿𝗲𝗽𝗹𝘆 𝘁𝗼 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝘁𝗼 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘀𝗲 𝘂𝘀𝗲𝗿 !")
    if message.reply_to_message.from_user.id not in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.append(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply(
            "🟢 𝘂𝘀𝗲𝗿 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘀𝗲𝗱.\n\n𝗳𝗿𝗼𝗺 𝗻𝗼𝘄 𝗼𝗻, 𝘁𝗵𝗮𝘁'𝘀 𝘂𝘀𝗲𝗿 𝗰𝗮𝗻 𝘂𝘀𝗲 𝘁𝗵𝗲 𝗮𝗱𝗺𝗶𝗻 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀."
        )
    else:
        await message.reply("✅ 𝘂𝘀𝗲𝗿 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘀𝗲𝗱!")


@Client.on_message(command(["unauth", f"deauth@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def deautenticate(client, message):
    global admins
    if not message.reply_to_message:
        return await message.reply("💡 𝗿𝗲𝗽𝗹𝘆 𝘁𝗼 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝘁𝗼 𝗱𝗲𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘀𝗲 𝘂𝘀𝗲𝗿 !")
    if message.reply_to_message.from_user.id in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.remove(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply(
            "🔴 𝘂𝘀𝗲𝗿 𝗱𝗲𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘀𝗲𝗱.\n\n𝗳𝗿𝗼𝗺 𝗻𝗼𝘄 𝘁𝗵𝗮𝘁'𝘀 𝘂𝘀𝗲𝗿 𝗰𝗮𝗻'𝘁 𝘂𝘀𝗲 𝘁𝗵𝗲 𝗮𝗱𝗺𝗶𝗻 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀."
        )
    else:
        await message.reply("✅ 𝘂𝘀𝗲𝗿 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗱𝗲𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘀𝗲𝗱!")


# this is a anti cmd feature
@Client.on_message(command(["delcmd", f"delcmd@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def delcmdc(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "𝗿𝗲𝗮𝗱 𝘁𝗵𝗲 /help 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝘁𝗼 𝗸𝗻𝗼𝘄 𝗵𝗼𝘄 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱"
        )
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status == "on":
        if await delcmd_is_on(message.chat.id):
            return await message.reply_text("✅ already activated")
        await delcmd_on(chat_id)
        await message.reply_text("🟢 𝗔𝗰𝘁𝗶𝘃𝗮𝘁𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆")
    elif status == "off":
        await delcmd_off(chat_id)
        await message.reply_text("🔴 𝗗𝗶𝘀𝗮𝗯𝗹𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆")
    else:
        await message.reply_text(
            "𝗿𝗲𝗮𝗱 𝘁𝗵𝗲 /help 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝘁𝗼 𝗸𝗻𝗼𝘄 𝗵𝗼𝘄 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱"
        )


# music player callbacks (control by buttons feature)


@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 𝗼𝗻𝗹𝘆 𝗮𝗱𝗺𝗶𝗻 𝗰𝗮𝗻 𝘁𝗮𝗽 𝘁𝗵𝗶𝘀 𝗯𝘂𝘁𝘁𝗼𝗻 !", show_alert=True)
    chat_id = get_chat_id(query.message.chat)
    ACTV_CALL = []
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALL.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALL:
        await query.edit_message_text(
            "❌ **𝗻𝗼 𝗺𝘂𝘀𝗶𝗰 𝗶𝘀 𝗰𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝗽𝗹𝗮𝘆𝗶𝗻𝗴**", reply_markup=BACK_BUTTON
        )
    else:
        await callsmusic.pytgcalls.pause_stream(chat_id)
        await query.edit_message_text(
            "⏸ 𝗺𝘂𝘀𝗶𝗰 𝗽𝗹𝗮𝘆𝗯𝗮𝗰𝗸 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗽𝗮𝘂𝘀𝗲𝗱", reply_markup=BACK_BUTTON
        )


@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 𝗼𝗻𝗹𝘆 𝗮𝗱𝗺𝗶𝗻 𝗰𝗮𝗻 𝘁𝗮𝗽 𝘁𝗵𝗶𝘀 𝗯𝘂𝘁𝘁𝗼𝗻 !", show_alert=True)
    chat_id = get_chat_id(query.message.chat)
    ACTV_CALL = []
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALL.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALL:
        await query.edit_message_text(
            "❌ **𝗻𝗼 𝗺𝘂𝘀𝗶𝗰 𝗶𝘀 𝗽𝗮𝘂𝘀𝗲𝗱**", reply_markup=BACK_BUTTON
        )
    else:
        await callsmusic.pytgcalls.resume_stream(chat_id)
        await query.edit_message_text(
            "▶️ 𝗺𝘂𝘀𝗶𝗰 𝗽𝗹𝗮𝘆𝗯𝗮𝗰𝗸 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗿𝗲𝘀𝘂𝗺𝗲𝗱", reply_markup=BACK_BUTTON
        )


@Client.on_callback_query(filters.regex("cbend"))
async def cbend(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 𝗼𝗻𝗹𝘆 𝗮𝗱𝗺𝗶𝗻 𝗰𝗮𝗻 𝘁𝗮𝗽 𝘁𝗵𝗶𝘀 𝗯𝘂𝘁𝘁𝗼𝗻 !", show_alert=True)
    chat_id = get_chat_id(query.message.chat)
    ACTV_CALL = []
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALL.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALL:
        await query.edit_message_text(
            "❌ **𝗻𝗼 𝗺𝘂𝘀𝗶𝗰 𝗶𝘀 𝗰𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝗽𝗹𝗮𝘆𝗶𝗻𝗴**", reply_markup=BACK_BUTTON
        )
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass
        
        await callsmusic.pytgcalls.leave_group_call(chat_id)
        await query.edit_message_text(
            "✅ 𝘁𝗵𝗲 𝗺𝘂𝘀𝗶𝗰 𝗾𝘂𝗲𝘂𝗲 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗰𝗹𝗲𝗮𝗿𝗲𝗱 𝗮𝗻𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗹𝗲𝗳𝘁 𝘃𝗼𝗶𝗰𝗲 𝗰𝗵𝗮𝘁",
            reply_markup=BACK_BUTTON,
        )


@Client.on_callback_query(filters.regex("cbskip"))
async def cbskip(_, query: CallbackQuery):
    global que
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 𝗼𝗻𝗹𝘆 𝗮𝗱𝗺𝗶𝗻𝘀 𝗰𝗮𝗻 𝘁𝗮𝗽 𝘁𝗵𝗶𝘀 𝗯𝘂𝘁𝘁𝗼𝗻 !", show_alert=True)
    chat_id = get_chat_id(query.message.chat)
    ACTV_CALLS = []
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await query.edit_message_text(
            "❌ **𝗻𝗼 𝗺𝘂𝘀𝗶𝗰 𝗶𝘀 𝗰𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝗽𝗹𝗮𝘆𝗶𝗻𝗴**", reply_markup=BACK_BUTTON
        )
    else:
        queues.task_done(chat_id)
        
        if queues.is_empty(chat_id):
            await callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            await callsmusic.pytgcalls.change_stream(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        queues.get(query.message.chat.id)["file"],
                    ),
                ),
            )

    qeue = que.get(chat_id)
    if qeue:
        qeue.pop(0)
    if not qeue:
        return
    await query.edit_message_text(
        "⏭ **𝗬𝗼𝘂'𝘃𝗲 𝘀𝗸𝗶𝗽𝗽𝗲𝗱 𝘁𝗼 𝘁𝗵𝗲 𝗻𝗲𝘅𝘁 𝘀𝗼𝗻𝗴**", reply_markup=BACK_BUTTON
    )


@Client.on_message(command(["volume", f"volume@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def change_volume(client, message):
    range = message.command[1]
    chat_id = message.chat.id
    try:
       await callsmusic.pytgcalls.change_volume_call(chat_id, volume=int(range))
       await message.reply(f"✅ **𝘃𝗼𝗹𝘂𝗺𝗲 𝘀𝗲𝘁 𝘁𝗼:** ```{range}%```")
    except Exception as e:
       await message.reply(f"**error:** {e}")
