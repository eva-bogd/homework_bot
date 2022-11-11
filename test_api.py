import os
import requests

from pprint import pprint

from dotenv import load_dotenv

from telegram import Bot

load_dotenv()


PRACTICUM_TOKEN = os.getenv('YAP_TOKEN')
TELEGRAM_TOKEN = os.getenv('TG_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TG_ID')

ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

bot = Bot(token=TELEGRAM_TOKEN)

payload = {'from_date': 1665462792}
homework_statuses = requests.get(ENDPOINT, headers=HEADERS, params=payload)

#pprint(homework_statuses.json())

#text = 'Привет!'
text = homework_statuses.json()

bot.send_message(TELEGRAM_CHAT_ID, text)
