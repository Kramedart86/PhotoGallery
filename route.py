from database import DATABASE_ACC, sqlite3
from flask import flash, send_from_directory
from account import session, render_template, redirect, request, url_for
from config import app, allowed_file
from werkzeug.utils import secure_filename

import os

@app.route('/donation_page')
def donation_page():
    return render_template('donation_page.html')

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
