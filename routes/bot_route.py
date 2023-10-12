from flask import Blueprint, jsonify, Response, request, abort
from services import TelegramBotService, bot_svc
from config.status_code import StatusCode
from config.services import Service

bot_rt = Blueprint('bot', __name__)

@bot_rt.route('/', methods=['GET'])
def index() -> Response:
    return jsonify({'message': 'home'}), StatusCode.HTTP_200_OK


@bot_rt.route('/set-webhook', methods=['GET'])
def set_webhook() -> Response:    
    print(Service.TELEGRAM_BOT['webhook'])
    TelegramBotService.set_webhook(Service.TELEGRAM_BOT['webhook'])
    return 'ok', StatusCode.HTTP_200_OK

@bot_rt.route('/handler', methods=['POST'])
def handler() -> Response:
    data = request.json        
    bot_svc.process(data)        
    return 'ok', StatusCode.HTTP_200_OK