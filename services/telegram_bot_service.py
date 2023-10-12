import requests
from config.services import Service

class TelegramBotService:
    
    TELEGRAM_BOT_API_BASE_LINK = 'https://api.telegram.org'
    TELEGRAM_BOT_TOKEN = Service.TELEGRAM_BOT['token']   
    TELEGRAM_BOT_API_LINK = f"{TELEGRAM_BOT_API_BASE_LINK}/bot{TELEGRAM_BOT_TOKEN}"
    BOT_NAME = Service.TELEGRAM_BOT['name']
    DEFAULT_COMMAND = 'start'
    
    @classmethod
    def set_webhook(self, webhook_link: str) -> object:
        return requests.get(f"{self.TELEGRAM_BOT_API_LINK}/setWebhook?url={webhook_link}")
        
    @classmethod
    def set_my_commands(self, data: object) -> object:
        return requests.post(f"{self.TELEGRAM_BOT_API_LINK}/setMyCommands", json = data)
    
    @classmethod
    def send_message(self, data: object) -> object:
        return requests.post(f"{self.TELEGRAM_BOT_API_LINK}/sendMessage", json = data)
    
    @classmethod
    def send_photo(self, data: object, files) -> object:
        return requests.post(f"{self.TELEGRAM_BOT_API_LINK}/sendPhoto", data = data, files = files)
    
    @classmethod
    def get_file(self, file_id: str) -> object:
        return requests.get(f"{self.TELEGRAM_BOT_API_LINK}/getFile" , params = {'file_id': file_id})
    
    @classmethod
    def get_content(self, file_path: str) -> str:
        return requests.get(f"{self.TELEGRAM_BOT_API_BASE_LINK}/file/bot{self.TELEGRAM_BOT_TOKEN}/{file_path}")