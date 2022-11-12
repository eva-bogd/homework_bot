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
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s'
)
logger = logging.getLogger()
fileHandler = logging.FileHandler('program.log', 'a', 'utf-8')
logger.addHandler(fileHandler)
streamHandler = logging.StreamHandler(sys.stdout)
logger.addHandler(streamHandler)


def send_message(bot, message):
    """
    Отправка сообщения в Telegram чат.
    Параметры:
    ----------
    bot: telegram.Bot
        телеграм-бот из пакета python-telegram-bot
    message: str
        сообщение, которое бот должен отправить
    """
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.info('Сообщение успешно отправлено.')
    except Exception:
        logging.exception('Сбой при отправке сообщения.')


def get_api_answer(current_timestamp):
    """
    Запрос к эндпоинту API-сервиса ЯндексПрактикум.
    Параметр:
    ----------
    current_timestamp: int
        время, с которого запрашиваются обновления
    Возвращает:
    ----------
    api_answer: dict
        ответ API-сервиса ЯндексПрактикум
    """
    timestamp = current_timestamp
    params = {'from_date': timestamp}
    api_answer = requests.get(ENDPOINT, headers=HEADERS, params=params)
    incorrect_codes = ['404', '408', '429', '504', '500']
    if api_answer.status_code == 200:
        return api_answer.json()
    elif api_answer.status_code in incorrect_codes:
        raise exceptions.StatusCodeError(
            f'Ошибка при обращении к эндпоинту API-сервиса ЯндексПрактикум.'
            f'Код ответа сервера:  {api_answer.status_code}')
    else:
        raise exceptions.StatusCodeError(
            'Ошибка при обращении к эндпоинту API-сервиса ЯндексПрактикум')


def check_response(response):
    """
    Проверка ответа API-сервиса ЯндексПрактикум на корректность.
    Параметр:
    ----------
    response: dict
        словарь с ключами 'homeworks' и 'current_date'
    Возвращает:
    ----------
    homeworks: list
        список с домашними работами
    """
    if (isinstance(response, dict)
        and response.__contains__('homeworks')
        and response.__contains__('current_date')):
            homeworks = response['homeworks']
            if isinstance(homeworks, list):
                return homeworks
            else:
                raise TypeError('homeworks не является списком.')

    else:
        raise TypeError(
            'Ответ API не является словарём и не содержит ожидаемые ключи.')


def parse_status(homework):
    """
    Получение информации о конкретной домашней работе, статус этой работы.
    Параметр:
    ----------
    homework: dict
        словарь с данными о домашней работе
    Возвращает:
    ----------
    str
        строку, содержащую сообщение о статусе домашней работы
    """
    if (isinstance(homework, dict)
        and homework.__contains__('homework_name')
        and homework.__contains__('status')):
            homework_name = homework['homework_name']
            homework_status = homework['status']
            if homework_status in HOMEWORK_STATUSES:
                verdict = HOMEWORK_STATUSES[homework_status]
            else:
                raise exceptions.HomeworkStatusError(
                'Получен неизвестный статус домашней работы.')
    else:
        raise KeyError(
            'homework не является словарём и не содержит ожидаемые ключи.')
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """
    Проверка доступности переменных окружения.
    Возвращает:
    ----------
    False - если отсутствует хотя бы одна переменная окружения
    True - если присутствуют все переменные окружения
    """
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        error_message = 'Переменные окружения недоступны.'
        logging.critical(error_message)
        raise exceptions.TokensError(error_message)

    bot = Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())

    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            if (len(homeworks) > 0):
                for homework in homeworks:
                    message = parse_status(homework)
                    send_message(bot, message)
            else:
                logging.debug('Нет новых статусов домашней работы.')
            current_timestamp = int(time.time())
            time.sleep(RETRY_TIME)

        except Exception as error:
            logging.error(error)
            message = f'Сбой в работе программы: {error}'
            send_message(bot, message)
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
