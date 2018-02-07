# lookup on each stock for new price
# how much can be done in jinja??

rows_cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
cash = rows_cash[0]["cash"]

# instansiate variables
table=[]
total_stock = 0

# take infor from database
rows = db.execute("SELECT stock_id, sum(shares) FROM portfolio WHERE id = :id GROUP BY stock_id", id=session["user_id"])
for row in rows:
    symbol = db.execute("SELECT * FROM stocks WHERE stock_id = :stock_id", stock_id=row['stock_id'])
    stock = lookup(symbol["symbol"])
    total = row['shares'] * stock['price']
    #create dict to append all info from table and lookup to one place
    table_dict = {"symbol": symbol['symbol'], "name": symbol['name'], "shares": row['shares'], "price": stock['price'], "total": total}
    #append dict to table
    table.append(table_dict)

# add all stock holdings
for line in table:
    total_stock += line['total']
# add holdings plus cash
total_all = cash + total_stock
return render_template("portfolio.html", table=table, cash=cash, total_all=total_all)


price_now = stocks['price']
stock_info = db.execute("SELECT * FROM stocks")
