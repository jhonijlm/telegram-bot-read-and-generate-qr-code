from .telegram_bot_service import TelegramBotService
from .qr_code_service import QrCodeService
from .file_service import FileService
from config.services import Service
import traceback
from .logger_service import Logger

class BotService:
    
    def __init__(self) -> None:        
        self.qr_code_svc = QrCodeService()
        self.file_svc = FileService()        
    
    def process(self, request_data) -> None:
        try:            
            if 'message' in request_data:         
                text = request_data.get('message').get('text')           
                chat_id = request_data.get('message').get('chat').get('id')
                message_id = request_data.get('message').get('message_id')
                user_first_name = request_data.get('message').get('from').get('first_name')
                
                if 'entities' in request_data.get('message'):
                    command_type = request_data.get('message').get('entities')[0].get('type')
                    
                    if command_type == 'bot_command':    
                        self._process_commands(chat_id, message_id, user_first_name, text)    
                        
                elif 'photo' in request_data.get('message'):
                    photos = request_data.get('message').get('photo')
                    self._process_photo(chat_id, message_id, photos)
                        
        except Exception as ex:                            
            TelegramBotService.send_message({'chat_id': chat_id, 'reply_to_message_id': message_id, 'text': "An error occurred 😞, please try again"})
            
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
                 
                      
    def _process_photo(self, chat_id: int, message_id: int , photos: list) -> None:
        sorted_photo_list = sorted(photos, key=lambda x: x['file_size'], reverse=True)
        photo = sorted_photo_list[0]
        
        file_repsonse = TelegramBotService.get_file(photo.get('file_id'))
        file_data = file_repsonse.json()
        
        file_content_response = TelegramBotService.get_content(file_data.get('result').get('file_path'))        
        filename = f"read-{self.file_svc.get_random_filename('jpg')}"   
        file_path = f"./storage/files/{filename}"
        self.file_svc.save_file(file_content_response.content, file_path)
        
        text = self.qr_code_svc.read(file_path)[:4000]
        if text:            
            TelegramBotService.send_message({'chat_id': chat_id, 'reply_to_message_id': message_id, 'text': text})   
        else:
            TelegramBotService.send_message({'chat_id': chat_id, 'reply_to_message_id': message_id, 'text': "I couldn't find the QR code 😞, please attach a clearer photo 😀."})
                      
    def _process_commands(self, chat_id: int, message_id: int, user_first_name: str, text: str) -> None:
        command_text = self._get_command(text)
        text_without_command = self._get_text_without_command(text)       
        
        help_text = "I'm a bot that can help you to generate and read qr codes, to generate just send <b>/generate text here</b> and to read just send me a picture or image of the qr code 😀"
        
        if command_text == '/start':
            self._set_commands()            
            TelegramBotService.send_message({
                'chat_id': chat_id, 
                'parse_mode': 'HTML',
                'text': f'''Hi {user_first_name}, I'm {TelegramBotService.BOT_NAME},\n{help_text}''',
            })            
                     
        elif command_text == '/help':
            TelegramBotService.send_message({'chat_id': chat_id, 'parse_mode': 'HTML', 'disable_web_page_preview': True, 'text': f'''{help_text}\n\nPlease note that, at the moment, I can only generate QR codes with a maximum of 500 characters and read up to 4000 characters.\n\nIf you have any questions or comments, don't hesitate to write to me on my contact page {Service.CONTACT_PAGE_LINK} 🙂.'''})   
        
        elif command_text == '/aboutus':
            TelegramBotService.send_message({'chat_id': chat_id, 'parse_mode': 'HTML', 'text': f'{help_text}'})   
        
        elif command_text == '/generate':     
            if text_without_command is not None:                       
                filename = f"generated-{self.file_svc.get_random_filename('png') }"         
                image = self.qr_code_svc.generate(text_without_command, filename)
                image_file = self.file_svc.get_file(image['path'])
                
                files = {'photo': image_file}
                data = {'chat_id': chat_id, 'reply_to_message_id': message_id}               
                TelegramBotService.send_photo(data, files)     
                       
            else:
                TelegramBotService.send_message({'chat_id': chat_id, 'text': f"{command_text} Please enter the text"})   
    
    def _commands(self) -> list:
        return [
            {
                'command': 'generate',
                'description': 'Here, enter the text to generate the QR code'
            },
            {
                'command': 'help',
                'description': 'How is the bot used?'
            },
            {
                'command': 'aboutus',
                'description': 'What is the bot about?'
            }
        ]  
        
    
    def _set_commands(self) -> None:
        commands = self._commands()      
                
        data = {
            'commands': commands,
            'scope': {
                'type': 'all_private_chats'
            }
        }
        
        TelegramBotService.set_my_commands(data)            
    
    def _get_command(self, text: str) -> str | None:
        commands = self._commands()
        command_text = None
        
        if text[0] == '/':
            for word in text.split():            
                if list(filter(lambda c: f"/{c['command']}" == word, commands)):
                    command_text = word
                    break
                elif f"/{TelegramBotService.DEFAULT_COMMAND}" == word:
                    command_text = word
                    break
        
        return command_text

    def _get_text_without_command(self, text: str) -> str | None:
        commands = self._commands()
        new_text = text
        
        for c in commands:
            new_text = new_text.replace(f"/{c['command']}", '')
        
        new_text_cleaned = new_text.strip()
        
        return new_text_cleaned if len(new_text_cleaned) > 0 else None