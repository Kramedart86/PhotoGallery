from flask import render_template, request, redirect, session, url_for
from database import DATABASE_ACC, get_db, sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from config import app, mail
from flask_mail import Message

import secrets

# Генерация уникальной ссылки
def generate_activation_link():
    return secrets.token_urlsafe(16)

@app.route('/search')
def search():
    query = request.args.get('query')  # Получаем текст поискового запроса из URL-адреса
    if query:
        # Выполняем поиск в базе данных по имени файла и описанию
        conn = sqlite3.connect(DATABASE_ACC)
        c = conn.cursor()
        c.execute("SELECT * FROM images WHERE description LIKE ? OR username LIKE ?", ('%' + query + '%', '%' + query + '%',))
        results = c.fetchall()
        conn.close()
        if 'username' in session:
            logged_in = True
            username = session['username']
            return render_template('index.html', results=results, username=username, logged_in=logged_in)
        else:
            return render_template('index.html', results=results, logged_in=False, result_message="Результаты не найдены")
    else:
        return "Введите текст для поиска"

@app.route('/get_profile')
def get_profile():
    query = request.args.get('query')  # Получаем текст поискового запроса из URL-адреса
    if query:
        conn = sqlite3.connect(DATABASE_ACC)
        c = conn.cursor()
        c.execute("SELECT * FROM images WHERE username LIKE ?", ('%' + query + '%',))
        results = c.fetchall()
        conn.close()
        if 'username' in session:
            logged_in = True
            username = session['username']   
        return render_template('index.html', results=results, username=username, logged_in=logged_in)

# Регистрация нового пользователя
def register_user(username, password, email, activation_link):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password, activation_link) VALUES (?, ?, ?, ?)", (username, email, generate_password_hash(password), activation_link))
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False # Пользователь с таким именем уже существует

# Поиск пользователя в базе данных
def find_user(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    return cursor.fetchone()

def verify_password(username, password):
    user = find_user(username)
    if user and check_password_hash(user[3], password):
        return True
    elif user is None:
        return "Пользователь не найден"
    return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Создаем соединение с базой данных
    conn = sqlite3.connect(DATABASE_ACC)
    c = conn.cursor()

    # Выполняем SQL-запрос для получения всех изображений
    c.execute("SELECT * FROM images")
    images = c.fetchall()

    # Закрываем соединение
    conn.close()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = find_user(username)

        if user is None:
            return render_template('index.html', message='Пользователь не найден', images=images)
        elif check_password_hash(user[3], password) and not user['activation_link']:
            session['username'] = username
            return redirect('/')
        else:            
            return render_template('index.html', message='Неправильное имя пользователя или пароль', images=images)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = sqlite3.connect(DATABASE_ACC)
    c = conn.cursor()

    c.execute("SELECT * FROM images")
    images = c.fetchall()

    conn.close()

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        activation_link = generate_activation_link()

        if register_user(username, password, email, activation_link):
            msg = Message('Подтверждение регистрации', recipients=[email])
            msg.body = f'Привет, {username}! Перейдите по следующей ссылке, чтобы завершить регистрацию: {request.host_url}activate/{activation_link}'
            mail.send(msg)
            return render_template('index.html', message_ok='Регистрация успешна, проверьте почту.', images=images)
        else:
            return render_template('index.html', message='Пользователь уже существует', images=images)
    return render_template('index.html')

# Страница активации
@app.route('/activate/<activation_link>')
def activate(activation_link):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE activation_link=?", (activation_link,))
    user = cursor.fetchone()

    if user:
        # Пользователь найден, активируем его аккаунт
        cursor.execute("UPDATE users SET activation_link=NULL WHERE id=?", (user['id'],))
        conn.commit()
        conn.close()
        return render_template('index.html', message_ok='Ваш аккаунт успешно активирован!')
    else:
        return render_template('index.html', message='Неверная ссылка активации или аккаунт уже активирован.')

    return redirect(url_for('login'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect('/')
