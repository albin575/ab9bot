import os


def _require_env(name, default=""):
    value = os.environ.get(name, "").strip()
    if not value:
        if default:
            return default
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            "Set it in the Render dashboard (or a local .env file) and restart."
        )
    return value


class Config:
    APP_ID = int(_require_env("APP_ID", "8733952"))
    API_HASH = _require_env("API_HASH", "858e4d8e6f4986317031c0b83373d865")
    BOT_TOKEN = _require_env("BOT_TOKEN", "5253662828:AAFikLGDgnDZQIHICSOHAtmOxiV7NFZI6nk")
    START_MSG = os.environ.get("START_MSG", "<b>ഹായ് {},\nനിങ്ങൾക്ക് വേണ്ട song കിട്ടാൻ /song ഇങ്ങനെ കമാൻഡ് ടൈപ്പ് ചെയ്ത ശേഷം space ഇട്ട ശേഷം പാട്ടിന്റെ വരി ടൈപ്പ് ചെയ്തു കൊടുക്കുക 💖💞,</b>\n\nSend me Any Songs name with /song command")
    START_IMG = os.environ.get("START_IMG", "https://i.ibb.co/Rpxdp77L/7a9802c2-e3a3-40fb-b101-d2a06d8c7be3.jpg")
    OWNER = os.environ.get("OWNER", "AB_Mediaw")
    DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS/")
    msg = {}
