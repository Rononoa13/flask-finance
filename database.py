import sqlite3

connection = sqlite3.connect("instance/finance.db", check_same_thread=False)
# Changes returned list to dictionaries
connection.row_factory = sqlite3.Row

# 
INSERT_USER = "INSERT INTO users (username, hash) VALUES (?, ?)"
SELECT_USERS = "SELECT * FROM users WHERE username = ?"
SELECT_SY_SH_PR = "SELECT symbol, SUM(shares) as shares, price FROM transactions WHERE user_id = ? GROUP BY symbol"
SELECT_ONE_USER = "SELECT username FROM users WHERE id = ?"
SELECT_CASH = "SELECT cash FROM users WHERE id = ?"
UPDATE_CASH = "UPDATE users SET cash = ? WHERE id = ?"
INSERT_INTO_TRANSACTION = "INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?);"
SELECT_SYMBOL_ONLY = "SELECT DISTINCT(symbol) FROM transactions WHERE user_id = ?"
SELECT_ALL = "SELECT * FROM transactions WHERE user_id = ?"


def add_user(name, hash):
    with connection:
        connection.execute(INSERT_USER, (name, hash))

def get_user(username):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_USERS, [username])
        return cursor.fetchall()

def get_one_user(userid):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_ONE_USER, (userid,))
        return cursor.fetchone()

def get_cash(userid):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_CASH, (userid,))
        return cursor.fetchone()
        # connection.execute(SELECT_CASH, [userid])

# sy- symbol sh- shares, pr- price
def get_sy_sh_pr(userid):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_SY_SH_PR, (userid,))
        return cursor.fetchall()

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

def get_symbol_from_transactions(userid):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_SY_SH_PR, (userid,))
        answer = cursor.fetchall()
        for row in answer:
            return row["symbol"]

def get_only_symbol(user_id):
    symbol_list = []
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_SYMBOL_ONLY, (user_id,))
        symbols =  cursor.fetchall()
        # symbol = [symbol['symbol'] for symbol in symbols]
        # return symbol
        for symbol in symbols:
            symbol_list.append(symbol['symbol'])
        return symbol_list

def get_all_transaction_db(user_id):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_ALL, (user_id, ))
        return cursor.fetchall()
