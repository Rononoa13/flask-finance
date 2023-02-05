import sqlite3

connection = sqlite3.connect("instance/finance.db", check_same_thread=False)
# Changes returned list to dictionaries
connection.row_factory = sqlite3.Row

# 
INSERT_USER = "INSERT INTO users (username, hash) VALUES (?, ?)"
SELECT_USERS = "SELECT * FROM users WHERE username = ?"

def add_user(name, hash):
    with connection:
        connection.execute(INSERT_USER, (name, hash))

def get_user(username):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_USERS, [username])
        return cursor.fetchall()