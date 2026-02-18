from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Pandamusic import app


HELP_TEXT = (
    "🎵 <b>Panda Music Bot — Yardım</b>\n\n"
    "✅ <b>Temel Komutlar</b>\n"
    "• /play <i>şarkı adı / link</i>\n"
    "• /vplay <i>video adı / link</i>\n"
    "• /pause — duraklat\n"
    "• /resume — devam\n"
    "• /skip — sonraki\n"
    "• /stop — durdur\n"
    "• /queue — sıra\n\n"
    "👑 <b>Yönetici</b>\n"
    "• /auth, /unauth, /authusers\n"
    "• /settings, /stats\n\n"
    "ℹ️ Not: Botu gruba ekleyip admin yap, VC aç, sonra /play kullan."
)


async def _bot_username():
    try:
        me = await app.get_me()
        return me.username
    except Exception:
        return None


@app.on_message(filters.command(["help"]) & filters.group)
async def help_group(_, message):
    uname = await _bot_username()
    if not uname:
        return await message.reply_text(
            "PM yardım menüsü için botu özelden başlat."
        )

    await message.reply_text(
        "📩 Yardım menüsünü özelden gönderdim / göndereceğim.\n"
        "Eğer gelmezse botu PM’de başlat.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💬 Yardımı Aç",
                        url=f"https://t.me/{uname}?start=help",
                    )
                ]
            ]
        ),
    )


@app.on_message(filters.command(["help", "start"]) & filters.private)
async def help_private(_, message):
    await message.reply_text(
        HELP_TEXT,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("➕ Gruba Ekle", url=f"https://t.me/{(await _bot_username())}?startgroup=true")]
            ]
        )
        if await _bot_username()
        else None,
    )
