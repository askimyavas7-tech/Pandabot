# Copyright (c) 2026 HAN THAR
# Location: Supaul, Bihar
#
# All rights reserved.
#
# This code is the intellectual property of Nand Yaduwanshi.
# You are not allowed to copy, modify, redistribute, or use this
# code for commercial or personal projects without explicit permission.
#
# Allowed:
# - Forking for personal learning
# - Submitting improvements via pull requests
#
# Not Allowed:
# - Claiming this code as your own
# - Re-uploading without credit or permission
# - Selling or using commercially
#
# Contact for permissions:
# Email: tzkgaming2019@gmail.com

import asyncio
import importlib

from pyrogram import idle
from pyrogram.types import BotCommand
from pyrogram.errors import FloodWait
from pytgcalls.exceptions import NoActiveGroupCall

import config
from Pandamusic import LOGGER, app, userbot
from Pandamusic.core.call import Nand
from Pandamusic.misc import sudo
from Pandamusic.plugins import ALL_MODULES
from Pandamusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

COMMANDS = [
    BotCommand("start", "❖ sᴛᴀʀᴛ ʙᴏᴛ • ᴛᴏ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ"),
    BotCommand("help", "❖ ʜᴇʟᴘ ᴍᴇɴᴜ • ɢᴇᴛ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴀɴᴅ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ"),
    BotCommand("ping", "❖ ᴘɪɴɢ ʙᴏᴛ • ᴄʜᴇᴄᴋ ᴘɪɴɢ ᴀɴᴅ sʏsᴛᴇᴍ sᴛᴀᴛs"),
    BotCommand("play", "❖ ᴘʟᴀʏ ᴀᴜᴅɪᴏ ᴏɴ ᴠᴄ • ᴛᴏ ᴘʟᴀʏ ᴀɴʏ ᴀᴜᴅɪᴏ ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ"),
    BotCommand("vplay", "❖ ᴘʟᴀʏ ᴠɪᴅᴇᴏ ᴏɴ ᴠᴄ • ᴛᴏ sᴛʀᴇᴀᴍ ᴀɴʏ ᴠɪᴅᴇᴏ ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ"),
    BotCommand("playrtmps", "❖ ᴘʟᴀʏ ʟɪᴠᴇ ᴠɪᴅᴇᴏ • sᴛʀᴇᴀᴍ ʟɪᴠᴇ ᴠɪᴅᴇᴏ ᴄᴏɴᴛᴇɴᴛ"),
    BotCommand("playforce", "❖ ғᴏʀᴄᴇ ᴘʟᴀʏ ᴀᴜᴅɪᴏ • ғᴏʀᴄᴇ ᴘʟᴀʏ ᴀɴʏ ᴀᴜᴅɪᴏ ᴛʀᴀᴄᴋ"),
    BotCommand("vplayforce", "❖ ғᴏʀᴄᴇ ᴘʟᴀʏ ᴠɪᴅᴇᴏ • ғᴏʀᴄᴇ ᴘʟᴀʏ ᴀɴʏ ᴠɪᴅᴇᴏ ᴛʀᴀᴄᴋ"),
    BotCommand("pause", "❖ ᴘᴀᴜsᴇ sᴛʀᴇᴀᴍ • ᴘᴀᴜsᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ sᴛʀᴇᴀᴍ"),
    BotCommand("resume", "❖ ʀᴇsᴜᴍᴇ sᴛʀᴇᴀᴍ • ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴘᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ"),
    BotCommand("skip", "❖ sᴋɪᴘ ᴛʀᴀᴄᴋ • sᴋɪᴘ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴛʀᴀᴄᴋ"),
    BotCommand("end", "❖ ᴇɴᴅ sᴛʀᴇᴀᴍ • sᴛᴏᴘ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ"),
    BotCommand("stop", "❖ sᴛᴏᴘ sᴛʀᴇᴀᴍ • sᴛᴏᴘ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ sᴛʀᴇᴀᴍ"),
    BotCommand("queue", "❖ sʜᴏᴡ ǫᴜᴇᴜᴇ • ᴅɪsᴘʟᴀʏ ᴛʀᴀᴄᴋ ǫᴜᴇᴜᴇ ʟɪsᴛ"),
    BotCommand("auth", "❖ ᴀᴅᴅ ᴀᴜᴛʜ ᴜsᴇʀ • ᴀᴅᴅ ᴜsᴇʀ ᴛᴏ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ʟɪsᴛ"),
    BotCommand("unauth", "❖ ʀᴇᴍᴏᴠᴇ ᴀᴜᴛʜ • ʀᴇᴍᴏᴠᴇ ᴜsᴇʀ ғʀᴏᴍ ᴀᴜᴛʜ ʟɪsᴛ"),
    BotCommand("authusers", "❖ ᴀᴜᴛʜ ʟɪsᴛ • sʜᴏᴡ ᴀʟʟ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀs"),
    BotCommand("cplay", "❖ ᴄʜᴀɴɴᴇʟ ᴀᴜᴅɪᴏ • ᴘʟᴀʏ ᴀᴜᴅɪᴏ ɪɴ ᴄʜᴀɴɴᴇʟ"),
    BotCommand("cvplay", "❖ ᴄʜᴀɴɴᴇʟ ᴠɪᴅᴇᴏ • ᴘʟᴀʏ ᴠɪᴅᴇᴏ ɪɴ ᴄʜᴀɴɴᴇʟ"),
    BotCommand("cplayforce", "❖ ᴄʜᴀɴɴᴇʟ ғᴏʀᴄᴇ ᴀᴜᴅɪᴏ • ғᴏʀᴄᴇ ᴘʟᴀʏ ɪɴ ᴄʜᴀɴɴᴇʟ"),
    BotCommand("cvplayforce", "❖ ᴄʜᴀɴɴᴇʟ ғᴏʀᴄᴇ ᴠɪᴅᴇᴏ • ғᴏʀᴄᴇ ᴘʟᴀʏ ᴠɪᴅᴇᴏ ɪɴ ᴄʜᴀɴɴᴇʟ"),
    BotCommand("channelplay", "❖ ᴄᴏɴɴᴇᴄᴛ ᴄʜᴀɴɴᴇʟ • ʟɪɴᴋ ɢʀᴏᴜᴘ ᴛᴏ ᴄʜᴀɴɴᴇʟ"),
    BotCommand("loop", "❖ ʟᴏᴏᴘ ᴍᴏᴅᴇ • ᴇɴᴀʙʟᴇ ᴏʀ ᴅɪsᴀʙʟᴇ ʟɪᴠᴇ ʟᴏᴏᴘ"),
    BotCommand("stats", "❖ ʙᴏᴛ sᴛᴀᴛs • sʜᴏᴡ ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs"),
    BotCommand("shuffle", "❖ sʜᴜғғʟᴇ ǫᴜᴇᴜᴇ • ʀᴀɴᴅᴏᴍɪᴢᴇ ᴛʀᴀᴄᴋ ᴏʀᴅᴇʀ"),
    BotCommand("seek", "❖ sᴇᴇᴋ ғᴏʀᴡᴀʀᴅ • sᴋɪᴘ ᴛᴏ sᴘᴇᴄɪғɪᴄ ᴛɪᴍᴇ"),
    BotCommand("seekback", "❖ sᴇᴇᴋ ʙᴀᴄᴋᴡᴀʀᴅ • ɢᴏ ʙᴀᴄᴋ ᴛᴏ ᴘʀᴇᴠɪᴏᴜs ᴛɪᴍᴇ"),
    BotCommand("song", "❖ ᴅᴏᴡɴʟᴏᴀᴅ sᴏɴɢ • ɢᴇᴛ ᴍᴘ3 ᴏʀ ᴍᴘ4 ғɪʟᴇ"),
    BotCommand("speed", "❖ ᴀᴅᴊᴜsᴛ sᴘᴇᴇᴅ • ᴄʜᴀɴɢᴇ ᴘʟᴀʏʙᴀᴄᴋ sᴘᴇᴇᴅ ɪɴ ɢʀᴏᴜᴘ"),
    BotCommand("cspeed", "❖ ᴄʜᴀɴɴᴇʟ sᴘᴇᴇᴅ • ᴀᴅᴊᴜsᴛ sᴘᴇᴇᴅ ɪɴ ᴄʜᴀɴɴᴇʟ"),
    BotCommand("tagall", "❖ ᴛᴀɢ ᴀʟʟ • ᴍᴇɴᴛɪᴏɴ ᴇᴠᴇʀʏᴏɴᴇ ɪɴ ɢʀᴏᴜᴘ"),
]


async def setup_bot_commands():
    try:
        await app.set_bot_commands(COMMANDS)
        LOGGER("Pandamusic").info("Bot commands set successfully!")
    except Exception as e:
        LOGGER("Pandamusic").error(f"Failed to set bot commands: {e}")


async def _safe_start(client, name: str):
    """
    FloodWait gelirse restart döngüsüne girmesin diye bekler.
    """
    while True:
        try:
            await client.start()
            LOGGER("Pandamusic").info(f"{name} started.")
            return
        except FloodWait as e:
            wait_s = int(getattr(e, "value", 0) or 0)
            if wait_s <= 0:
                wait_s = 5
            LOGGER("Pandamusic").warning(f"FloodWait ({name}): {wait_s}s. Bekleniyor...")
            await asyncio.sleep(wait_s + 5)
        except Exception as e:
            # Başlangıç hatası varsa spam restart olmasın
            LOGGER("Pandamusic").error(f"{name} start failed: {e}")
            await asyncio.sleep(5)


def _has_any_assistant_string() -> bool:
    return any(
        [
            getattr(config, "STRING1", None),
            getattr(config, "STRING2", None),
            getattr(config, "STRING3", None),
            getattr(config, "STRING4", None),
            getattr(config, "STRING5", None),
        ]
    )


async def _import_all_plugins():
    """
    ALL_MODULES içindeki modülleri doğru path ile import eder.
    Eski hata: "Pandamusic.plugins" + all_module (nokta yok)
    """
    ok = 0
    fail = 0

    for m in ALL_MODULES:
        mod = str(m).strip()

        # ".start" gibi gelirse düzelt
        mod = mod.lstrip(".")

        # boş modül gelirse geç
        if not mod:
            continue

        full = f"Pandamusic.plugins.{mod}"
        try:
            importlib.import_module(full)
            ok += 1
        except Exception as e:
            fail += 1
            LOGGER("Pandamusic.plugins").error(f"Failed to import {full}: {e}")

    LOGGER("Pandamusic.plugins").info(f"Plugins imported. OK={ok} FAIL={fail}")


async def init():
    if not _has_any_assistant_string():
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        return

    # sudo init
    try:
        await sudo()
    except Exception as e:
        LOGGER("Pandamusic").error(f"sudo() failed: {e}")

    # banned lists
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)

        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER("Pandamusic").warning(f"Could not load banned users: {e}")

    # Start bot
    await _safe_start(app, "app")
    await setup_bot_commands()

    # Import plugins (DÜZELTİLDİ)
    await _import_all_plugins()

    # Start userbot
    await _safe_start(userbot, "userbot")

    # Start call client
    try:
        await Nand.start()
    except Exception as e:
        LOGGER("Pandamusic").error(f"Nand.start() failed: {e}")

    # VC kapalıysa kapanmasın
    try:
        await Nand.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("Pandamusic").warning(
            "Log group VC kapalı. Bot çalışmaya devam ediyor. Müzik çalmak için VC aç."
        )
    except Exception as e:
        LOGGER("Pandamusic").warning(f"stream_call skipped: {e}")

    # Decorators
    try:
        await Nand.decorators()
    except Exception as e:
        LOGGER("Pandamusic").warning(f"Nand.decorators() failed: {e}")

    LOGGER("Pandamusic").info(
        "\x50\x61\x6e\x64\x61\x20\x4d\x75\x73\x69\x63\x20\x42\x6f\x74\x20\x53\x74\x61\x72\x74\x65\x64\x20\x53\x75\x63\x63\x65\x73\x73\x66\x75\x6c\x6c\x79\x2e"
    )

    # Keep alive
    await idle()

    # Stop
    try:
        await app.stop()
    except Exception:
        pass
    try:
        await userbot.stop()
    except Exception:
        pass

    LOGGER("Pandamusic").info("Stopping Panda Music Bot...🥺")


if __name__ == "__main__":
    asyncio.run(init())
