import asyncio
import time
from logging import getLogger

from pyrogram import enums, filters
from pyrogram.types import ChatMemberUpdated

from Pandamusic import app
from Pandamusic.core.mongo import mongodb
from Pandamusic.utils.database import get_assistant
from config import OWNER_ID

LOGGER = getLogger(__name__)

# ✅ Collection (bool/or yok)
awelcome_collection = mongodb.awelcome


class AWelDatabase:
    """
    MongoDB-backed assistant welcome state per group.

    Logic:
    - If no doc exists => welcome OFF (default True = off)
    - If doc exists and state == "off" => welcome OFF
    - Otherwise => welcome ON
    """

    @staticmethod
    async def is_off(chat_id: int) -> bool:
        doc = await awelcome_collection.find_one({"chat_id": chat_id})
        if doc is None:
            return True
        return doc.get("state") == "off"

    @staticmethod
    async def set_off(chat_id: int):
        await awelcome_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"state": "off"}},
            upsert=True,
        )

    @staticmethod
    async def set_on(chat_id: int):
        # ON olunca doc'u siliyoruz (temiz)
        await awelcome_collection.delete_one({"chat_id": chat_id})


wlcm = AWelDatabase()

# ✅ Spam prevention
user_last_message_time = {}
user_command_count = {}
SPAM_THRESHOLD = 2
SPAM_WINDOW_SECONDS = 5


@app.on_message(filters.command("awelcome") & filters.group)
async def auto_state(_, message):
    if not message.from_user:
        return

    user_id = message.from_user.id
    current_time = time.time()
    last_message_time = user_last_message_time.get(user_id, 0)

    if current_time - last_message_time < SPAM_WINDOW_SECONDS:
        user_last_message_time[user_id] = current_time
        user_command_count[user_id] = user_command_count.get(user_id, 0) + 1
        if user_command_count[user_id] > SPAM_THRESHOLD:
            hu = await message.reply_text(
                f"{message.from_user.mention} spam yapma, 5 saniye sonra tekrar dene."
            )
            await asyncio.sleep(3)
            await hu.delete()
            return
    else:
        user_command_count[user_id] = 1
        user_last_message_time[user_id] = current_time

    usage = "ᴜsᴀɢᴇ:\n⦿ /awelcome [on|off]"
    if len(message.command) == 1:
        return await message.reply_text(usage)

    chat_id = message.chat.id
    member = await app.get_chat_member(chat_id, user_id)

    if member.status not in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
        return await message.reply_text(
            "Sadece adminler /awelcome açıp kapatabilir."
        )

    state = message.text.split(None, 1)[1].strip().lower()
    is_off = await wlcm.is_off(chat_id)

    if state == "on":
        if not is_off:
            return await message.reply_text(
                "Assistant welcome zaten açık."
            )
        await wlcm.set_on(chat_id)
        return await message.reply_text(
            f"✅ Assistant welcome açıldı: {message.chat.title}"
        )

    if state == "off":
        if is_off:
            return await message.reply_text(
                "Assistant welcome zaten kapalı."
            )
        await wlcm.set_off(chat_id)
        return await message.reply_text(
            f"❌ Assistant welcome kapatıldı: {message.chat.title}"
        )

    return await message.reply_text(usage)


@app.on_chat_member_updated(filters.group, group=5)
async def greet_new_members(_, member: ChatMemberUpdated):
    try:
        chat_id = member.chat.id

        # sadece yeni katılım
        if not member.new_chat_member:
            return
        if member.old_chat_member:
            return
        if member.new_chat_member.status in {"left", "banned", "restricted"}:
            return

        is_off = await wlcm.is_off(chat_id)
        if is_off:
            return

        chat = await app.get_chat(chat_id)
        chat_name = chat.title or "Group"
        count = await app.get_chat_members_count(chat_id)

        user = member.new_chat_member.user
        if not user:
            return

        # ✅ assistant client seç
        userbot = await get_assistant(chat_id)

        # username güvenli yazım
        username_text = f"@{user.username}" if user.username else "ɴᴏᴛ sᴇᴛ"

        # owner / özel id welcome
        if user.id == OWNER_ID or user.id == 7574330905:
            text = f"""🌟 <b>𝐎ᴡɴᴇʀ ɢᴇʟᴅɪ!</b> 🌟

🔥 <b>ʙᴏss</b> {user.mention} <b>gruba katıldı!</b>
👑 <b>ᴏᴡɴᴇʀ ɪᴅ:</b> <code>{user.id}</code>
🎯 <b>ᴜsᴇʀɴᴀᴍᴇ:</b> {username_text}
👥 <b>ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs:</b> {count}
🏰 <b>ɢʀᴏᴜᴘ:</b> {chat_name}

<b>Hoş geldin boss 👑</b>"""
        else:
            text = f"""⛳️ <b>𝐆ʀᴜʙᴀ 𝐇ᴏş 𝐆ᴇʟᴅɪɴ!</b> ⛳️

➤ <b>𝐍ᴀᴍᴇ</b> {user.mention}
➤ <b>𝐔ꜱᴇʀ 𝐈ᴅ</b> <code>{user.id}</code>
➤ <b>𝐔ꜱᴇʀɴᴀᴍᴇ</b> {username_text}
➤ <b>𝐌ᴇᴍʙᴇʀs</b> {count}"""

        await asyncio.sleep(2)
        await userbot.send_message(chat_id, text=text)

    except Exception as e:
        LOGGER.error(e)
        return
