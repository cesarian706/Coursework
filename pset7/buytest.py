from datetime import datetime

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    # check method
    if request.method == "POST":
        # return apologies for invalid input
        if not request.form.get("symbol"):
            return apology("enter valid stock symbol")
        if request.form.get("shares") > 0:
            return apology("enter valid number of shares")

        # lookup stock to buy
        stocks = lookup(request.form.get("symbol"))
        # return error if not found
        if stocks == None:
            return apology("stock not found")

        # check that user has enough cash to purchase
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        total = (stocks['price'] * request.form.get("shares"))
        if cash < total:
            return apology("not enough cash")

        else:
            # adjust user cash for new purchase
            new_cash = cash - total
            db.execute("UPDATE cash IN users WHERE cash = :cash", cash=new_cash)
            # insert stock info into database if not already there
            stock = db.execute("SELECT symbol FROM stocks WHERE symbol = :symbol", symbol=stocks['symbol'])
            if stock == None:
                db.execute("INSERT INTO stocks (symbol, name) VALUES(:symbol, :name)", symbol=stocks['symbol'],name=stocks['name'])

            # get stock_id from stock table
            stock_id = db.execute("SELECT stock_id FROM stocks WHERE symbol = :symbol", symbol=stocks['symbol'])

            # insert into portfolio with date
            db.execute("INSERT INTO portfolio (id, stock_id, shares, price, date) VALUES(:id, :stock_id, :shares, :price, :date)",
            id=session["user_id"], stock_id=stock_id, shares=request.form.get("shares"), price=stocks['price'], date=datetime.now())

    else:
        return render_template("buy.html")

        # price has to be updated on every view of portfolio

         # use group by clause to show condensed data










     # check that user has enough cash to purchase

        total = (stocks['price']) * (int(request.form.get("shares"))
        if cash < total:
            return apology("not enough cash")