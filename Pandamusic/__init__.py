# Copyright (c) 2026 HAN THAR <HANTHAR999>
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


from Pandamusic.core.bot import Nand
from Pandamusic.core.dir import dirr
from Pandamusic.core.git import git
from Pandamusic.core.userbot import Userbot
from Pandamusic.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Nand()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()


# ©️ Copyright Reserved - @HANTHAR999 HAN THAR

# ===========================================
# ©️ 2026 HAN THAR
# 🔗 GitHub : https://github.com/tzkgaming2019-creator/Pandabot
# 📢 Telegram Channel : https://t.me/myanmarbot_music
# ===========================================


# ❤️ Love From myanmarbot_music 
