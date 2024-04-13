from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

import os
import sqlite3

app = Flask(__name__, template_folder="templates")
app.config['UPLOAD_FOLDER'] = 'static/images/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    # Создаем соединение с базой данных SQLite
    conn = sqlite3.connect('gallery.db')
    c = conn.cursor()

    # Выполняем SQL-запрос для получения всех изображений
    c.execute("SELECT * FROM images")
    images = c.fetchall()

    # Закрываем соединение
    conn.close()

    return render_template('index.html', images=images)

@app.route('/clear_gallery', methods=['POST'])
def clear_gallery():
    # Установка соединения с базой данных
    conn = sqlite3.connect('gallery.db')
    c = conn.cursor()

    # Удаление всех изображений из базы данных
    c.execute("DELETE FROM images")
    conn.commit()

    # Закрытие соединения
    conn.close()

    # Удаляем все изображения из папки
    image_folder = os.path.join(app.root_path, 'static/images')
    for filename in os.listdir(image_folder):
        file_path = os.path.join(image_folder, filename)
        os.remove(file_path)

    # Перенаправление пользователя на главную страницу
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
            count = 1
            while os.path.exists(save_path):
                name, ext = os.path.splitext(filename)
                new_filename = f"{name}{count}{ext}"
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                count += 1
                filename = new_filename

            file.save(save_path)
            conn = sqlite3.connect('gallery.db')
            c = conn.cursor()
            c.execute("INSERT INTO images (filename, description) VALUES (?, ?)", (filename, description))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))   
        
    return render_template('add_image.html')

# Функция для удаления изображения из базы данных
@app.route('/delete_image/<filename>', methods=['POST'])
def delete_image(filename):
    conn = sqlite3.connect('gallery.db')
    c = conn.cursor()
    c.execute("SELECT * FROM images WHERE filename = ?", (filename,))
    image = c.fetchone()
    if image:
        filename = image[1]
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        c.execute("DELETE FROM images WHERE filename = ?", (filename,))
        conn.commit()

    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
