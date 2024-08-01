import sqlite3
import os
from config import DB_FILE_NAME


def create_table():
    try:
        with sqlite3.connect(DB_FILE_NAME) as conn:
            cur = conn.cursor()
            cur.execute(f"""
            CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        username TEXT,
                        name TEXT,
                        number TEXT,
                        form TEXT,
                        buttons TEXT DEFAULT "[]")""")
            conn.commit()
    except Exception as e:
        print(e)


def get_data_from_db(user_id: int, columns: str):
        try:
            with sqlite3.connect(DB_FILE_NAME) as conn:
                cur = conn.cursor()
                data = cur.execute(f"SELECT {columns} FROM users WHERE user_id = {user_id}")
                return data.fetchall()
        except Exception as e:
            print(e)


def get_users_from_db(columns: str):
        try:
            with sqlite3.connect(DB_FILE_NAME) as conn:
                cur = conn.cursor()
                data = cur.execute(f"SELECT {columns} FROM users")
                return data.fetchall()
        except Exception as e:
            print(e)


def insert_user_to_db(user_id):
    try:
        with sqlite3.connect(DB_FILE_NAME) as con:
            cur = con.cursor()
            if not get_data_from_db(user_id, 'user_id'):
                cur.execute(f'''
                INSERT INTO users(user_id)
                VALUES ({user_id});
                ''')
                con.commit()
 
    except Exception as e:
        print(e)


def update_db(user_id: int, columns: tuple, values: tuple):
    try:
        with sqlite3.connect(DB_FILE_NAME) as con:
            cur = con.cursor()
            for column, value in zip(columns, values):
                cur.execute(f'UPDATE users SET {column} = ? WHERE user_id = {user_id};', (value,))
        con.commit()
 
    except Exception as e:
        print(e)
 


if not os.path.exists(DB_FILE_NAME):
    create_table()

