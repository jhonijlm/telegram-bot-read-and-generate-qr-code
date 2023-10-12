from decouple import config

class Service:    
    APP_ENV = True if config('APP_ENV') == 'true' else False
    
    TELEGRAM_BOT = {
        'name': config('TELEGRAM_BOT_NAME'),
        'token': config('TELEGRAM_BOT_TOKEN'),
        'webhook': config('TELEGRAM_BOT_WEBHOOK')
    }
    
    CONTACT_PAGE_LINK = config('CONTACT_PAGE_LINK')
    