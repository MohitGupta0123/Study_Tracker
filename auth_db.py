import sqlite3
from streamlit_authenticator.utilities.hasher import Hasher

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT username, name, email, password FROM users")
    users = c.fetchall()
    conn.close()
    return {
        'usernames': {
            u[0]: {'name': u[1], 'email': u[2], 'password': u[3]} for u in users
        }
    }

def user_exists(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM users WHERE username=?", (username,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def register_user(username, name, email, password):
    hashed_pw = Hasher().hash(password)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, name, email, password) VALUES (?, ?, ?, ?)",
              (username, name, email, hashed_pw))
    conn.commit()
    conn.close()
