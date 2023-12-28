import os

from dotenv import load_dotenv


load_dotenv()


# =+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
BOT_TOKEN = os.getenv('BOT_TOKEN')
# =+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
DATABASE_URL = os.getenv('DATABASE_URL')
LOG_FILE = os.getenv('LOG_FILE')
# =+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
CRON_TRIGGER_DAY_OF_WEEK = os.getenv("CRON_TRIGGER_DAY_OF_WEEK")
CRON_TRIGGER_HOUR = os.getenv("CRON_TRIGGER_HOUR")
CRON_TRIGGER_MINUTE = os.getenv("CRON_TRIGGER_MINUTE")
# =+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
ADMIN_ID = os.getenv('ADMIN_ID')
SUPPORT_CHAT_ID = os.getenv('SUPPORT_CHAT_ID')
