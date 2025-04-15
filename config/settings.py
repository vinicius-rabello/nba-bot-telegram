import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Database settings
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PORT = os.environ.get("DB_PORT")

# define sslmode
SSLMODE = "require" if os.environ.get("DB_SSL", "false").lower() == "true" else "disable"

# Telegram bot token
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")