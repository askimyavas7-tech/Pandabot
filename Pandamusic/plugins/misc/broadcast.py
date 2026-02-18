import asyncio

from pyrogram import filters
from pyrogram.types import Message

from Pandamusic import app


def _get_sudo_list():
    # projeye göre farklı isimlerde olabiliyor, hepsine fallback
    try:
        from Pandamusic.misc import SUDOERS
        return set(SUDOERS)
    except Exception:
        pass
    try:
        from config import SUDO_USERS
        # SUDO_USERS bazen list, bazen str olabilir
        if isinstance(SUDO_USERS, str):
            return set(int(x) for x in SUDO_USERS.split() if x.strip().isdigit())
        return set(SUDO_USERS)
    except Exception:
        return set()


def _is_sudo(user_id: int) -> bool:
    return int(user_id) in _get_sudo_list()


@app.on_message(filters.command(["broadcast"]) & filters.private)
async def broadcast_message(_, message: Message):
    if not message.from_user or not _is_sudo(message.from_user.id):
        return await message.reply_text("⛔ Bu komut sadece SUDO içindir.")

    if not message.reply_to_message:
        return await message.reply_text("Bir mesaja yanıt verip /broadcast yaz.")

    from Pandamusic.utils.database import get_served_chats  # mevcutsa kullan
    served_chats = await get_served_chats()

    x = message.reply_to_message
    done = 0
    failed = 0

    m = await message.reply_text("🔄 Broadcast başlıyor...")

    for chat in served_chats:
        cid = chat.get("chat_id") if isinstance(chat, dict) else chat
        try:
            await x.copy(cid)
            done += 1
            await asyncio.sleep(0.2)
        except Exception:
            failed += 1

    await m.edit_text(f"✅ Bitti!\n\n✅ Gönderildi: {done}\n❌ Hata: {failed}")


@app.on_message(filters.command(["ubroadcast"]) & filters.private)
async def user_broadcast(_, message: Message):
    if not message.from_user or not _is_sudo(message.from_user.id):
        return await message.reply_text("⛔ Bu komut sadece SUDO içindir.")

    if not message.reply_to_message:
        return await message.reply_text("Bir mesaja yanıt verip /ubroadcast yaz.")

    from Pandamusic.utils.database import get_served_users
    served_users = await get_served_users()

    x = message.reply_to_message
    done = 0
    failed = 0

    m = await message.reply_text("🔄 Kullanıcılara broadcast başlıyor...")

    for u in served_users:
        uid = u.get("user_id") if isinstance(u, dict) else u
        try:
            await x.copy(uid)
            done += 1
            await asyncio.sleep(0.2)
        except Exception:
            failed += 1

    await m.edit_text(f"✅ Bitti!\n\n✅ Gönderildi: {done}\n❌ Hata: {failed}")
