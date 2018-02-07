from flask import Flask, flash, redirect, render_template, request, session, url_for
from cs50 import SQL
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from helpers import *
from datetime import datetime

app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# instantiate database
db = SQL("sqlite:///project.db")

# default route
@app.route("/")
@login_required
def index():
    return redirect(url_for("home"))


@app.route("/login", methods=["GET", "POST"])
def login():
    # forget any user_id
    session.clear()

    if request.method=="POST":
        # ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html")

        # ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html")

        # check that account exists
        rows_acct=db.execute("SELECT acct_id FROM master WHERE acct_name = :acct_name", acct_name=request.form.get("acct_name"))
        if rows_acct != 1:
            render_template("login.html")
        # select all users on account
        rows=db.execute("SELECT * FROM users WHERE acct_id = :acct_id", acct_id=rows_acct[0]["acct_id"])
        # compare login info to users
        for row in rows:
            if request.form.get("username") == row["username"] and pwd_context.verify(request.form.get("password"), row["hash"]):
                session["user_id"] = row["id"]

        return redirect(url_for("index"))

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():

    session.clear()

    if request.method=="POST":
        # check if account already exists
        rows=db.execute("SELECT * FROM master WHERE acct_name=:acct_name", acct_name=request.form.get("acct_name"))
        if len(rows) == 1:
            return render_template("register.html")

        # insert new user to database
        if request.form.get("password") == request.form.get("pwdconfirm") and len(rows) != 1:
            db.execute("INSERT INTO master (acct_name) VALUES(:acct_name)", acct_name=request.form.get("acct_name"))
            rows=db.execute("SELECT acct_id FROM master WHERE acct_name = :acct_name", acct_name=request.form.get("acct_name"))
            db.execute("INSERT INTO users (acct_id, username, hash) VALUES(:acct_id, :username, :hash)", acct_id=rows[0]["acct_id"],username=request.form.get("username"),
            hash=pwd_context.hash(request.form.get("password")))
            rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
            # remember which user has logged in
            session["user_id"] = rows[0]["id"]

            # redirect user to home page
            return redirect(url_for("index"))

    else:
        return render_template("register.html")


@app.route("/add_user", methods=["GET", "POST"])
@login_required
def add_user():
    if request.method == "POST":

        # insert new user to database
        if request.form.get("password") == request.form.get("pwdconfirm"):
            rows_acct=db.execute("SELECT acct_id FROM users WHERE id = :id", id=session["user_id"])
            rows=db.execute("SELECT * FROM users WHERE acct_id = :acct_id", acct_id=rows_acct[0]["acct_id"])
            for row in rows:
                if request.form.get("username") == rows[0]["username"]:
                    return render_template("add_user.html")
            db.execute("INSERT INTO users (acct_id, username, hash) VALUES(:acct_id, :username, :hash)", acct_id=rows[0]["acct_id"],username=request.form.get("username"),
            hash=pwd_context.hash(request.form.get("password")))

        return render_template("add_user.html")
    else:
        return render_template("add_user.html")


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    # create current date and time variables
    date_time = datetime.now()
    date = date_time.date()
    time = date_time.time()

    rows_acct=db.execute("SELECT acct_id FROM users WHERE id = :id", id=session["user_id"])
    rows=db.execute("SELECT * FROM users WHERE acct_id = :acct_id", acct_id=rows_acct[0]["acct_id"])
    events=db.execute("SELECT * FROM events WHERE acct_id = :acct_id", acct_id=rows_acct[0]["acct_id"])
    for event in events:
        if datetime.strptime(event["date"], '%Y-%m-%d') < datetime.now():
            db.execute("DELETE FROM events WHERE date = :date", date=event["date"])

    if request.method == "POST":
        if request.form.get("event") != None and request.form.get("date") != None:
            # create new event
            db.execute("INSERT INTO events (event_name, date, id, acct_id) VALUES(:event_name, :date, :id, :acct_id)", event_name=request.form.get("event"),
            date=request.form.get("date"), id=session["user_id"], acct_id=rows_acct[0]["acct_id"])
        # create new message
        for row in rows:
            if request.form.get("recipient") == row['username'] and rows_acct[0]["acct_id"] == row['acct_id']:
                recipient=db.execute("SELECT id FROM users WHERE username = :username AND acct_id = :acct_id", username=request.form.get("recipient"),acct_id=rows_acct[0]["acct_id"])
                db.execute("INSERT INTO messages (message, id, recipient, date, time) VALUES(:message, :id, :recipient, :date, :time)", message=request.form.get("message"),
                id=session["user_id"], recipient=recipient[0]['id'], date=date, time=time)
        return redirect(url_for("home"))
    # get messages sent and recieved by user, list by date
    messages=db.execute("SELECT * FROM messages WHERE recipient = :recipient OR id = :id ORDER BY date, time ASC", recipient=session["user_id"], id=session["user_id"])

    return render_template("home.html", rows=rows, messages=messages, events=events)



