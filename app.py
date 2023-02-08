import os

# from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

import database

import json
"""
Apparently directly using jsonify from Flask did not as it could not 
serialize the Stream object in `user_cash_from_db`. When doing jsonify(user_cash_from_db)
Error:  TypeError: Object of type Stream is not JSON serializable

Using jsonpickle did the job. Below code is working:
"""
import jsonpickle

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
# Configure sqlalchemy to use sqlite database
app.config['SECRET_KEY'] = "finance"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'

db = SQLAlchemy()
db.init_app(app)

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")

        # Render an apology if the input is blank or the symbol does not exist 
        if not symbol:
            return apology("Must provide symbol")
        
        stock = lookup(symbol)
        if not stock:
            return apology("Symbol does not exist.")

        shares = int(request.form.get("shares"))
        if shares < 0:
            return apology("Input positive number")

        transaction_value = shares * stock["price"]

        user_id = session["user_id"]
      
        user_cash_from_db = database.get_cash(user_id)

        # Get value from cash column from users table in database
        user_cash = user_cash_from_db['cash']
        
        if user_cash < transaction_value:
            return apology("Not enough balance.")

        update_cash = user_cash - transaction_value
        # UPDATE users SET cash = ? WHERE id = ?
        database.update_cash(update_cash, user_id)

        current_date = datetime.now()

        # INSERT data into transaction table
        database.add_entry_in_transaction(user_id, stock["symbol"], shares, stock["price"], current_date)
        # Redirect user to home page
        flash("Congratulation, you bought the stock.")
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = database.get_user(request.form.get("username"))
        print(f"Rows - {rows}")

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
  
        if not symbol:
            return apology("Must give symbol")

        stock = lookup(symbol)
        
        if not stock:
            return apology("Symbol does not exist.")
        
        return render_template("quoted.html", name = stock["name"], price = stock["price"], symbol = stock["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Add the user's entry to ...
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Apology if the user’s input is blank or the username already exists.
        # if username == '':
        if not username:
            return apology("provide correct username", 403)
        
        # Render an apology if either input is blank or the passwords do not match.
        # if password == '':
        if not password:
            return apology("provide password", 403)
        
        if not confirmation:
            return apology("Provide confirmation password")

        if password != confirmation:
            return apology("Password don't match", 403)
        
        hash = generate_password_hash(password)

        try:
            # INSERT INTO table_name (column1, column2 ...) VALUES (value1, value2, ...)
            new_user = database.add_user(username, hash)
            print(f"New user - {new_user}")
        except KeyError:
            return apology("USERNAME ALREADY EXIST")

        session["user_id"] = new_user

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")
