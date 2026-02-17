import asyncio
import importlib
from pyrogram import idle
from pyrogram.types import BotCommand
from pytgcalls.exceptions import NoActiveGroupCall
import config
from Pandamusic import LOGGER, app, userbot
from Pandamusic.core.call import Nand
from Pandamusic.misc import sudo
from Pandamusic.plugins import ALL_MODULES
from Pandamusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


COMMANDS = [
    BotCommand("start", "Start the bot"),
    BotCommand("help", "Show help menu"),
    BotCommand("ping", "Check bot ping"),
    BotCommand("play", "Play audio in VC"),
    BotCommand("vplay", "Play video in VC"),
    BotCommand("pause", "Pause stream"),
    BotCommand("resume", "Resume stream"),
    BotCommand("skip", "Skip track"),
    BotCommand("stop", "Stop stream"),
    BotCommand("queue", "Show queue"),
]


async def setup_bot_commands():
    try:
        await app.set_bot_commands(COMMANDS)
        LOGGER("Pandamusic").info("Bot commands set successfully!")
    except Exception as e:
        LOGGER("Pandamusic").error(f"Failed to set bot commands: {e}")


async def init():

    # Assistant string kontrolü
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER("Pandamusic").error("Assistant String Session not defined!")
        return

    await sudo()

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)

        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)

    except Exception:
        pass

    await app.start()
    LOGGER("Pandamusic").info("Bot client started")

    await setup_bot_commands()

    for module in ALL_MODULES:
        importlib.import_module("Pandamusic.plugins" + module)

    LOGGER("Pandamusic.plugins").info("Plugins imported successfully")

    await userbot.start()
    LOGGER("Pandamusic").info("Assistant started")

    await Nand.start()
    LOGGER("Pandamusic").info("Call client started")

    # 🚀 ARTIK BOT KAPANMAZ
    try:
        await Nand.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("Pandamusic").warning(
            "Log group VC kapalı. Bot çalışmaya devam ediyor."
        )
    except Exception as e:
        LOGGER("Pandamusic").warning(f"Stream test skipped: {e}")

    await Nand.decorators()

    LOGGER("Pandamusic").info("✅ Panda Music Bot Started Successfully!")

    await idle()

    await app.stop()
    await userbot.stop()
    LOGGER("Pandamusic").info("Bot stopped.")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
