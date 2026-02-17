# Copyright (c) 2026 HANTHAR
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


import glob
from os.path import dirname, isfile


def __list_all_modules():
    work_dir = dirname(__file__)
    mod_paths = glob.glob(work_dir + "/*/*.py")

    all_modules = [
        (((f.replace(work_dir, "")).replace("/", "."))[:-3])
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]

    return all_modules


ALL_MODULES = sorted(__list_all_modules())
__all__ = ALL_MODULES + ["ALL_MODULES"]


# ©️ Copyright Reserved - @HANTHAR999 HAN THAR

# ===========================================
# ©️ 2026 HAN THAR
# 🔗 GitHub : https://github.com/tzkgaming2019-creator/Pandabot
# 📢 Telegram Channel : https://t.me/myanmarbot_music
# ===========================================


# ❤️ Love From  myanmarbot_music
