import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    holdings_cumulated = 0

    # retrieving portfolio dict
    list_of_stocks = db.execute("SELECT stock_symbol, stock_volume FROM portfolio WHERE id = ?", session["user_id"])
    if len(list_of_stocks) == 0:
        apology("Empty portfolio", 403)

    # looping over portfolio dict
    for stock in list_of_stocks:

        # suplementing with actual prices
        stock_quote = lookup(stock["stock_symbol"])
        stock["actual_price"] = stock_quote["price"]

        # suplementing with holding values
        stock["holding_value"] = stock["stock_volume"] * stock["actual_price"]
        holdings_cumulated += stock["holding_value"]

    holdings_cumulated = float(round(holdings_cumulated, 2))
    available_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    if not available_cash:
        available_cash = 0
    else:
        available_cash = available_cash[0]["cash"]
        available_cash = float(round(available_cash, 2))

    total = holdings_cumulated + available_cash
    return render_template("index.html", list_of_stocks=list_of_stocks, holdings_cumulated=holdings_cumulated, available_cash=available_cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # POST
    if request.method == "POST":
        stock_symbol = request.form.get("symbol")
        stock_quote = lookup(stock_symbol)
        input_stock_volume = request.form.get("shares")

        # ensure that symbol was submitted
        if not stock_symbol:
            return apology("must provide stock's symbol", 400)

        # ensure symbol exists
        if stock_quote == None:
            return apology("such stock doesn't exist", 400)

        try:
            input_stock_volume = int(input_stock_volume)
        except ValueError:
            return apology("stock's number must be a number", 400)

        # ensure number of shares is positive
        if input_stock_volume < 0:
            return apology("stock's number must be a positive number", 400)

        stock_price = stock_quote["price"]

        # check if the user has enough cash for the purchase
        available_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        if (available_cash[0]["cash"] - input_stock_volume*stock_price < 0):
            return apology("sorry, not enough cash", 403)

        # if such stock already in portfolio
        portfolio = db.execute("SELECT stock_symbol, stock_volume FROM portfolio WHERE stock_symbol = ? AND id = ?", stock_symbol, session["user_id"])
        if len(portfolio) == 1:

            # update user's portfolio stock volume for given stock symbol
            db.execute("UPDATE portfolio SET stock_volume = ? WHERE stock_symbol = ? AND id = ?", portfolio[0]["stock_volume"] + input_stock_volume, stock_symbol, session["user_id"])

        # if stock not yet in portfolio
        elif len(portfolio) == 0:

            # insert stock in portfolio
            db.execute("INSERT INTO portfolio (id, stock_symbol, stock_volume) VALUES (?, ?, ?)", session["user_id"], stock_symbol, input_stock_volume)

        # decreases cash for a given user
        db.execute("UPDATE users SET cash = ? WHERE id = ?", available_cash[0]["cash"] - input_stock_volume*stock_price, session["user_id"])

        # update history
        ct = datetime.datetime.now()
        db.execute("INSERT INTO history (id, transaction_type, stock_symbol, stock_volume, stock_price, timestamp) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], "buy", stock_symbol, input_stock_volume, stock_price, ct)

        # When purchase complete, redirect user to home page
        return redirect("/")

    # GET
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    list_of_transactions = db.execute("SELECT transaction_type, stock_symbol, stock_volume, stock_price, timestamp FROM history WHERE id = ?", session["user_id"])
    return render_template("history.html", list_of_transactions=list_of_transactions)

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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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
    # POST: renders stock quotation for a given symbol
    if request.method == "POST":
        stock_symbol = request.form.get("symbol")
        stock_quote = lookup(stock_symbol)

        # ensure that symbol was submitted
        if not stock_symbol:
            return apology("must provide stock's symbol", 400)

        # ensure symbol exists
        if stock_quote == None:
            return apology("such stock doesn't exist", 400)

        stock_price = stock_quote["price"]
        return render_template("quoted.html", symbol=stock_symbol, price=stock_price)

    # GET: prompt's user for stock's symbol
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # POST
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        existing_users = db.execute("SELECT username FROM users;")

        if not username:
            return apology("must provide username", 400)
        for row in existing_users:
            if row["username"] == username:
                return apology("user already exists", 400)
        if not password == confirmation:
            return apology("passwords don't match", 400)

        # insert new user into users table
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash, cash) VALUES(?, ?, ?)", username, hash, 10000)

        # log user in
        row = db.execute("SELECT id FROM users WHERE username = ?", username)
        session["user_id"] = row[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # GET
    # display registration form
    else:
        return render_template("registration.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # POST
    if request.method == "POST":
        stock_symbol = request.form.get("symbol")
        stock_quote = lookup(stock_symbol)
        input_stock_volume = request.form.get("shares")

        # ensure that symbol was submitted
        if not stock_symbol:
            return apology("must provide stock's symbol", 403)

        #try:
        #    stock_quote = lookup(request.form.get("symbol"))
        #except TypeError:
        #    return apology("Stock's symbol does not exist.", 403)

        # ensure such stock exists
        if stock_quote == None:
            return apology("such stock doesn't exist", 403)

        # retrieve stock's price
        stock_price = stock_quote["price"]

        # ensure user owns such stock
        portfolio = db.execute("SELECT stock_symbol FROM portfolio WHERE stock_symbol = ? AND id = ?", stock_symbol, session["user_id"])
        print(portfolio)
        if len(portfolio) == 0:
            return apology("You don't have that stock.", 403)

        # ensure number of shares is a number
        try:
            input_stock_volume = int(input_stock_volume)
        except ValueError:
            return apology("stock's number must be a number", 403)

        # ensure number of shares is positive
        if input_stock_volume < 0:
            return apology("stock's number must be a positive number", 403)

        # ensure user owns such number of stocks
        list_of_stocks = db.execute("SELECT stock_symbol, stock_volume FROM portfolio WHERE stock_symbol = ? AND id = ?", stock_symbol, session["user_id"])
        if input_stock_volume > list_of_stocks[0]["stock_volume"]:
            return apology("You don't have that many stocks to sell", 403)

        # decrease stock volume for a given user
        db.execute("UPDATE portfolio SET stock_volume = ? WHERE stock_symbol = ? AND id = ?", list_of_stocks[0]["stock_volume"] - input_stock_volume, stock_symbol, session["user_id"])

        # increases cash for a given user
        available_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        db.execute("UPDATE users SET cash = ? WHERE id = ?", available_cash[0]["cash"] + input_stock_volume*stock_price, session["user_id"])

        # update history
        ct = datetime.datetime.now()
        db.execute("INSERT INTO history (id, transaction_type, stock_symbol, stock_volume, stock_price, timestamp) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], "sell", stock_symbol, input_stock_volume, stock_price, ct)

        # When sale complete, redirect user to home page
        return redirect("/")

    # GET
    else:
        return render_template("sell.html")


@app.route("/password", methods=["GET", "POST"])
def password():
    """Change password"""

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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # ensure new password and confirmation match
        if not request.form.get("new_password") == request.form.get("confirmation"):
            return apology("new passwords don't match", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # change password
        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(request.form.get("new_password")), session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("password.html")


