import asyncio
import logging
import os
import threading

# pyrogram 2.0.106 calls asyncio.get_event_loop() at import time, which
# raises RuntimeError on Python 3.12+ when no main-thread loop exists yet.
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import pyrogram
from flask import Flask

from config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Render health checks require a process listening on $PORT
web = Flask(__name__)


@web.route("/")
def health():
    return "Bot is running", 200


def run_web():
    web.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


threading.Thread(target=run_web, daemon=True).start()

app = pyrogram.Client(
    "mwk",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    plugins=dict(root="modules")
)
app.run()
