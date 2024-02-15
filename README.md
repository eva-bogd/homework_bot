[![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue)](https://www.python.org/)
[![Telegram Bot](https://img.shields.io/badge/Telegram%20Bot-Yes-brightgreen)](https://telegram.org/)

## Homework bot

**Homework bot** - это Telegram-бот для отслеживания статуса проверки домашней работы на Яндекс Практикуме.

Данный бот обращается к API сервиса Практикум.Домашка и узнаёт статус домашней работы: взята ли домашка в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку, после чего отправляет соответствующее сообщение в telegram.

### Технологии:

* Python 3.7.9
* Python-dotenv 0.19.0
* Python-telegram-bot 13.7

### Как запустить проект:

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/eva-bogd/homework_bot.git
```

```
cd homework_bot
```

2. Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
venv/scripts/activate
```

3. Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

4. Создать в корневой директории файл .env и заполнить следующие переменные в .env:

```
YAP_TOKEN = токен_к_api_практикум.домашка
TG_TOKEN = токен_telegram_бота
TG_ID = telegram_ID
```

5. В директории c файлом homework.py выполнить команду:

```
python homework.py
```