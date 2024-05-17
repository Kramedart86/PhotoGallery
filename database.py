import sqlite3

DATABASE_ACC = 'account.db'

# Функция для установки соединения с базой данных
def get_db():
    conn = sqlite3.connect(DATABASE_ACC)
    conn.row_factory = sqlite3.Row
    return conn

# Создание таблицы users, если она не существует
def create_table_users():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT NOT NULL,
              email TEXT NOT NULL UNIQUE,
              password TEXT NOT NULL,
              activation_link TEXT)''')
    conn.commit()
    conn.close()

create_table_users()
