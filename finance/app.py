import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

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
    user = db.execute(
        "SELECT * FROM users WHERE id = ?", session["user_id"])
    cash = float(user[0]["cash"])
    ports = db.execute(
        "SELECT * FROM Portfolios WHERE id = ? ORDER BY SYMBOL", session["user_id"])
    total_s = cash
    for port in ports:
        prices = lookup(port["SYMBOL"])
        stock_v = prices["price"] * port["SHARES"]
        db.execute("UPDATE Portfolios SET PRICE=?, TOTAL=? WHERE SYMBOL=? AND SHARES=?",
                   prices["price"], stock_v, prices["symbol"], port["SHARES"])
        total_s += float(stock_v)

    return render_template("index.html", ports=ports, cash=usd(cash), total_s=usd(total_s))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if lookup(request.form.get("symbol")) != None:
            q = lookup(request.form.get("symbol"))
            user = db.execute(
                "SELECT * FROM users WHERE id = ?", session["user_id"])
            user_c = user[0]["cash"]
            try:
                shares_c = int(request.form.get("shares"))
            except ValueError:
                return apology("shares must be whole numbers", 400)
            if not shares_c >= 1:
                return apology("shares must be whole numbers", 400)
            transaction_c = q["price"] * int(request.form.get("shares"))
            if user_c < transaction_c:
                return apology("can't afford", 400)
            else:
                if db.execute("SELECT * FROM Portfolios WHERE ID = ? AND SYMBOL=?",  user[0]["id"], q["symbol"]):
                    old = db.execute(
                        "SELECT SHARES, TOTAL FROM Portfolios WHERE ID = ? AND SYMBOL=?",  user[0]["id"], q["symbol"])
                    shares_n = int(old[0]["SHARES"]) + \
                        int(request.form.get("shares"))
                    transaction_cn = float(
                        transaction_c) + float(old[0]["TOTAL"])
                    db.execute("UPDATE Portfolios SET PRICE=?, SHARES=?, TOTAL=? WHERE ID = ? AND SYMBOL= ?",
                               q["price"], shares_n, transaction_cn, user[0]["id"], q["symbol"])
                    db.execute("INSERT INTO History (ID, SYMBOL, PRICE, SHARES, TRANSACTED) VALUES (?,?,?,?,?)",
                               user[0]["id"], q["symbol"], q["price"], request.form.get("shares"), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    db.execute("UPDATE users SET cash= ? WHERE id = ?",
                               user_c - transaction_c, session["user_id"])
                    flash("Bought!")
                    return redirect("/")
                else:
                    db.execute("INSERT INTO Portfolios (ID, SYMBOL, PRICE, SHARES,TOTAL) VALUES (?,?,?,?,?)",
                               user[0]["id"], q["symbol"], q["price"], request.form.get("shares"), transaction_c)
                    db.execute("INSERT INTO History (ID, SYMBOL, PRICE, SHARES, TRANSACTED) VALUES (?,?,?,?,?)",
                               user[0]["id"], q["symbol"], q["price"], request.form.get("shares"), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    db.execute("UPDATE users SET cash= ? WHERE id = ?",
                               user_c - transaction_c, session["user_id"])
                    flash("Bought!")
                    return redirect("/")
        else:
            return apology("invalid symbol", 400)

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    histories = db.execute(
        "SELECT * FROM History WHERE ID=?", session["user_id"])
    return render_template("history.html", histories=histories)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get(
                "username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
    if request.method == "POST":
        if lookup(request.form.get("symbol")) != None:
            q = lookup(request.form.get("symbol"))
            q["price"] = usd(q["price"])
            return render_template("quote.html", q=q)
        else:
            return apology("invalid symbol", 400)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username")):
            return apology("username taken", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match")
        db.execute("INSERT INTO users (username, hash) VALUES(?,?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        if request.form.get("symbol") == None:
            return apology("missing symbol", 400)
        port = db.execute("SELECT SHARES FROM Portfolios WHERE ID = ? AND SYMBOL = ?",
                          session["user_id"], request.form.get("symbol"))
        shares = port[0]["SHARES"]
        user = db.execute("SELECT * FROM users WHERE ID=?", session["user_id"])
        q = lookup(request.form.get("symbol"))
        if int(request.form.get("shares")) > int(shares):
            return apology("too many shares", 400)
        else:
            if (int(request.form.get("shares")) - int(shares)) == 0:
                cash = user[0]["cash"] + \
                    float(q["price"] * int(request.form.get("shares")))
                db.execute("UPDATE users SET cash=?", cash)
                db.execute("DELETE FROM Portfolios WHERE ID=? AND SYMBOL=?",
                           session["user_id"], request.form.get("symbol"))
                db.execute("INSERT INTO History (ID, SYMBOL, PRICE, SHARES, TRANSACTED) VALUES (?,?,?,?,?)",
                           user[0]["id"], q["symbol"], q["price"], int(request.form.get("shares")) * -1, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                flash("Sold!")
                return redirect("/")
            else:
                cash = user[0]["cash"] + \
                    float(q["price"] * int(request.form.get("shares")))
                shares_n = shares - int(request.form.get("shares"))
                total_n = float(shares_n) * q["price"]
                db.execute("UPDATE users SET cash=?", cash)
                db.execute("UPDATE Portfolios SET SHARES=?, TOTAL=? WHERE ID=? AND SYMBOL=?",
                           shares_n, total_n, session["user_id"], request.form.get("symbol"))
                db.execute("INSERT INTO History (ID, SYMBOL, PRICE, SHARES, TRANSACTED) VALUES (?,?,?,?,?)",
                           user[0]["id"], q["symbol"], q["price"], int(request.form.get("shares")) * -1, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                flash("Sold!")
                return redirect("/")

    else:
        symbols = db.execute(
            "SELECT SYMBOL FROM Portfolios WHERE ID = ? ORDER BY SYMBOL", session["user_id"])
        return render_template("sell.html", symbols=symbols)


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    if request.method == "POST":
        user = db.execute("SELECT hash FROM users WHERE ID=?",
                          session["user_id"])
        if not check_password_hash(user[0]["hash"], request.form.get("old_password")):
            return apology("old password inconrrect", 404)
        elif not request.form.get("password"):
            return apology("must provide a new password", 403)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("new passwords don't match")
        db.execute("UPDATE users SET hash=? WHERE id=?", generate_password_hash(
            request.form.get("password")), session["user_id"])
        flash("Password changed successfully!")
        return redirect("/")

    else:
        return render_template("password.html")
