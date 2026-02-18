import os
from logging import getLogger

from unidecode import unidecode
from PIL import ImageDraw, Image, ImageFont, ImageChops

from pyrogram import filters, enums
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ChatMemberUpdated,
    Message,
)

from Pandamusic import app
from Pandamusic.core.mongo import mongodb

log = getLogger(__name__)

# ✅ Welcome collection
# bazı projelerde collection adı welcome / welcomes olabilir.
wlcm = getattr(mongodb, "welcome", None) or getattr(mongodb, "welcomes", None) or mongodb.welcome


class temp:
    MELCOW = {}


def circle(pfp, size=(450, 450)):
    pfp = pfp.resize(size, Image.LANCZOS).convert("RGBA")
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.LANCZOS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp


def welcomepic(pic, user, chat, uid, uname):
    background = Image.open("Pandamusic/assets/welcome.png").convert("RGBA")
    pfp = Image.open(pic).convert("RGBA")
    pfp = circle(pfp).resize((450, 450))

    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("Pandamusic/assets/font.ttf", size=45)

    draw.text((65, 250), f"NAME : {unidecode(str(user))}", fill="white", font=font)
    draw.text((65, 340), f"ID : {uid}", fill="white", font=font)
    draw.text(
        (65, 430),
        f"USERNAME : {('@' + uname) if uname else 'NOT SET'}",
        fill="white",
        font=font,
    )

    pfp_position = (767, 133)
    background.paste(pfp, pfp_position, pfp)

    os.makedirs("downloads", exist_ok=True)
    out = f"downloads/welcome#{uid}.png"
    background.save(out)
    return out


async def _bot_username():
    try:
        me = await app.get_me()
        return me.username
    except Exception:
        return None


@app.on_message(filters.command("welcome") & filters.group)
async def auto_state(_, message: Message):
    usage = "<b>❖ ᴜsᴀɢᴇ ➥</b> /welcome [on|off]"
    if len(message.command) == 1:
        return await message.reply_text(usage)

    chat_id = message.chat.id
    try:
        member = await app.get_chat_member(chat_id, message.from_user.id)
    except Exception:
        return await message.reply_text("✦ Yetki kontrolü yapılamadı.")

    if member.status not in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
        return await message.reply_text("✦ Only Admins Can Use This Command")

    state = message.text.split(None, 1)[1].strip().lower()
    A = await wlcm.find_one({"chat_id": chat_id})

    if state == "on":
        if A and not A.get("disabled", False):
            return await message.reply_text("✦ Special Welcome Already Enabled")
        await wlcm.update_one({"chat_id": chat_id}, {"$set": {"disabled": False}}, upsert=True)
        return await message.reply_text(f"✦ Enabled Special Welcome in {message.chat.title}")

    if state == "off":
        if A and A.get("disabled", False):
            return await message.reply_text("✦ Special Welcome Already Disabled")
        await wlcm.update_one({"chat_id": chat_id}, {"$set": {"disabled": True}}, upsert=True)
        return await message.reply_text(f"✦ Disabled Special Welcome in {message.chat.title}")

    return await message.reply_text(usage)


@app.on_chat_member_updated(filters.group, group=-3)
async def greet_group(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
    A = await wlcm.find_one({"chat_id": chat_id})
    if A and A.get("disabled", False):
        return

    if not member.new_chat_member:
        return
    if member.new_chat_member.status in {"banned", "left", "restricted"}:
        return

    user = member.new_chat_member.user

    key = f"welcome-{chat_id}"
    if temp.MELCOW.get(key) is not None:
        try:
            await temp.MELCOW[key].delete()
        except Exception:
            pass

    pic_path = None
    try:
        if user.photo:
            pic_path = await app.download_media(
                user.photo.big_file_id, file_name=f"downloads/pp{user.id}.png"
            )
    except Exception:
        pic_path = None

    if not pic_path:
        pic_path = "Pandamusic/assets/upic.png"

    try:
        welcomeimg = welcomepic(
            pic_path,
            user.first_name or "User",
            member.chat.title or "Group",
            user.id,
            user.username,
        )
    except Exception as e:
        log.error(e)
        welcomeimg = None

    bot_username = await _bot_username()
    add_btn = (
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🎵 ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ 🎵",
                        url=f"https://t.me/{bot_username}?startgroup=True",
                    )
                ]
            ]
        )
        if bot_username
        else None
    )

    caption = f"""🌟 <b>ᴡᴇʟᴄᴏᴍᴇ {user.mention}!</b>

📋 <b>ɢʀᴏᴜᴘ:</b> {member.chat.title}
🆔 <b>ʏᴏᴜʀ ɪᴅ:</b> <code>{user.id}</code>
👤 <b>ᴜsᴇʀɴᴀᴍᴇ:</b> @{user.username if user.username else "ɴᴏᴛ sᴇᴛ"}"""

    try:
        if welcomeimg:
            temp.MELCOW[key] = await app.send_photo(
                chat_id,
                photo=welcomeimg,
                caption=caption,
                reply_markup=add_btn,
            )
        else:
            temp.MELCOW[key] = await app.send_message(
                chat_id,
                text=caption,
                reply_markup=add_btn,
            )
    except Exception as e:
        log.error(e)

    try:
        if welcomeimg and os.path.exists(welcomeimg):
            os.remove(welcomeimg)
        if pic_path and pic_path.startswith("downloads/") and os.path.exists(pic_path):
            os.remove(pic_path)
    except Exception:
        pass
