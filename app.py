from flask import Flask
from flask_cors import CORS
from settings_function import settings
from Home_page_trust_bearing import home_bearing
from information import information
from openBrowser import openBrowser
from simple_display import simpleDisplay

app = Flask(__name__)
CORS(app)
app.register_blueprint(settings)
app.register_blueprint(home_bearing)
app.register_blueprint(information)
app.register_blueprint(simpleDisplay)

@app.route('/')
def index():
    return "Badan anda bau, Harap mandi Wajib"

if __name__ == '__main__':
    app.run(debug=True)
    openBrowser()  # Membuka browser dengan halaman utama Badan Anda Bau
