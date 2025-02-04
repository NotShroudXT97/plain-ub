import os

from dotenv import load_dotenv

load_dotenv("config.env")

from app.config import Config  # NOQA
from app.core.db import DB  # NOQA
from app.core.client.client import BOT  # NOQA

if "com.termux" not in os.environ.get("PATH", ""):
    import uvloop

    uvloop.install()

bot = BOT()

from app.core.client.conversation import Conversation as Convo  # NOQA
