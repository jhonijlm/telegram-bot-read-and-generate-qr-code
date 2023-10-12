from flask import Flask
from routes.bot_route import bot_rt

app = Flask(__name__)

app.register_blueprint(bot_rt)

if __name__ == '__main__':
    app.run(debug=True)