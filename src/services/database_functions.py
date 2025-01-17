import sqlite3


def create_connection():
    conn = sqlite3.connect("src/database/users.db")
    # conn = sqlite3.connect("../database/users.db")
    return conn


def make_entry_a_dict(data: tuple) -> dict:
    user_keys = ('id', 'telegram_id', 'username', 'first_name', 'last_name', 'created_at', 'loading_file')
    return dict(zip(user_keys, data))


def add_user(telegram_id, username, first_name, last_name, created_at, loading_file):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO bot_user (telegram_id, username, first_name, last_name, created_at, loading_file)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (telegram_id, username, first_name, last_name, created_at, loading_file))
    conn.commit()
    conn.close()


def get_user(telegram_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM bot_user WHERE telegram_id = ?''', (telegram_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_loading_status(telegram_id: int) -> bool:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM bot_user WHERE telegram_id = ?''', (telegram_id,))
    user = make_entry_a_dict(cursor.fetchone())
    return user['loading_file']


def change_loading_photo_status(telegram_id: int) -> None:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM bot_user WHERE telegram_id = ?''', (telegram_id,))
    user = cursor.fetchone()
    print(user[-1])
    if user[-1]:
        cursor.execute('''UPDATE bot_user SET loading_file = 0 WHERE telegram_id = ?''', (telegram_id,))
    else:
        cursor.execute('''UPDATE bot_user SET loading_file = 1 WHERE telegram_id = ?''', (telegram_id,))
    conn.commit()
    conn.close()


def del_user(telegram_id: int):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM bot_user WHERE telegram_id = ?''', (telegram_id,))
    # cursor.execute('''DELETE FROM bot_user WHERE telegram_id = 7613056223''')
    conn.close()

# del_user(7613056223)
