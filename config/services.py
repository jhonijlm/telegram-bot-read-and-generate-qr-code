from decouple import config

class Service:    
    TELEGRAM_BOT = {
        'name': config('TELEGRAM_BOT_NAME'),
        'token': config('TELEGRAM_BOT_TOKEN'),
        'webhook': config('TELEGRAM_BOT_WEBHOOK')
    }
    
    CONTACT_PAGE_LINK = config('CONTACT_PAGE_LINK')
    