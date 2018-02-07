from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from datetime import datetime

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        # ensure valid input
        str = request.form.get("money")
        if str.isnumeric() == False:
            return apology("enter positive numeric value")
        money = request.form.get("money")
        if float(money) < 0:
            return apology("enter positive value")
        # add new cash to balace
        cash_old = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        cash_money = money + cash_old[0]["cash"]
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=cash_money, id=session["user_id"])
        # reload page with update
        return redirect(url_for("index"))

    # get user's cash balance
    rows_cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
    cash = rows_cash[0]["cash"]

    # instansiate variables
    table=[]
    total_stock = 0

    # get portfoilio table
    rows = db.execute("SELECT stock_id, sum(shares) FROM portfolio WHERE id = :id GROUP BY stock_id", id=session["user_id"])
    # iterate rows to create comprehensive dict
    for row in rows:
        # get stock information
        symbol = db.execute("SELECT * FROM stocks WHERE stock_id = :stock_id", stock_id=row['stock_id'])
        # get current stock price
        stock = lookup(symbol[0]["symbol"])
        # get total value of stock holding
        total = row['sum(shares)'] * stock['price']
        #create dict to append all info from database and lookup to one place
        table_dict = {"symbol": symbol[0]['symbol'], "name": symbol[0]['name'], "shares": row['sum(shares)'], "price": usd(stock['price']), "total": usd(total)}
        #append to dict
        table.append(table_dict)
        # increment total value of holdings
        total_stock += total

    # add holdings plus cash
    total_all = cash + total_stock
    return render_template("portfolio.html", table=table, cash=usd(cash), total_all=usd(total_all))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
        # check method
    if request.method == "POST":
        # return apologies for invalid input
        if not request.form.get("symbol"):
            return apology("enter valid stock symbol")

        str = request.form.get("shares")
        if str.isnumeric() == False:
            return apology("enter numeric value")

        if int(request.form.get("shares")) < 0:
            return apology("enter valid number of shares")

        # lookup stock to buy
        stocks = lookup(request.form.get("symbol"))
        shares = int(request.form.get("shares"))
        # return error if not found
        if stocks == None:
            return apology("stock not found")

        # check that user has enough cash to purchase
        rows = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        cash = rows[0]["cash"]
        total = stocks['price'] * shares
        if cash < total:
            return apology("not enough cash")

        # get stock_id from stock table
        stock_id = db.execute("SELECT stock_id FROM stocks WHERE symbol = :symbol", symbol=stocks['symbol'])
        # insert stock info into database if not already there
        if len(stock_id) != 1:
            db.execute("INSERT INTO stocks (symbol, name) VALUES(:symbol, :name)", symbol=stocks['symbol'],name=stocks['name'])
            stock_id = db.execute("SELECT stock_id FROM stocks WHERE symbol = :symbol", symbol=stocks['symbol'])

        # insert into portfolio with date
        price = stocks['price']
        db.execute("INSERT INTO portfolio VALUES(:id, :stock_id, :shares, :price, :date)",id=session["user_id"], stock_id=stock_id[0]["stock_id"], shares=shares, price=price, date=datetime.now())
        # adjust user cash for new purchase
        new_cash = cash - total
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=new_cash,id=session["user_id"])
        return redirect(url_for("history"))
    # render template for GET method
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    # display purchases and sales information
    rows = db.execute("SELECT * FROM portfolio JOIN stocks ON portfolio.stock_id = stocks.stock_id WHERE id = :id", id=session["user_id"])
    table = []
    for row in rows:
        table_dict = {"symbol": row['symbol'], "shares": row['shares'], "price": usd(row['price']), "date": row['date']}
        table.append(table_dict)
    return render_template("history.html", rows=table)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # ensure valid input
        if not request.form.get:
            return apology("enter valid stock symbol")
        # ensure stock exists
        stocks = lookup(request.form.get("stock"))
        if stocks == None:
            return apology("stock not found")
        else:
            # display stock info
            return render_template("quoted.html", stock = stocks)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # check for blank fields
        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")
        # ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password")
        # ensure reasonable username
        if len(request.form.get("username")) < 3 or len(request.form.get("username")) > 15:
            return apology("username must be 3 to 15 characters")
        # check pasword entry
        if request.form.get("password") != request.form.get("pwdconfirm"):
            return apology("password does not match")

        # check if username provided exists already
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        if len(rows) == 1:
            return apology("username already exists")

        # insert new user to database
        if request.form.get("password") == request.form.get("pwdconfirm") and len(rows) != 1:
            db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"),
            hash=pwd_context.hash(request.form.get("password")))

            rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
            # remember which user has logged in
            session["user_id"] = rows[0]["id"]

            # redirect user to home page
            return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    if request.method == "POST":
        # return apologies for invalid input
        if not request.form.get("symbol"):
            return apology("enter valid stock symbol")
        # check that user input is numeric
        str = request.form.get("shares")
        if str.isnumeric() == False:
            return apology("enter numeric value")
        # check that it is a positive value greater than 0
        if int(request.form.get("shares")) < 0:
            return apology("enter valid number of shares")

        # instansiate variables
        rows_cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        cash = rows_cash[0]["cash"]
        stock = request.form.get("symbol")
        rows = db.execute("SELECT stock_id, sum(shares) FROM portfolio WHERE id = :id GROUP BY stock_id", id=session["user_id"])
        # check for stock in portfolio
        for row in rows:
            symbol = db.execute("SELECT symbol FROM stocks WHERE stock_id = :stock_id", stock_id=row['stock_id'])
            if symbol[0]["symbol"] == stock.upper():
                if row['sum(shares)'] >= int(request.form.get("shares")) and row['sum(shares)'] > 0:
                    #complete sale
                    info = lookup(request.form.get("symbol"))
                    price = info['price']
                    price_total = price * int(request.form.get("shares"))
                    cash_new = cash + price_total
                    shares_new = - int(request.form.get("shares"))
                    # update user info
                    db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=cash_new, id=session["user_id"])
                    db.execute("INSERT INTO portfolio (id, stock_id, shares, price, date) VALUES(:id, :stock_id, :shares, :price, :date)",
                    id=session["user_id"], stock_id=row['stock_id'], shares=shares_new, price=price, date=datetime.now())
                else:
                    return apology("not enough shares")
        # redirect to updated table
        return redirect(url_for("history"))
    else:
        # instansiate variables
        rows_cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        cash = rows_cash[0]["cash"]
        table=[]
        total_stock = 0

        # take info from database
        rows = db.execute("SELECT stock_id, sum(shares) FROM portfolio WHERE id = :id GROUP BY stock_id", id=session["user_id"])
        for row in rows:
            symbol = db.execute("SELECT * FROM stocks WHERE stock_id = :stock_id", stock_id=row['stock_id'])
            stock = lookup(symbol[0]["symbol"])
            total = row['sum(shares)'] * stock['price']
            #create dict to append all info from table and lookup to one place
            table_dict = {"symbol": symbol[0]['symbol'], "name": symbol[0]['name'], "shares": row['sum(shares)'], "price": usd(stock['price']), "total": usd(total)}
            #append dict to table
            table.append(table_dict)
            # add all stock holdings
            total_stock += total

        # add holdings plus cash
        total_all = cash + total_stock
        # display sell page if method GET
        return render_template("sell.html",table=table, cash=usd(cash), total_all=usd(total_all))

