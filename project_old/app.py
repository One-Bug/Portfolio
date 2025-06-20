import os
import jwt


from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, FileField, validators, DecimalField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask import Flask, flash, redirect, render_template, request, session, jsonify, url_for, render_template_string, Response
from itsdangerous import URLSafeTimedSerializer as Serializer
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from threading import Thread
from functools import wraps
from flask_login import UserMixin
from flask_session import Session
from werkzeug.utils import secure_filename

from helpers import apology, login_required


app = Flask(__name__)


SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret'

app.config['SECRET_KEY'] = SECRET_KEY
app.config["JWT_SECRET_KEY"] = 'jwt_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "2eliot22061@gmail.com" #temporal mail its gonna be on the video but no on the final code. Use a email to try yourself
app.config['MAIL_PASSWORD'] = "tkud aknt waux olss"
mail = Mail(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    hash = db.Column(db.String, nullable=False)

    def get_reset_token(self, expires=500):
        s = Serializer(app.config['SECRET_KEY'], expires)
        return s.dumps(self.email, salt=self.hash)

    def verify_reset_token(token: str, id: int):

        user = Users.query.filter_by(id=id).first()

        if user is None:
            return None
        s = Serializer(app.config['SECRET_KEY'])
        try:
            token_user_email = s.loads(token, salt=user.hash)
            print(token_user_email)
        except Exception as e:
            print(e)
            return None
        if not token_user_email == user.email:
            return None
        return user

    def __repr__(self):
        return f'{self.username} : {self.email} : {self.hash}'


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    session_id = db.Column(db.Integer, nullable=False)
    item = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Numeric)
    price = db.Column(db.Numeric)
    description = db.Column(db.String)
    img = db.Column(db.Text)
    mimetype = db.Column(db.Text)


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return apology("Missing Token", 401)
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return apology("Invalid Token", 400)
    return decorated


class AddForm(FlaskForm):
    item = StringField(
        "Item", [validators.DataRequired(message="Item name required")])
    amount = IntegerField("Amount")
    cost = DecimalField('Cost')
    price = DecimalField('Price')
    description = TextAreaField(u'Description')


class UpdateForm(FlaskForm):
    item = StringField(
        "Item", [validators.DataRequired(message="Item name required")])
    amount = IntegerField("Amount")
    cost = DecimalField('Cost')
    price = DecimalField('Price')
    description = TextAreaField(u'Description')


def send_email(user):
    token = user.get_reset_token()
    id = user.id
    msg = Message()
    msg.subject = "Password Reset"
    msg.recipients = [user.email]
    msg.sender = '2eliot22061@gmail.com'
    msg.body = f''' to reset your password follow the link below.



    {url_for('password_forgot', token=token, id=id, _external=True)}


     If you didn't request a password reset. Please ignore this message.


    '''
    Thread(target=send_email, args=(app, msg)).start()
    mail.send(msg)


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    # db.create_all()
    data = Data.query.filter_by(session_id=session["user_id"])
    return render_template("index.html", data=data)


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()
    session["logged_in"] = False

    if request.method == "POST":

        if not request.form.get("username"):
            flash("must provide username", "error")
            return render_template("login.html")

        elif not request.form.get("password"):
            flash("must provide password", "error")
            return render_template("login.html")

        rows = Users.query.filter_by(
            username=request.form.get("username")).first()
        if rows == None:
            flash("invalid username and/or password", "error")
            return render_template("login.html")
        if not check_password_hash(
            rows.hash, request.form.get("password")
        ):
            flash("invalid username and/or password", "error")
            return render_template("login.html")

        token = jwt.encode({
            'user': request.form.get("username"),
            'expiration': str(datetime.utcnow() + timedelta(seconds=120))
        },
            app.config['SECRET_KEY'])
        session["logged_in"] = True
        session["user_id"] = rows.id

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()
    session["logged_in"] = False

    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        test_u = Users.query.filter_by(
            username=request.form.get("username")).first()
        test_e = Users.query.filter_by(
            email=request.form.get("email")).first()
        if not request.form.get("name"):
            flash("must provide name", "error")
            return render_template("register.html")
        if not request.form.get("last_name"):
            flash("must provide last name", "error")
            return render_template("register.html")
        if not request.form.get("email"):
            flash("must provide email", "error")
            return render_template("register.html")
        elif test_e:
            flash("email already in use", "error")
            return render_template("register.html")
        if not request.form.get("gender"):
            flash("must provide gender", "error")
            return render_template("register.html")
        if not request.form.get("username"):
            flash("must provide username", "error")
            return render_template("register.html")
        elif test_u:
            flash("username taken", "error")
            return render_template("register.html")
        elif not request.form.get("password"):
            flash("must provide password", "error")
            return render_template("register.html")
        if request.form.get("password") != request.form.get("confirmation"):
            flash("passwords don't match", "error")
            return render_template("register.html")
        new = Users(name=request.form.get("name"), last_name=request.form.get("last_name"), gender=request.form.get("gender"), email=request.form.get("email"), username=request.form.get(
            "username"), hash=generate_password_hash(request.form.get("password")))
        db.session.add(new)
        db.session.commit()
        token = jwt.encode({
            'user': request.form.get("username"),
            'expiration': str(datetime.utcnow() + timedelta(seconds=120))
        },

            app.config['SECRET_KEY'])
        session["logged_in"] = True
        session["user_id"] = new.id
        flash("user registered successfully", "success")
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    if request.method == "POST":
        user = Users.query.filter_by(id=session["user_id"]).first()
        if not check_password_hash(user.hash, request.form.get("old_password")):
            flash("old password inconrrect", "error")
            return render_template("password.html")
        elif not request.form.get("password"):
            flash("must provide a new password", "error")
            return render_template("password.html", "error")
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("new passwords don't match", "error")
            return render_template("password.html")
        user.hash = generate_password_hash(
            request.form.get("password"))
        db.session.commit()
        flash("Password changed successfully!", "success")
        return redirect("/")

    else:
        return render_template("password.html")


@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        if not request.form.get("email"):
            flash("must provide email", "error")
            return render_template("forgot.html")
        elif not Users.query.filter_by(
                email=request.form.get("email")).first():
            flash("email is not registered", "error")
            return render_template("forgot.html")
        else:
            user = Users.query.filter_by(
                email=request.form.get("email")).first()
            send_email(user)
            flash("Reset request sent. Please go check mail", "success")
            return render_template("login.html")
    return render_template("forgot.html")


@app.route("/password_forgot/<token>/<int:id>", methods=["GET", "POST"])
def password_forgot(token, id):
    if request.method == "POST":
        user = Users.verify_reset_token(token, id)
        flash(id)
        if not user:
            flash("Password Reset Error")
            return redirect("/register")
        if not request.form.get("password"):
            flash("must provide a new password", "error")
            return render_template("password_forgot.html", "error")
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("new passwords don't match", "error")
            return render_template("password_forgot.html")
        user.hash = generate_password_hash(request.form.get("password"))
        db.session.commit()
        flash("password updated! please login", "success")
        return redirect("/login")
    else:
        idp = id
        tokenp = token
        return render_template("password_forgot.html", idp=idp, tokenp=tokenp)




@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = AddForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if not form.item.data:
                flash("item name required", "error")
                return render_template("/add")
            user = Data.query.filter_by(item=form.item.data).first()
            pic = request.files['img']
            if pic:
                name = secure_filename(pic.filename)
                mimetype = pic.mimetype
                data = Data(session_id=session["user_id"], item=form.item.data, amount=form.amount.data, cost=form.cost.data,
                        price=form.price.data, description=form.description.data, img=pic.read(), mimetype=mimetype)
            else:
                pic= ""
                mimetype = ""
                data = Data(session_id=session["user_id"], item=form.item.data, amount=form.amount.data, cost=form.cost.data,
                            price=form.price.data, description=form.description.data, img=pic, mimetype=mimetype)
            db.session.add(data)
            db.session.commit()
            return redirect("/")
    else:
        return render_template("add.html", form=form)


@app.route("/img/<int:id>")
@login_required
def img(id):
    img = Data.query.filter_by(id=id).first()
    if not img:
        return redirect("/")
    return Response(img.img, mimetype=img.mimetype)


@app.route("/update/<id>", methods=["GET", "POST"])
@login_required
def update(id):
    form = UpdateForm()
    data = Data.query.filter_by(id=id).first()
    if request.method == "POST":
        if form.validate_on_submit():
            print(data)
            data.item = form.item.data
            data.amount = form.amount.data
            data.cost = form.cost.data
            data.price = form.price.data
            data.description = form.description.data
            pic = request.files["img"]
            if pic:
                name = secure_filename(pic.filename)
                mimetype = pic.mimetype
                data.img = pic.read()
                data.mimetype = mimetype
            db.session.commit()
            return redirect("/")
    else:
        form.item.data = data.item
        form.amount.data = data.amount
        form.cost.data = data.cost
        form.price.data = data.price
        form.description.data = data.description
        return render_template("update.html", form=form, id=id)


@app.route("/delete/<id>")
@login_required
def delete(id):
    data = Data.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect("")


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
#Sorry if you found some trash code but I was on a hurry. Hope you understand.
