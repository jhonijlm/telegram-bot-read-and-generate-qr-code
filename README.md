# Telegram Bot QR Code

It is a telegram bot that can generate and read QR code

## Requirements
- Python 3.11
- pip3
- virtualenv

## Virtual environments
This project requires a virtual environment, in this case __virtualenv__ is used.
```
$ python -m virtualenv venv
```

Enable virtual environment
```
$ source venv/Scripts/activate
```

Install all project dependencies using:
```
$ pip install -r requirements.txt
```

## Variable environment
Copy the __.env-example__ file to __.env__, create a bot with __Telegram BotFather__, copy the accesses and configure the __.env__ file.
```
$ copy .env-example .env
```
__.env__ file
```Enable virtual environment
APP_ENV=true

TELEGRAM_BOT_NAME=
TELEGRAM_BOT_TOKEN=
TELEGRAM_BOT_WEBHOOK=

CONTACT_PAGE_LINK=
```

## Running
```
$ python app.py 
```
Set webhook to enable telegram bot e.g. https://domain.com/handler, it must replace the domain and only works with SSL.