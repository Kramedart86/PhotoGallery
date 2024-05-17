from flask import Flask
from flask_mail import Mail

app = Flask(__name__, template_folder="templates")
app.config['UPLOAD_FOLDER'] = 'static/images/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = 'gotohellbobbykotick'  # Секретный ключ для сеансов. Нужен для обеспечения безопасности сессий на стороне клиента.

# Конфигурация Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.yandex.ru'  # Адрес SMTP сервера
app.config['MAIL_PORT'] = 587  # Порт SMTP сервера (обычно 587 для TLS или 465 для SSL)
app.config['MAIL_USE_TLS'] = True  # Использовать ли TLS
app.config['MAIL_USERNAME'] = 'i.pavluschin@ya.ru'  # Ваше имя пользователя на почтовом сервере
app.config['MAIL_PASSWORD'] = 'iyrirtmegxqynjam'  # Ваш пароль на почтовом сервере
app.config['MAIL_DEFAULT_SENDER'] = ('GuardiArt', 'i.pavluschin@ya.ru')

mail = Mail(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
