import asyncio
import random

from pyrogram import filters
from pyrogram.types import Message

from Pandamusic import app, userbot, LOGGER
from Pandamusic.core.userbot import assistants
from Pandamusic.utils.database import get_served_chats, get_served_users
from Pandamusic.utils.functions.decorators import sudo_only

# Broadcast plugin


@app.on_message(filters.command(["broadcast"]) & filters.private)
@sudo_only
async def broadcast_message(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a message to broadcast it.\n\nUsage: `/broadcast` (reply)"
        )

    x = message.reply_to_message
    done = 0
    failed = 0
    served_chats = await get_served_chats()

    await message.reply_text("🔄 Broadcasting...")

    for chat in served_chats:
        try:
            await x.copy(chat["chat_id"])
            done += 1
            await asyncio.sleep(0.2)
        except Exception:
            failed += 1
            continue

    await message.reply_text(f"✅ Broadcast Completed!\n\nDone: {done}\nFailed: {failed}")


@app.on_message(filters.command(["ubroadcast"]) & filters.private)
@sudo_only
async def user_broadcast(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a message to broadcast it to users.\n\nUsage: `/ubroadcast` (reply)"
        )

    x = message.reply_to_message
    done = 0
    failed = 0
    served_users = await get_served_users()

    await message.reply_text("🔄 Broadcasting to users...")

    for user in served_users:
        try:
            await x.copy(user["user_id"])
            done += 1
            await asyncio.sleep(0.2)
        except Exception:
            failed += 1
            continue

    await message.reply_text(f"✅ User Broadcast Completed!\n\nDone: {done}\nFailed: {failed}")


@app.on_message(filters.command(["assistantbroadcast"]) & filters.private)
@sudo_only
async def assistant_broadcast(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a message to broadcast it using assistants.\n\nUsage: `/assistantbroadcast` (reply)"
        )

    x = message.reply_to_message
    done = 0
    failed = 0
    served_chats = await get_served_chats()

    await message.reply_text("🔄 Broadcasting with assistants...")

    for chat in served_chats:
        try:
            for client in assistants:
                try:
                    await x.copy(chat["chat_id"], from_chat_id=message.chat.id)
                    done += 1
                    break
                except Exception:
                    continue
            await asyncio.sleep(0.2)
        except Exception:
            failed += 1
            continue

    await message.reply_text(
        f"✅ Assistant Broadcast Completed!\n\nDone: {done}\nFailed: {failed}"
    )
