from os import path

from yt_dlp import YoutubeDL

from config import DURATION_LIMIT
from helpers.errors import DurationLimitError

ydl_opts = {
    "format": "bestaudio/best",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = YoutubeDL(ydl_opts)


def download(url: str) -> str:
    info = ydl.extract_info(url, False)
    duration = round(info["duration"] / 60)
    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"🛑 𝗩𝗶𝗱𝗲𝗼𝘀 𝗹𝗼𝗻𝗴𝗲𝗿 𝘁𝗵𝗮𝗻 {DURATION_LIMIT} 𝗺𝗶𝗻𝘂𝘁𝗲(s) 𝗮𝗿𝗲𝗻'𝘁 𝗮𝗹𝗹𝗼𝘄𝗲𝗱, "
            f"the provided video is {duration} minute(s)",
        )
    ydl.download([url])
    return path.join("downloads", f"{info['id']}.{info['ext']}")
