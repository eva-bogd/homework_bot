import logging
import sys
import os
import requests
import time
from telegram import Bot
from dotenv import load_dotenv

import exceptions

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


logging.basicConfig(
    level=logging.DEBUG,
    filename='program.log', 
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s'
)


def send_message(bot, message):
    """Отправка сообщения в Telegram чат"""
    # bot.send_message(TELEGRAM_CHAT_ID, message)
    try: 
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.info('Сообщение успешно отправлено.')
    except Exception:
        logging.exception('Сбой при отправке сообщения.')



def get_api_answer(current_timestamp):
    """Запрос к эндпоинту API-сервиса ЯндексПрактикум"""
    timestamp = current_timestamp #or int(time.time())
    params = {'from_date': timestamp}
    api_answer = requests.get(ENDPOINT, headers=HEADERS, params=params)
    incorrect_codes = ['404', '408', '429', '504', '500']
    if api_answer.status_code == 200:
        return api_answer.json()
    elif api_answer.status_code in incorrect_codes:
        raise exceptions.StatusCodeError(f'Ошибка при обращении к эндпоинту API-сервиса ЯндексПрактикум.' 
                                         f'Код ответа сервера:  {api_answer.status_code}')
    else:
        raise exceptions.StatusCodeError('Ошибка при обращении к эндпоинту API-сервиса ЯндексПрактикум')


def check_response(response):
    """Проверка ответа API на корректность"""
    if isinstance(response, dict) and response.__contains__('homeworks'):
        return response['homeworks']
    else:
        raise exceptions.ResponseError('Ошибка при проверке ответа API на корректность')


def parse_status(homework):
    """Получение информации о конкретной домашней работе, статус этой работы"""
    homework_name = homework['homework_name']
    homework_status = homework['status']
    if homework_status in HOMEWORK_STATUSES:
        verdict= HOMEWORK_STATUSES[homework_status]
    else:
        raise exceptions.StatusKeyError('Ошибка при получении информации о домашней работе, неизвестный статус домашней работы')
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверка доступности переменных окружения"""
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logging.critical('Переменные окружения недоступны.')
        sys.exit()

    bot = Bot(token=TELEGRAM_TOKEN)
    current_timestamp = 0 # int(time.time())

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

        except exceptions.HomeworkException as error:
            logging.error(error)
            message = f'Сбой в работе программы: {error}'
            send_message(bot, message)
            time.sleep(RETRY_TIME)
       # else:



if __name__ == '__main__':
    main()
