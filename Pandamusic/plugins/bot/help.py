import asyncio

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Pandamusic import app
from Pandamusic.utils.inline.help import (
    first_page,
    help_back_markup,
    help_buttons,
    help_pannel,
    private_help_panel,
)
from Pandamusic.utils.functions import cln
from Pandamusic.utils.functions.decorators import is_admin
from Pandamusic.utils.inline import paginate_modules
from Pandamusic.utils.stream.stream import stream
from Pandamusic.utils import database

from config import SUPPORT_GROUP

# Help command handler

@app.on_message(filters.command(["help"]) & filters.group)
@is_admin
async def help_command(_, message):
    if message.chat.type == "private":
        return await help_private(_, message)

    try:
        await message.reply_text(
            "📩 **Check your private messages for help menu!**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "💬 Open Help Menu",
                            url=f"https://t.me/{app.username}?start=help",
                        )
                    ]
                ]
            ),
        )
    except Exception:
        await message.reply_text("❌ I couldn't send you a message. Please start me in PM first.")


@app.on_message(filters.command(["help"]) & filters.private)
async def help_private(_, message):
    await message.reply_text(
        help_pannel(),
        reply_markup=InlineKeyboardMarkup(
            [
                *help_buttons(),
                [
                    InlineKeyboardButton("🔙 Back", callback_data="close_help"),
                ],
            ]
        ),
    )


@app.on_callback_query(filters.regex(r"help_callback"))
async def help_callback(_, callback_query):
    data = callback_query.data
    if data == "help_callback":
        await callback_query.message.edit_text(
            help_pannel(),
            reply_markup=InlineKeyboardMarkup(
                [
                    *help_buttons(),
                    [
                        InlineKeyboardButton("🔙 Back", callback_data="close_help"),
                    ],
                ]
            ),
        )


@app.on_callback_query(filters.regex(r"close_help"))
async def close_help(_, callback_query):
    await callback_query.message.delete()


@app.on_callback_query(filters.regex(r"help_(?!back|home).*"))
async def help_modules(_, callback_query):
    module = callback_query.data.split("_", 1)[1]
    help_text = database.get_help_text(module)

    await callback_query.message.edit_text(
        help_text,
        reply_markup=InlineKeyboardMarkup(help_back_markup(module)),
        disable_web_page_preview=True,
    )


@app.on_callback_query(filters.regex(r"help_back_"))
async def help_back(_, callback_query):
    module = callback_query.data.split("_", 2)[2]
    await callback_query.message.edit_text(
        help_pannel(),
        reply_markup=InlineKeyboardMarkup(
            [
                *help_buttons(),
                [
                    InlineKeyboardButton("🔙 Back", callback_data="close_help"),
                ],
            ]
        ),
    )


@app.on_callback_query(filters.regex(r"help_home"))
async def help_home(_, callback_query):
    await callback_query.message.edit_text(
        help_pannel(),
        reply_markup=InlineKeyboardMarkup(
            [
                *help_buttons(),
                [
                    InlineKeyboardButton("🔙 Back", callback_data="close_help"),
                ],
            ]
        ),
    )


@app.on_callback_query(filters.regex(r"help_menu"))
async def help_menu(_, callback_query):
    await callback_query.message.edit_text(
        private_help_panel(),
        reply_markup=InlineKeyboardMarkup(
            [
                *private_help_panel(),
                [
                    InlineKeyboardButton("🔙 Back", callback_data="help_home"),
                ],
            ]
        ),
    )


@app.on_callback_query(filters.regex(r"help_tutorial"))
async def help_tutorial(_, callback_query):
    text = (
        "📚 **Tutorial**\n\n"
        "➤ Add the bot to your group and make it admin.\n"
        "➤ Start a voice chat.\n"
        "➤ Use `/play` to play music.\n"
        "➤ Use `/vplay` to stream video.\n\n"
        f"Need support? Join: {SUPPORT_GROUP}"
    )
    await callback_query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🔙 Back", callback_data="help_home")],
            ]
        ),
        disable_web_page_preview=True,
    )


@app.on_callback_query(filters.regex(r"help_commands"))
async def help_commands(_, callback_query):
    await callback_query.message.edit_text(
        first_page(),
        reply_markup=InlineKeyboardMarkup(
            [
                *paginate_modules(0, help_pannel()),
                [InlineKeyboardButton("🔙 Back", callback_data="help_home")],
            ]
        ),
        disable_web_page_preview=True,
    )


@app.on_callback_query(filters.regex(r"help_next\((.+)\)"))
async def help_next(_, callback_query):
    page = int(callback_query.matches[0].group(1))
    await callback_query.message.edit_reply_markup(
        InlineKeyboardMarkup(
            [
                *paginate_modules(page, help_pannel()),
                [InlineKeyboardButton("🔙 Back", callback_data="help_home")],
            ]
        )
    )


@app.on_callback_query(filters.regex(r"help_prev\((.+)\)"))
async def help_prev(_, callback_query):
    page = int(callback_query.matches[0].group(1))
    await callback_query.message.edit_reply_markup(
        InlineKeyboardMarkup(
            [
                *paginate_modules(page, help_pannel()),
                [InlineKeyboardButton("🔙 Back", callback_data="help_home")],
            ]
        )
    )


@app.on_callback_query(filters.regex(r"help_close"))
async def help_close(_, callback_query):
    await callback_query.message.delete()
