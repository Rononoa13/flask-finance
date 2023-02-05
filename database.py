import sqlite3

connection = sqlite3.connect("instance/finance.db", check_same_thread=False)
# Changes returned list to dictionaries
connection.row_factory = sqlite3.Row

# 
INSERT_USER = "INSERT INTO users (username, hash) VALUES (?, ?)"


def add_user(name, hash):
    with connection:
        connection.execute(INSERT_USER, (name, hash))