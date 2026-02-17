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

from __future__ import annotations

# --- logging ---
from .logging import LOGGER

# --- core imports ---
from Pandamusic.core.bot import Nand
from Pandamusic.core.userbot import Userbot

# --- startup helpers (safe) ---
from Pandamusic.core.dir import dirr
from Pandamusic.core.git import git
from Pandamusic.misc import dbb, heroku


def _safe_bootstrap():
    """
    Bu fonksiyonlar import anında patlarsa bot hiç açılmaz.
    O yüzden hepsini safe çalıştırıyoruz.
    """
    for fn, name in [
        (dirr, "dirr"),
        (git, "git"),
        (dbb, "dbb"),
        (heroku, "heroku"),
    ]:
        try:
            fn()
        except Exception as e:
            # Logla ama botu öldürme
            try:
                LOGGER("Pandamusic").warning(f"Bootstrap {name} skipped: {e}")
            except Exception:
                # LOGGER fonksiyon değilse diye ekstra koruma
                pass


_safe_bootstrap()

# --- create clients ---
app = Nand()
userbot = Userbot()

# --- platforms: explicit import (no star import) ---
try:
    from .platforms import (
        AppleAPI,
        CarbonAPI,
        SoundAPI,
        SpotifyAPI,
        RessoAPI,
        TeleAPI,
        YouTubeAPI,
    )

    Apple = AppleAPI()
    Carbon = CarbonAPI()
    SoundCloud = SoundAPI()
    Spotify = SpotifyAPI()
    Resso = RessoAPI()
    Telegram = TeleAPI()
    YouTube = YouTubeAPI()

except Exception as e:
    # Platformlar opsiyonel olsun; yoksa bot yine de açılabilsin
    try:
        LOGGER("Pandamusic").warning(f"Platforms not loaded: {e}")
    except Exception:
        pass

    Apple = None
    Carbon = None
    SoundCloud = None
    Spotify = None
    Resso = None
    Telegram = None
    YouTube = None
