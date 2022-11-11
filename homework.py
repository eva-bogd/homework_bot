import logging
import os
import requests
import time
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()


PRACTICUM_TOKEN = os.getenv('YAP_TOKEN')
TELEGRAM_TOKEN = os.getenv('TG_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TG_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    """Отправка сообщения в Telegram чат"""
    bot.send_message(TELEGRAM_CHAT_ID, message)


def get_api_answer(current_timestamp):
    """Запрос к эндпоинту API-сервиса"""
    timestamp = current_timestamp #or int(time.time())
    params = {'from_date': timestamp}
    api_answer = requests.get(ENDPOINT, headers=HEADERS, params=params)
    if api_answer.status_code == 200:
        return api_answer.json()
    else:
        raise Exception


def check_response(response):
    """Проверка ответа API на корректность"""
    if isinstance(response, dict) and response.__contains__('homeworks'):
        return response['homeworks']
    else:
        raise Exception


def parse_status(homework):
    """Получение информации о конкретной домашней работе, статус этой работы"""
    homework_name = homework['homework_name']
    homework_status = homework['status']
    #verdict = HOMEWORK_STATUSES.get(homework['status'])
    if homework_status in HOMEWORK_STATUSES:
        verdict= HOMEWORK_STATUSES[homework_status]
    else:
        raise Exception
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверка доступности переменных окружения"""
    if PRACTICUM_TOKEN or TELEGRAM_TOKEN or TELEGRAM_CHAT_ID is not None:
        return True
    else:
        return False


def main():
    """Основная логика работы бота."""
    bot = Bot(token=TELEGRAM_TOKEN)
    #current_timestamp = int(time.time())
    current_timestamp = 0
    # Вызвать проверку токкенов, вписать логи, остановить если токены Falseттт
    # bot.stop_polling()


    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            if (len(homeworks) > 0):
                for homework in homeworks:
                    message = parse_status(homework)
                    send_message(bot, message)
            current_timestamp = int(time.time())
            time.sleep(RETRY_TIME)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            send_message(bot, message)
            time.sleep(RETRY_TIME)
       # else:



if __name__ == '__main__':
    main()
