import os


from dotenv import load_dotenv

load_dotenv()

PRACTICUM_TOKEN = os.getenv('YAP_TOKEN')
TELEGRAM_TOKEN = os.getenv('TG_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TG_ID')

print(PRACTICUM_TOKEN)
