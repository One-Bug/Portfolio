import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for



# Configure application
app = Flask(__name__)
app.secret_key = "Secret Key"

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    # TODO: Display the entries in the database on index.html
    birthdays = db.execute("SELECT * FROM birthdays")
    return render_template("index.html", birthdays=birthdays)


@app.route("/insert", methods=["POST"])
def insert():
    if request.method == "POST":
        # TODO: Add the user's entry into the database
        name = request.form.get("name")
        if not name:
            return redirect("/")
        month = request.form.get("month")
        if not month:
            return redirect("/")
        try:
            month = int(month)
        except ValueError:
            return redirect("/")
        if month < 1 or month > 12:
            return redirect("/")
        day = request.form.get("day")
        if not day:
            return redirect("/")
        try:
            day = int(day)
        except ValueError:
            return redirect("/")
        if month == (1, 3, 5, 7, 8, 10, 12) and (day < 1 or day > 31):
            return redirect("/")
        if month == (4, 6, 9, 11) and (day < 1 or day > 30):
            return redirect("/")
        if month == 2 and (day < 1 or day > 28):
            return redirect("/")

        db.execute(
            "INSERT INTO birthdays (name, month, day) VALUES (?,?,?)", name, month, day)
        flash("Birthday Inserted Sucessfully")
        return redirect(url_for('index'))


@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "POST":

        name = request.form.get("name")
        if not name:
            return redirect("/")
        month = request.form.get("month")
        if not month:
            return redirect("/")
        try:
            month = int(month)
        except ValueError:
            return redirect("/")
        if month < 1 or month > 12:
            return redirect("/")
        day = request.form.get("day")
        if not day:
            return redirect("/")
        try:
            day = int(day)
        except ValueError:
            return redirect("/")
        if month == (1, 3, 5, 7, 8, 10, 12) and (day < 1 or day > 31):
            return redirect("/")
        if month == (4, 6, 9, 11) and (day < 1 or day > 30):
            return redirect("/")
        if month == 2 and (day < 1 or day > 28):
            return redirect("/")
        id = request.form.get("id")

        db.execute(
            "UPDATE birthdays SET name = ?, month = ?, day = ? WHERE id = ?", name, month, day, id)
        flash("Birthday Updated Sucessfully")
        return redirect(url_for("index"))

@app.route("/delete/<id>", methods = ["GET", "POST"])
def delete(id):
    db.execute("DELETE FROM birthdays WHERE id = ?", id)
    flash("Birthday Deleted Sucessfully")
    return redirect(url_for("index"))
