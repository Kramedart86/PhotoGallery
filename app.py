from flask import Flask, render_template, request, redirect, url_for, flash, g, session, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

import os
import sqlite3

app = Flask(__name__, template_folder="templates")
app.config['UPLOAD_FOLDER'] = 'static/images/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = 'gotohellbobbykotick'  # Секретный ключ для сеансов. Нужен для обеспечения безопасности сессий на стороне клиента.

DATABASE_ACC = 'account.db'

# Создание подключения к базе данных аккаунтов
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_ACC)
    return db

# Инициализация базы данных
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          username TEXT UNIQUE NOT NULL,
                          password TEXT NOT NULL)''')
        db.commit()

# Закрытие подключения к базе данных
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

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
def register_user(username, password):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, generate_password_hash(password)))
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
    if user and check_password_hash(user[2], password):
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
        elif check_password_hash(user[2], password):
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
        password = request.form['password']
        if register_user(username, password):
            return render_template('index.html', message_ok='Регистрация успешна', images=images)
        else:
            return render_template('index.html', message='Пользователь уже существует', images=images)
    return render_template('index.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect('/')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE_ACC)
    c = conn.cursor()

    c.execute("SELECT * FROM images")
    images = c.fetchall()

    conn.close()

    if 'username' in session:
        logged_in = True
        username = session['username']
        return render_template('index.html', logged_in=logged_in, username=username, images=images)

    return render_template('index.html', logged_in=False, images=images)

@app.route('/clear_gallery', methods=['POST'])
def clear_gallery():
    conn = sqlite3.connect(DATABASE_ACC)
    c = conn.cursor()

    # Удаление всех изображений из базы данных
    c.execute("DELETE FROM images")
    conn.commit()
    conn.close()

    # Удаляем все изображения из папки
    image_folder = os.path.join(app.root_path, 'static/images')
    for filename in os.listdir(image_folder):
        file_path = os.path.join(image_folder, filename)
        os.remove(file_path)

    # Перенаправление пользователя на главную страницу
    return redirect(url_for('index'))


@app.route('/delete_user_images', methods=['POST'])
def delete_user_images():
    # Получаем имя пользователя из сеанса
    username = session.get('username')

    conn = sqlite3.connect(DATABASE_ACC)
    c = conn.cursor()

    # Выбираем все изображения конкретного пользователя
    c.execute("SELECT filename FROM images WHERE username = ?", (username,))
    user_images = c.fetchall()
    
    for image in user_images:
        filename = image[0]
        # Удаляем изображение из локальной папки
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    # Удаляем изображения из базы данных
    c.execute("DELETE FROM images WHERE username = ?", (username,))
    conn.commit()

    conn.close()
    return redirect(url_for('index'))

@app.route('/add_image', methods=['GET', 'POST'])
def add_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['image']
        description = request.form['description']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            name = os.path.splitext(filename)[0]
            count = 1

            while os.path.exists(save_path):
                new_name, ext = os.path.splitext(filename)
                new_name = name
                new_filename = f"{new_name} ({count}){ext}"
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                count += 1
                filename = new_filename

            file.save(save_path)

            # Получаем текущего пользователя из сеанса
            username = session.get('username')

            conn = sqlite3.connect(DATABASE_ACC)
            c = conn.cursor()
            
            c.execute("INSERT INTO images (filename, description, username) VALUES (?, ?, ?)", (filename, description, username))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))   
        
    return render_template('add_image.html')

# Функция для удаления изображения из базы данных
@app.route('/delete_image/<filename>', methods=['POST'])
def delete_image(filename):
    # Получаем имя пользователя из сеанса
    username = session.get('username')

    conn = sqlite3.connect(DATABASE_ACC)
    c = conn.cursor()
    c.execute("SELECT username, filename FROM images WHERE filename = ?", (filename,))
    image = c.fetchone()
    
    if image and image[0] == username:
        filename = image[1]
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        c.execute("DELETE FROM images WHERE filename = ?", (filename,))
        conn.commit()

    conn.close()
    return redirect(url_for('index'))

@app.route('/download_image/<filename>', methods=['GET'])
def download_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
