import importlib
import re
import time
from platform import python_version as y
from sys import argv
import random
from pyrogram import version as pyrover
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update, InputMediaPhoto
from telegram import version as telever
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop
from telegram.utils.helpers import escape_markdown
from telethon import version as tlhver

import DazaiRobot.modules.sql.users_sql as sql
from DazaiRobot import (
    BOT_NAME,
    BOT_USERNAME,
    LOGGER,
    OWNER_ID,
    START_IMG,
    SUPPORT_CHAT,
    TOKEN,
    StartTime,
    dispatcher,
    pbot,
    telethn,
    updater,
)
from DazaiRobot.modules import ALL_MODULES
from DazaiRobot.modules.helper_funcs.chat_status import is_user_admin
from DazaiRobot.modules.helper_funcs.misc import paginate_modules

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

import random

# List of video URLs
pm_start_texts = [
    
"ʜᴇʏ, ɪ’ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ⚡\nㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n ㋡ ʜɪ, ɪ'ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ᴛʜᴇ ʙᴏᴛ ᴛʜᴀᴛ's ғᴀsᴛᴇʀ ᴛʜᴀɴ ᴀ sᴘᴇᴇᴅɪɴɢ ʙᴜʟʟᴇᴛ ᴀɴᴅ sᴍᴏᴏᴛʜᴇʀ ᴛʜᴀɴ Jᴀᴢᴢ.\n                               \n‣ ɪ ʜᴀᴠᴇ ᴍᴀɴʏ ғᴇᴀᴛᴜʀᴇs ᴍᴜsɪᴄ? ɴᴏ ᴘʀᴏʙʟᴇᴍ. ᴍᴀɴᴀɢᴇᴍᴇɴᴛ? ᴘɪᴇᴄᴇ ᴏғ ᴄᴀᴋᴇ. ʟᴀɢ? ɴᴏᴛ ᴏɴ ᴍʏ ᴡᴀᴛᴄʜ!ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n ◉ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ 「 Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ 」 ғᴇᴀᴛᴜʀᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs+ [ㅤ](https://files.catbox.moe/yeoh6e.mp4)",
    
"ʜᴇʏ, ɪ’ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ⚡\nㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n ㋡ ʜɪ, ɪ'ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ᴛʜᴇ ʙᴏᴛ ᴛʜᴀᴛ's ғᴀsᴛᴇʀ ᴛʜᴀɴ ᴀ sᴘᴇᴇᴅɪɴɢ ʙᴜʟʟᴇᴛ ᴀɴᴅ sᴍᴏᴏᴛʜᴇʀ ᴛʜᴀɴ Jᴀᴢᴢ.\n                               \n‣ ɪ ʜᴀᴠᴇ ᴍᴀɴʏ ғᴇᴀᴛᴜʀᴇs ᴍᴜsɪᴄ? ɴᴏ ᴘʀᴏʙʟᴇᴍ. ᴍᴀɴᴀɢᴇᴍᴇɴᴛ? ᴘɪᴇᴄᴇ ᴏғ ᴄᴀᴋᴇ. ʟᴀɢ? ɴᴏᴛ ᴏɴ ᴍʏ ᴡᴀᴛᴄʜ!ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n ◉ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ 「 Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ 」 ғᴇᴀᴛᴜʀᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs+ [ㅤ](https://files.catbox.moe/yeoh6e.mp4)",
    
"ʜᴇʏ, ɪ’ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ⚡\nㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n ㋡ ʜɪ, ɪ'ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ᴛʜᴇ ʙᴏᴛ ᴛʜᴀᴛ's ғᴀsᴛᴇʀ ᴛʜᴀɴ ᴀ sᴘᴇᴇᴅɪɴɢ ʙᴜʟʟᴇᴛ ᴀɴᴅ sᴍᴏᴏᴛʜᴇʀ ᴛʜᴀɴ Jᴀᴢᴢ.\n                               \n‣ ɪ ʜᴀᴠᴇ ᴍᴀɴʏ ғᴇᴀᴛᴜʀᴇs ᴍᴜsɪᴄ? ɴᴏ ᴘʀᴏʙʟᴇᴍ. ᴍᴀɴᴀɢᴇᴍᴇɴᴛ? ᴘɪᴇᴄᴇ ᴏғ ᴄᴀᴋᴇ. ʟᴀɢ? ɴᴏᴛ ᴏɴ ᴍʏ ᴡᴀᴛᴄʜ!ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n ◉ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ 「 Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ 」 ғᴇᴀᴛᴜʀᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs+ [ㅤ](https://files.catbox.moe/yeoh6e.mp4)",
    
"ʜᴇʏ, ɪ’ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ⚡\nㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n ㋡ ʜɪ, ɪ'ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ᴛʜᴇ ʙᴏᴛ ᴛʜᴀᴛ's ғᴀsᴛᴇʀ ᴛʜᴀɴ ᴀ sᴘᴇᴇᴅɪɴɢ ʙᴜʟʟᴇᴛ ᴀɴᴅ sᴍᴏᴏᴛʜᴇʀ ᴛʜᴀɴ Jᴀᴢᴢ.\n                               \n‣ ɪ ʜᴀᴠᴇ ᴍᴀɴʏ ғᴇᴀᴛᴜʀᴇs ᴍᴜsɪᴄ? ɴᴏ ᴘʀᴏʙʟᴇᴍ. ᴍᴀɴᴀɢᴇᴍᴇɴᴛ? ᴘɪᴇᴄᴇ ᴏғ ᴄᴀᴋᴇ. ʟᴀɢ? ɴᴏᴛ ᴏɴ ᴍʏ ᴡᴀᴛᴄʜ!ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n ◉ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ 「 Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ 」 ғᴇᴀᴛᴜʀᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs+ [ㅤ](https://files.catbox.moe/yeoh6e.mp4)",
    
"ʜᴇʏ, ɪ’ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ⚡\nㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n ㋡ ʜɪ, ɪ'ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ᴛʜᴇ ʙᴏᴛ ᴛʜᴀᴛ's ғᴀsᴛᴇʀ ᴛʜᴀɴ ᴀ sᴘᴇᴇᴅɪɴɢ ʙᴜʟʟᴇᴛ ᴀɴᴅ sᴍᴏᴏᴛʜᴇʀ ᴛʜᴀɴ Jᴀᴢᴢ.\n                               \n‣ ɪ ʜᴀᴠᴇ ᴍᴀɴʏ ғᴇᴀᴛᴜʀᴇs ᴍᴜsɪᴄ? ɴᴏ ᴘʀᴏʙʟᴇᴍ. ᴍᴀɴᴀɢᴇᴍᴇɴᴛ? ᴘɪᴇᴄᴇ ᴏғ ᴄᴀᴋᴇ. ʟᴀɢ? ɴᴏᴛ ᴏɴ ᴍʏ ᴡᴀᴛᴄʜ!ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n ◉ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ 「 Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ 」 ғᴇᴀᴛᴜʀᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs+ [ㅤ](https://files.catbox.moe/yeoh6e.mp4)",

"ʜᴇʏ, ɪ’ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ⚡\nㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n ㋡ ʜɪ, ɪ'ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ᴛʜᴇ ʙᴏᴛ ᴛʜᴀᴛ's ғᴀsᴛᴇʀ ᴛʜᴀɴ ᴀ sᴘᴇᴇᴅɪɴɢ ʙᴜʟʟᴇᴛ ᴀɴᴅ sᴍᴏᴏᴛʜᴇʀ ᴛʜᴀɴ Jᴀᴢᴢ.\n                               \n‣ ɪ ʜᴀᴠᴇ ᴍᴀɴʏ ғᴇᴀᴛᴜʀᴇs ᴍᴜsɪᴄ? ɴᴏ ᴘʀᴏʙʟᴇᴍ. ᴍᴀɴᴀɢᴇᴍᴇɴᴛ? ᴘɪᴇᴄᴇ ᴏғ ᴄᴀᴋᴇ. ʟᴀɢ? ɴᴏᴛ ᴏɴ ᴍʏ ᴡᴀᴛᴄʜ!ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n ◉ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ 「 Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ 」 ғᴇᴀᴛᴜʀᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs+ [ㅤ](https://files.catbox.moe/yeoh6e.mp4)",
    
"ʜᴇʏ, ɪ’ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ⚡\nㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n ㋡ ʜɪ, ɪ'ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ᴛʜᴇ ʙᴏᴛ ᴛʜᴀᴛ's ғᴀsᴛᴇʀ ᴛʜᴀɴ ᴀ sᴘᴇᴇᴅɪɴɢ ʙᴜʟʟᴇᴛ ᴀɴᴅ sᴍᴏᴏᴛʜᴇʀ ᴛʜᴀɴ Jᴀᴢᴢ.\n                               \n‣ ɪ ʜᴀᴠᴇ ᴍᴀɴʏ ғᴇᴀᴛᴜʀᴇs ᴍᴜsɪᴄ? ɴᴏ ᴘʀᴏʙʟᴇᴍ. ᴍᴀɴᴀɢᴇᴍᴇɴᴛ? ᴘɪᴇᴄᴇ ᴏғ ᴄᴀᴋᴇ. ʟᴀɢ? ɴᴏᴛ ᴏɴ ᴍʏ ᴡᴀᴛᴄʜ!ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n ◉ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ 「 Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ 」 ғᴇᴀᴛᴜʀᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs+ [ㅤ](https://files.catbox.moe/yeoh6e.mp4)",
    
"ʜᴇʏ, ɪ’ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ⚡\nㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n ㋡ ʜɪ, ɪ'ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ᴛʜᴇ ʙᴏᴛ ᴛʜᴀᴛ's ғᴀsᴛᴇʀ ᴛʜᴀɴ ᴀ sᴘᴇᴇᴅɪɴɢ ʙᴜʟʟᴇᴛ ᴀɴᴅ sᴍᴏᴏᴛʜᴇʀ ᴛʜᴀɴ Jᴀᴢᴢ.\n                               \n‣ ɪ ʜᴀᴠᴇ ᴍᴀɴʏ ғᴇᴀᴛᴜʀᴇs ᴍᴜsɪᴄ? ɴᴏ ᴘʀᴏʙʟᴇᴍ. ᴍᴀɴᴀɢᴇᴍᴇɴᴛ? ᴘɪᴇᴄᴇ ᴏғ ᴄᴀᴋᴇ. ʟᴀɢ? ɴᴏᴛ ᴏɴ ᴍʏ ᴡᴀᴛᴄʜ!ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n ◉ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ 「 Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ 」 ғᴇᴀᴛᴜʀᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs+ [ㅤ](https://files.catbox.moe/yeoh6e.mp4)",
    
"ʜᴇʏ, ɪ’ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ⚡\nㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n ㋡ ʜɪ, ɪ'ᴍ Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ! ᴛʜᴇ ʙᴏᴛ ᴛʜᴀᴛ's ғᴀsᴛᴇʀ ᴛʜᴀɴ ᴀ sᴘᴇᴇᴅɪɴɢ ʙᴜʟʟᴇᴛ ᴀɴᴅ sᴍᴏᴏᴛʜᴇʀ ᴛʜᴀɴ Jᴀᴢᴢ.\n                               \n‣ ɪ ʜᴀᴠᴇ ᴍᴀɴʏ ғᴇᴀᴛᴜʀᴇs ᴍᴜsɪᴄ? ɴᴏ ᴘʀᴏʙʟᴇᴍ. ᴍᴀɴᴀɢᴇᴍᴇɴᴛ? ᴘɪᴇᴄᴇ ᴏғ ᴄᴀᴋᴇ. ʟᴀɢ? ɴᴏᴛ ᴏɴ ᴍʏ ᴡᴀᴛᴄʜ!ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n ◉ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ 「 Ꮐᴏᴊᴏ ꕶᴀᴛᴏʀᴜ 」 ғᴇᴀᴛᴜʀᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs+ [ㅤ](https://files.catbox.moe/yeoh6e.mp4)",
    
 ]
 
START_TEXT  = random.choice(pm_start_texts)

# PM start text with the selected video link


NEXT_PHT = [
"https://files.catbox.moe/zp1nve.jpg", 
"https://files.catbox.moe/dwxv2v.jpg", 
"https://telegra.ph/file/fa572b60698cb9017cc59.jpg", 
"https://telegra.ph/file/0693ad8ba218cd8727c4a.jpg" , 
"https://files.catbox.moe/zp1nve.jpg", 
"https://files.catbox.moe/vh0ppc.jpg",
"https://telegra.ph/file/63ac376c0376956b2d8e4.jpg", 
"https://files.catbox.moe/dwxv2v.jpg", 
"https://telegra.ph/file/fa572b60698cb9017cc59.jpg", 
"https://files.catbox.moe/dwxv2v.jpg", 
"https://files.catbox.moe/dwxv2v.jpg", 
"https://files.catbox.moe/vh0ppc.jpg", 
"https://telegra.ph/file/63ac376c0376956b2d8e4.jpg", 
"https://telegra.ph/file/fa572b60698cb9017cc59.jpg", 
]

NEXT_PHT2 = [
"https://files.catbox.moe/vh0ppc.jpg", 
"https://telegra.ph/file/63ac376c0376956b2d8e4.jpg", 
"https://files.catbox.moe/dwxv2v.jpg", 
"https://telegra.ph/file/fa572b60698cb9017cc59.jpg", 
"https://files.catbox.moe/vh0ppc.jpg", 
"https://files.catbox.moe/dwxv2v.jpg", 
"https://telegra.ph/file/b8719b281572b48d0b74e.jpg", 
"https://files.catbox.moe/dwxv2v.jpg", 
]


buttons = [

    [
        InlineKeyboardButton(
            text="⚡️ ᴀᴅᴅ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ⚡️", 
            url=f"https://t.me/GojoAiBot?startgroup=true", 
        ),
    ],
    [
        InlineKeyboardButton(text="✨ ᴜᴘᴅᴀᴛᴇs ✨", url=f"https://t.me/TheGojoSupport"),
        InlineKeyboardButton(text="🫧 sᴜᴘᴘᴏʀᴛ 🫧", url=f"https://t.me/Nirvox"),
    ],
    [
        InlineKeyboardButton(text="🎵 ᴍᴜsɪᴄ 🎶", callback_data="dazai_"),
        InlineKeyboardButton(text="⚔ ɴᴇᴛᴡᴏʀᴋ ⚔", url=f"https://t.me/OgApexMainchat"),
    ],
    [
        InlineKeyboardButton(text="🛠️ ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs ⚙️", callback_data="help_back"),
    ],

]

startbutton = [
        
    [
        InlineKeyboardButton(text="sᴜᴩᴩᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
        
    ],
]

HELP_STRINGS = f"""
{BOT_NAME} Exclusive Features
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
➲ /start: Kick off the bot. (You’ve already got this!)

➲ /help: Check out all commands.
‣ Private Message: Detailed help for every module.
‣ Group: Redirects you to a private message for full support.
➲ For clone Commands Press /reacthelp and /chathelp
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
"""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("DazaiRobot.modules." + module_name)
    if not hasattr(imported_module, "mod_name"):
        imported_module.mod_name = imported_module.name

    if imported_module.mod_name.lower() not in IMPORTED:
        IMPORTED[imported_module.mod_name.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "help") and imported_module.help:
        HELPABLE[imported_module.mod_name.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "migrate"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "stats"):
        STATS.append(imported_module)

    if hasattr(imported_module, "user_info"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "import_data"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "export_data"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "chat_settings"):
        CHAT_SETTINGS[imported_module.mod_name.lower()] = imported_module

    if hasattr(imported_module, "user_settings"):
        USER_SETTINGS[imported_module.mod_name.lower()] = imported_module


# do not async
import random
from telegram import InlineKeyboardMarkup, ParseMode

def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    
    NEXT_PHT = [
        "https://files.catbox.moe/vh0ppc.jpg", 
        "https://telegra.ph/file/b8719b281572b48d0b74e.jpg", 
        "https://telegra.ph/file/63ac376c0376956b2d8e4.jpg", 
        "https://telegra.ph/file/63ac376c0376956b2d8e4.jpg", 
        "https://files.catbox.moe/vh0ppc.jpg", 
        "https://telegra.ph/file/63ac376c0376956b2d8e4.jpg",
        "https://telegra.ph/file/b8719b281572b48d0b74e.jpg", 
        "https://files.catbox.moe/vh0ppc.jpg", 
        "https://files.catbox.moe/vh0ppc.jpg", 
        "https://telegra.ph/file/b8719b281572b48d0b74e.jpg", 
        "https://files.catbox.moe/dwxv2v.jpg", 
        "https://files.catbox.moe/vh0ppc.jpg", 
        "https://telegra.ph/file/63ac376c0376956b2d8e4.jpg", 
        "https://files.catbox.moe/vh0ppc.jpg", 
    ]

    # Send a random photo from the list
    photo_url = random.choice(NEXT_PHT)
    dispatcher.bot.send_photo(
        chat_id=chat_id,
        photo=photo_url,
        caption=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard
    )



import random
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext

# Example list of stickers
stickers = [
    "CAACAgQAAyEFAASFNi5HAAIM7Gdta9nwnEnCErwtBIxBh_O_l14cAAIaDwACTUpRUOcjBCAu4kdjNgQ",
    "CAACAgQAAyEFAASFNi5HAAIM7Wdta9rk6eIMP18_oJXZzVP2ahd7AAKADQACGZ5RUFo1A_BOgrGfNgQ",
    "CAACAgQAAyEFAASFNi5HAAIM7Gdta9nwnEnCErwtBIxBh_O_l14cAAIaDwACTUpRUOcjBCAu4kdjNgQ",
]

# Assuming NEXI_VID, PM_START_TEXT, buttons, startbutton, NEXT_PHT2 are already defined elsewhere

import time

def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))  # Assuming StartTime is defined
    
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            # Handle various commands here
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,

HELPABLE[mod].help,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="◁", callback_data="help_back")]]
                    ),
                )
            elif args[0].lower() == "markdownhelp":
                IMPORTED["exᴛʀᴀs"].markdown_help_sender(update)
            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))
                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)
            elif args[0][1:].isdigit() and "rᴜʟᴇs" in IMPORTED:
                IMPORTED["rᴜʟᴇs"].send_rules(update, args[0], from_pm=True)

        else:
            # Send a random sticker
            sticker_msg = update.effective_message.reply_sticker(
                random.choice(stickers),
                timeout=60
            )

            # Wait for 1 second
            time.sleep(1)

            # Delete the sent sticker message
            sticker_msg.delete()

            # Then send the video
            update.effective_message.reply_text(
            START_TEXT, 
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            )
    else:
        update.effective_message.reply_photo(
            random.choice(NEXT_PHT2),
            caption=" ᴛʜᴀɴᴋs ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ᴛᴏ ᴛʜɪs ɢʀᴏᴜᴘ!\n"
                "<b>⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯</b>\n"
                "<b>ɪ ᴅɪᴅɴ'ᴛ sʟᴇᴘᴛ sɪɴᴄᴇ:</b> <code>{}</code>\n"
                "<b> ʙᴜᴛ ᴅᴏɴ’ᴛ ᴡᴏʀʀʏ, ɪ’ᴍ ᴀʟᴡᴀʏs ʜᴇʀᴇ ᴛᴏ ʜᴇʟᴘ ᴋᴇᴇᴘ ᴛʜɪɴɢs ʀᴜɴɴɪɴɢ sᴍᴏᴏᴛʜʟʏ!</b>".format(uptime),
            reply_markup=InlineKeyboardMarkup(startbutton),
            parse_mode=ParseMode.HTML,
            )


def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.traceback
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors

def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "» *ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ* *{}* :\n".format(
                    HELPABLE[module].mod_name
                )
                + HELPABLE[module].help
            )
            query.message.edit_media(
            media=InputMediaPhoto(
                random.choice(NEXT_PHT),
                caption=text,
                parse_mode=ParseMode.MARKDOWN,
         ),
                #disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="◁", callback_data="help_back")]]
                ),
            )
    
        
        elif prev_match:
           curr_page = int(prev_match.group(1))
           query.message.edit_media(
           media=InputMediaPhoto(
              random.choice(NEXT_PHT),
              caption=HELP_STRINGS,
              parse_mode=ParseMode.MARKDOWN,
        ),
             reply_markup=InlineKeyboardMarkup(
                 paginate_modules(curr_page - 1, HELPABLE, "help")
        ), 
    )
    

        elif next_match:
           next_page = int(next_match.group(1))
           query.message.edit_media(
           media=InputMediaPhoto(
              random.choice(NEXT_PHT),
              caption=HELP_STRINGS,
              parse_mode=ParseMode.MARKDOWN,
        ),
              reply_markup=InlineKeyboardMarkup(
                 paginate_modules(next_page + 1, HELPABLE, "help")
        ), 
    )

        elif back_match:
           query.message.edit_media(
           media=InputMediaPhoto(
              random.choice(NEXT_PHT),
              caption=HELP_STRINGS,
              parse_mode=ParseMode.MARKDOWN,
        ),
             reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help")
        ), 
    )

        context.bot.answer_callback_query(query.id)

    except BadRequest:
        pass

def Dazai_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "dazai_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text(
            text=f"*ʜᴇʏ,*🥀\n  *ᴛʜɪs ɪs {BOT_NAME}*"
            "\n*ᴀ ᴘᴏᴡᴇʀꜰᴜʟ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ʙᴜɪʟᴛ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴇᴀꜱɪʟʏ ᴀɴᴅ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ ʏᴏᴜʀ ɢʀᴏᴜᴘ ꜰʀᴏᴍ ꜱᴄᴀᴍᴍᴇʀꜱ ᴀɴᴅ ꜱᴘᴀᴍᴍᴇʀꜱ.*"
            "\n*ᴡʀɪᴛᴛᴇɴ ɪɴ ᴩʏᴛʜᴏɴ ᴡɪᴛʜ sǫʟᴀʟᴄʜᴇᴍʏ ᴀɴᴅ ᴍᴏɴɢᴏᴅʙ ᴀs ᴅᴀᴛᴀʙᴀsᴇ.*"
            "\n\n────────────────────"
            f"\n*➻ ᴜᴩᴛɪᴍᴇ »* {uptime}"
            f"\n*➻ ᴜsᴇʀs »* {sql.num_users()}"
            f"\n*➻ ᴄʜᴀᴛs »* {sql.num_chats()}"
            "\n────────────────────"
            "\n\n➲  ɪ ᴄᴀɴ ʀᴇꜱᴛʀɪᴄᴛ ᴜꜱᴇʀꜱ."
            "\n➲  ɪ ʜᴀᴠᴇ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴᴛɪ-ꜰʟᴏᴏᴅ ꜱʏꜱᴛᴇᴍ."
            "\n➲  ɪ ᴄᴀɴ ɢʀᴇᴇᴛ ᴜꜱᴇʀꜱ ᴡɪᴛʜ ᴄᴜꜱᴛᴏᴍɪᴢᴀʙʟᴇ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇꜱꜱᴀɢᴇꜱ ᴀɴᴅ ᴇᴠᴇɴ ꜱᴇᴛ ᴀ ɢʀᴏᴜᴘ'ꜱ ʀᴜʟᴇꜱ."
            "\n➲  ɪ ᴄᴀɴ ᴡᴀʀɴ ᴜꜱᴇʀꜱ ᴜɴᴛɪʟ ᴛʜᴇʏ ʀᴇᴀᴄʜ ᴍᴀx ᴡᴀʀɴꜱ, ᴡɪᴛʜ ᴇᴀᴄʜ ᴘʀᴇᴅᴇꜰɪɴᴇᴅ ᴀᴄᴛɪᴏɴꜱ ꜱᴜᴄʜ ᴀꜱ ʙᴀɴ, ᴍᴜᴛᴇ, ᴋɪᴄᴋ, ᴇᴛᴄ."
            "\n➲  ɪ ʜᴀᴠᴇ ᴀ ɴᴏᴛᴇ ᴋᴇᴇᴘɪɴɢ ꜱʏꜱᴛᴇᴍ, ʙʟᴀᴄᴋʟɪꜱᴛꜱ, ᴀɴᴅ ᴇᴠᴇɴ ᴘʀᴇᴅᴇᴛᴇʀᴍɪɴᴇᴅ ʀᴇᴘʟɪᴇꜱ ᴏɴ ᴄᴇʀᴛᴀɪɴ ᴋᴇʏᴡᴏʀᴅꜱ."
            f"\n\n➻ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ғᴏʀ ɢᴇᴛᴛɪɴɢ ʙᴀsɪᴄ ʜᴇʟᴩ ᴀɴᴅ ɪɴғᴏ ᴀʙᴏᴜᴛ {BOT_NAME}.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="sᴜᴩᴩᴏʀᴛ", callback_data="zxbbzxce"

),
                        InlineKeyboardButton(
                            text="ᴄᴏᴍᴍᴀɴᴅs", callback_data="help_back"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="ᴅᴇᴠᴇʟᴏᴩᴇʀ", url=f"tg://user?id={OWNER_ID}"
                        ),
                        InlineKeyboardButton(
                            text="sᴏᴜʀᴄᴇ",
                            callback_data="source_",
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="◁", callback_data="dazai_back"),
                    ],
                ]
            ),
        )
    elif query.data == "dazai_support":
        query.message.edit_text(
            text="*๏ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ʜᴇʟᴩ ᴀɴᴅ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴍᴇ.*"
            f"\n\nɪғ ʏᴏᴜ ғᴏᴜɴᴅ ᴀɴʏ ʙᴜɢ ɪɴ {BOT_NAME} ᴏʀ ɪғ ʏᴏᴜ ᴡᴀɴɴᴀ ɢɪᴠᴇ ғᴇᴇᴅʙᴀᴄᴋ ᴀʙᴏᴜᴛ ᴛʜᴇ {BOT_NAME}, ᴩʟᴇᴀsᴇ ʀᴇᴩᴏʀᴛ ɪᴛ ᴀᴛ sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="sᴜᴩᴩᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"
                        ),
                        InlineKeyboardButton(
                            text="ᴜᴩᴅᴀᴛᴇs", url=f"https://t.me/APEX_X_NETWORK"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="ᴅᴇᴠᴇʟᴏᴩᴇʀ", url=f"tg://user?id={OWNER_ID}"
                        ),
                        InlineKeyboardButton(
                            text="ɢɪᴛʜᴜʙ",
                            url="https://te.legra.ph/file/7b2a7b25395862954ae1c.mp4",
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="◁", callback_data="dazai_"),
                    ],
                ]
            ),
        )
    elif query.data == "dazai_back":
        first_name = update.effective_user.first_name
        query.message.edit_text(
            PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME, escape_markdown(uptime)),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=True,
        )


def Source_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "source_":
        query.message.edit_text(
            text=f"""
*ʜᴇʏ,
 ᴛʜɪs ɪs {BOT_NAME},
ᴀɴ ᴏᴩᴇɴ sᴏᴜʀᴄᴇ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴩ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ.*

ᴡʀɪᴛᴛᴇɴ ɪɴ ᴩʏᴛʜᴏɴ ᴡɪᴛʜ ᴛʜᴇ ʜᴇʟᴩ ᴏғ : [ᴛᴇʟᴇᴛʜᴏɴ](https://github.com/LonamiWebs/Telethon)
[ᴩʏʀᴏɢʀᴀᴍ](https://github.com/pyrogram/pyrogram)
[ᴩʏᴛʜᴏɴ-ᴛᴇʟᴇɢʀᴀᴍ-ʙᴏᴛ](https://github.com/python-telegram-bot/python-telegram-bot)
ᴀɴᴅ ᴜsɪɴɢ [sǫʟᴀʟᴄʜᴇᴍʏ](https://www.sqlalchemy.org) ᴀɴᴅ [ᴍᴏɴɢᴏ](https://cloud.mongodb.com) ᴀs ᴅᴀᴛᴀʙᴀsᴇ.


*ʜᴇʀᴇ ɪs ᴍʏ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ :* [ɢɪᴛʜᴜʙ](https://te.legra.ph/file/7b2a7b25395862954ae1c.mp4)


{BOT_NAME} ɪs ʟɪᴄᴇɴsᴇᴅ ᴜɴᴅᴇʀ ᴛʜᴇ [ᴍɪᴛ ʟɪᴄᴇɴsᴇ](https://github.com/adi6804/DazaiRobot/blob/main/LICENSE).
© 2022 - 2023 | [sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ](https://t.me/{SUPPORT_CHAT}), ᴀʟʟ ʀɪɢʜᴛs ʀᴇsᴇʀᴠᴇᴅ.
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="◁", callback_data="source_back")]]
            ),
        )
    elif query.data == "source_back":
        first_name = update.effective_user.first_name
        query.message.edit_text(
            PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME, escape_markdown(uptime)),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=True,
        )

def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_text(
                f"Contact me in PM to get help for {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="ʜᴇʟᴘ",
                                url=f"https://t.me/{context.bot.username}?start=ghelp_{module}",
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_text(
            "[»](https://files.catbox.moe/vh0ppc.jpg) ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴏᴘᴇɴ ᴀʟʟ ᴍʏ ᴍᴀɴᴀɢᴍᴇɴᴛ ᴍᴏᴅᴜʟᴇs sᴏ ʏᴏᴜ ᴄᴀɴ ᴋɴᴏᴡ ᴀʙᴏᴜᴛ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs ᴍᴏʀᴇ.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ᴏᴩᴇɴ ʜᴇʀᴇ",
                            callback_data="help_back",
                        )
                    ],
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].mod_name
            )
            + HELPABLE[module].help
        )
        send_help(
            chat.id,
            photo_url,
            text, 
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="◁", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)



def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.mod_name, mod.user_settings(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Which module would you like to check {}'s settings for?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any chat settings available :'(\nSend this "
                "in a group chat you're admin in to find its current settings!",
                parse_mode=ParseMode.MARKDOWN,
            )


def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)

back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].mod_name
            ) + CHAT_SETTINGS[module].chat_settings(chat_id, user.id)
            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="◁",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                text="Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "Message is not modified",
            "Query_id_invalid",
            "Message can't be deleted",
        ]:
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))

            


def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "Click here to get this chat's settings, as well as yours."
            msg.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="sᴇᴛᴛɪɴɢs",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "Click here to check your settings."

    else:
        send_settings(chat.id, user.id, True)

def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.migrate(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop

LOG_GROUP = "chocoXsupport"
def main():
    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.send_photo(
                chat_id=f"@{LOG_GROUP}",
                photo=START_IMG,
                caption=f"""
Lᴏᴠᴇ ɪs ᴛʜᴇ ᴍᴏsᴛ ᴘᴏᴡᴇʀғᴜʟ ᴇᴍᴏᴛɪᴏɴ, ᴀɴᴅ ɪᴛ ᴄᴀɴ ᴜɴʟᴇᴀsʜ ɪɴᴄʀᴇᴅɪʙʟᴇ sᴛʀᴇɴɢᴛʜ ᴡɪᴛʜɪɴ ᴜs.""",
                parse_mode=ParseMode.MARKDOWN,
            )
        except Unauthorized:
            LOGGER.warning(
                f"Bot isn't able to send message to @{LOG_GROUP}, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)

    start_handler = CommandHandler("start", start, run_async=True)

    help_handler = CommandHandler("help", get_help, run_async=True)
    help_callback_handler = CallbackQueryHandler(
        help_button, pattern=r"help_.*", run_async=True
    )

    settings_handler = CommandHandler("settings", get_settings, run_async=True)
    settings_callback_handler = CallbackQueryHandler(
        settings_button, pattern=r"stngs_", run_async=True
    )


    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_error_handler(error_callback)

    LOGGER.info("Using long polling.")
    updater.start_polling(timeout=15, read_latency=4, drop_pending_updates=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if name == "main":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    pbot.start()
    main()
