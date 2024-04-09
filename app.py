from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__) # Инициализация сервера

@app.route('/') # Аннотация с параметром  
def index():
    # Создаем соединение с базой данных SQLite
    conn = sqlite3.connect('gallery.db')
    c = conn.cursor()

    # Выполняем SQL-запрос для получения всех изображений
    c.execute("SELECT * FROM images")
    images = c.fetchall()

    # Закрываем соединение
    conn.close()

    return render_template('index.html', images=images) # Возврат главной страницы 

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

    # Перенаправление пользователя на главную страницу
    return redirect(url_for('index'))

@app.route('/add_image', methods=['GET', 'POST'])
def add_image():
    if request.method == 'POST':
        # Создаем соединение с базой данных SQLite
        conn = sqlite3.connect('gallery.db')
        c = conn.cursor()

        # Получаем данные из формы
        image_file = request.files['image']
        description = request.form['description']
        
        if image_file:
            filename = image_file.filename
            image_file.save('static/images/' + filename)
            
            # Вставляем данные в базу данных
            c.execute("INSERT INTO images (filename, description) VALUES (?, ?)", (filename, description))
            conn.commit()
        
        # Закрываем соединение
        conn.close()

        return redirect(url_for('index'))
    return render_template('add_image.html')

if __name__ == '__main__': # Запуск сервера 
    app.run(debug=True)
