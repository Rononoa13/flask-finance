import sqlite3

connection = sqlite3.connect("instance/finance.db", check_same_thread=False)
# Changes returned list to dictionaries
connection.row_factory = sqlite3.Row

# 
INSERT_USER = "INSERT INTO users (username, hash) VALUES (?, ?)"
SELECT_USERS = "SELECT * FROM users WHERE username = ?"
SELECT_CASH = "SELECT cash FROM users WHERE id = ?"
UPDATE_CASH = "UPDATE users SET cash = ? WHERE id = ?"
INSERT_INTO_TRANSACTION = "INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?);"


def add_user(name, hash):
    with connection:
        connection.execute(INSERT_USER, (name, hash))

def get_user(username):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_USERS, [username])
        return cursor.fetchall()

def get_cash(userid):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_CASH, (userid,))
        return cursor.fetchone()
        # connection.execute(SELECT_CASH, [userid])

# cursor = connection.cursor()
# cursor.execute("SELECT * FROM users")
# answer = cursor.fetchall()

# for ans in answer:
#     print(ans['cash'])
# 
# cursor = connection.cursor()
# cursor.execute(SELECT_CASH)
# answer = cursor.fetchone()
# print(answer['cash'])

def update_cash(cash, userid):
    with connection:
        cursor = connection.cursor()
        cursor.execute(UPDATE_CASH, (cash, userid))
        return cursor.fetchone()

def add_entry_in_transaction(user_id, symbol, shares, price, date):
    with connection:
        connection.execute(INSERT_INTO_TRANSACTION, (user_id, symbol, shares, price, date))