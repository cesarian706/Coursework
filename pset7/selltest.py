
# portfolio table, most variables are here already
    rows_cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
    cash = rows_cash[0]["cash"]

    # instansiate variables
    table=[]
    total_stock = 0

    # take info from database
    rows = db.execute("SELECT stock_id, sum(shares) FROM portfolio WHERE id = :id GROUP BY stock_id", id=session["user_id"])
    for row in rows:
        symbol = db.execute("SELECT * FROM stocks WHERE stock_id = :stock_id", stock_id=row['stock_id'])
        stock = lookup(symbol[0]["symbol"])
        total = row['sum(shares)'] * stock['price']
        #create dict to append all info from table and lookup to one place
        table_dict = {"symbol": symbol[0]['symbol'], "name": symbol[0]['name'], "shares": row['sum(shares)'], "price": stock['price'], "total": total}
        #append dict to table
        table.append(table_dict)

    # add all stock holdings
    for line in table:
        total_stock += line['total']
    # add holdings plus cash
    total_all = cash + total_stock

if request.method == "POST":
    # make sure user owns stock
    # return apologies for invalid input
    if not request.form.get("symbol"):
        return apology("enter valid stock symbol")
        # could cause problem with invalid input being cast as int
    if int(request.form.get("shares")) < 0:
        return apology("enter valid number of shares")
    #need escape for no stock in portfolio
    for row in rows:
        if row['symbol'] == request.form.get("symbol"):
            if row['sum(shares)'] <= request.form.get("shares") and row['sum(shares)'] > 0:
                #complete sale
                info = lookup(request.form.get("symbol"))
                price = info['price]'] * int(request.form.get("shares"))
                cash_new = cash + price
                shares_new = row['sum(shares)'] - int(request.form.get("shares"))
                db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=cash_new, id=session["user_id"];
                "UPDATE portfolio SET sum(shares) = :shares WHERE id = :id, stock_id= :stock_id", shares=shares_new, id=session["user_id"], stock_id=row['stock_id'])
            else:
                return apology("not enough shares")

# goes at end, ad else for get method
else:
    return render_template("sell.html", table=table, cash=cash, total_all=total_all)

    # set up sell function copy buy










        # check user has stocks to sell
        stock_id = db.execute("SELECT stock_id FROM stocks WHERE symbol = :symbol", symbol=request.form.get("symbol"))
        #need two where conditions look it up
        stock_owned = db.execute("SELECT sum(shares) from PORTFOLIO WHERE id = :id", id=session["user_id"])

        # lookup stock to sell for new price
        stocks = lookup(request.form.get("symbol"))

        # return error if not found
        if stocks == None:
            return apology("stock not found")




        # change to rertrieve cash total into variable for adding or subtracting sale
        rows = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        cash = rows[0]["cash"]
        total = stocks['price'] * shares
        if cash < total:
            return apology("not enough cash")

        else:
            # get stock_id from stock table
            stock_id = db.execute("SELECT stock_id FROM stocks WHERE symbol = :symbol", symbol=stocks['symbol'])
            # insert stock info into database if not already there
            if len(stock_id) != 1:
                db.execute("INSERT INTO stocks (symbol, name) VALUES(:symbol, :name)", symbol=stocks['symbol'],name=stocks['name'])
                stock_id = db.execute("SELECT stock_id FROM stocks WHERE symbol = :symbol", symbol=stocks['symbol'])

            # adjust user cash for new purchase
            new_cash = cash - total
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=new_cash,id=session["user_id"])

            # insert into portfolio with date
            db.execute("INSERT INTO portfolio (id, stock_id, shares, price, date) VALUES(:id, :stock_id, :shares, :price, :date)",
            id=session["user_id"], stock_id=stock_id[0]["stock_id"], shares=request.form.get("shares"), price=stocks['price'], date=datetime.now())
            #TODO return render_template

else:
    return render_template("buy.html")