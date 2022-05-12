import os

SERVER_URL = os.environ["SERVER_URL"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
USERS = [
    {
        "chat_id": int(os.environ["CHAT_ID"]),
        "anki_username": os.environ["ANKI_USERNAME"],
        "anki_password": os.environ["ANKI_PASSWORD"]
    }
]
ALLOWED_CHAT_ID = [user_config["chat_id"] for user_config in USERS]
