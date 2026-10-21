import asyncio
import os

import requests
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import Config

ABS = "Developer"
OWNER = "Owner"
GITCLONE = "https://github.com/albin575/song-bot"
B2 = "https://telegram.dog/AB_Mediaw"
BUTTON1 = "📜 Source Code 📜"

# Telegram's audio player only accepts these containers; anything else
# (e.g. opus inside .webm) is sent as a document instead.
AUDIO_EXTS = {"m4a", "mp3", "ogg", "opus", "flac", "wav"}


def _extractor_args():
    # NOTE: don't force a player_client here. youtube-search-style scraping is
    # dead and clients like tv/web_embedded/android are SABR-limited or need a
    # JS runtime; yt-dlp's defaults are the actively maintained workaround.
    # If YouTube bot-checks the server's IP ("Sign in to confirm..."), the
    # only reliable fixes are YOUTUBE_PO_TOKEN / YOUTUBE_COOKIES_FILE below.
    extractor_args = {"youtube": {}}
    # "client+token" pairs, e.g. "web+XXX,android+YYY".
    po_token = os.environ.get("YOUTUBE_PO_TOKEN", "").strip()
    if po_token:
        extractor_args["youtube"]["po_token"] = po_token.split(",")
    return extractor_args


def _yt_dlp_opts(outtmpl):
    opts = {
        "quiet": True,
        "noplaylist": True,
        "format": "bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio/best",
        "outtmpl": outtmpl,
        "retries": 3,
        "fragment_retries": 3,
        "file_access_retries": 3,
        "extractor_args": _extractor_args(),
    }
    cookies = os.environ.get("YOUTUBE_COOKIES_FILE", "").strip()
    if cookies:
        opts["cookiefile"] = cookies
    return opts


def _search(query):
    with yt_dlp.YoutubeDL({"quiet": True, "extractor_args": _extractor_args()}) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=False)
    entries = (info or {}).get("entries") or []
    return entries[0] if entries else None


def _download(url, outtmpl):
    with yt_dlp.YoutubeDL(_yt_dlp_opts(outtmpl)) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info), info


def _seconds(duration):
    try:
        return int(duration or 0)
    except (TypeError, ValueError):
        return 0


def _fetch_thumbnail(url, path):
    thumb = requests.get(url, allow_redirects=True, timeout=15)
    with open(path, 'wb') as f:
        f.write(thumb.content)


@Client.on_message(filters.command('start') & filters.private)
async def start(client, message):
    await message.reply_photo(
        photo=Config.START_IMG,
        caption=Config.START_MSG.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(BUTTON1, url=GITCLONE)
                ], [
                    InlineKeyboardButton(OWNER, url=f"https://telegram.dog/{Config.OWNER}"),
                    InlineKeyboardButton(ABS, url=B2)
                ]
            ]
        ),
        reply_to_message_id=message.id
    )


@Client.on_message(filters.command(['song']))
async def song(client, message):
    query = ' '.join(str(i) for i in message.command[1:])
    if not query.strip():
        await message.reply("**Enter Song Name with /song Command!**")
        return

    status = await message.reply('`Searching... Please Wait...`')

    try:
        entry = await asyncio.to_thread(_search, query)
    except Exception as e:
        await status.edit('**Search failed. Please try again later.**')
        print(f"yt-dlp search error: {e}")
        return

    if not entry:
        await status.edit('**Nothing found! Try another song name.**')
        return

    link = entry.get("webpage_url") or entry.get("url")
    title = entry.get("title") or query
    thumbnail = entry.get("thumbnail")
    if not thumbnail:
        thumbs = entry.get("thumbnails") or []
        thumbnail = thumbs[-1].get("url") if thumbs else None
    duration = _seconds(entry.get("duration"))

    performer = "[@AB_Mediaw]"
    os.makedirs(Config.DOWNLOAD_LOCATION, exist_ok=True)
    thumb_name = os.path.join(Config.DOWNLOAD_LOCATION, f'thumb{message.chat.id}_{message.id}.jpg')
    try:
        if thumbnail:
            await asyncio.to_thread(_fetch_thumbnail, thumbnail, thumb_name)
    except Exception as e:
        print(e)
        thumb_name = None

    await status.edit("`Downloading... Please Wait...`")
    try:
        outtmpl = os.path.join(Config.DOWNLOAD_LOCATION, f"{message.chat.id}_{message.id}.%(ext)s")
        audio_file, info = await asyncio.to_thread(_download, link, outtmpl)
    except Exception as e:
        err = str(e)
        print(f"yt-dlp download error: {err}")
        if "Sign in to confirm" in err or "bot" in err.lower():
            await status.edit(
                "**YouTube is blocking this server's IP.**\n"
                "Set the `YOUTUBE_PO_TOKEN` env variable (format `client+token`, from a logged-in browser) and restart."
            )
        else:
            await status.edit('**Download failed. Report @redbullfed**')
        if thumb_name and os.path.exists(thumb_name):
            os.remove(thumb_name)
        return

    rep = f'🎶 <b>Title:</b> <a href="{link}">{title}</a>\n' \
          f'⌚ <b>Duration:</b> <code>{duration // 60}:{duration % 60:02d}</code>\n' \
          f'📻 <b>Uploaded By:</b> <a href="https://t.me/AB_Mediaw">AB_Mediaw</a>'

    await status.edit("`Uploading... Please Wait...`")
    try:
        ext = os.path.splitext(audio_file)[1].lstrip(".").lower()
        if ext in AUDIO_EXTS:
            await message.reply_audio(
                audio_file,
                caption=rep,
                parse_mode='HTML',
                quote=False,
                title=title,
                duration=duration,
                performer=performer,
                thumb=thumb_name
            )
        else:
            await message.reply_document(
                audio_file,
                caption=rep,
                parse_mode='HTML',
                quote=False,
                thumb=thumb_name
            )
        await status.delete()
    except Exception as e:
        await status.edit('**Upload failed. Report @redbullfed**')
        print(f"telegram upload error: {e}")

    for path in (audio_file, thumb_name):
        if not path:
            continue
        try:
            os.remove(path)
        except Exception as e:
            print(e)
