# version 1
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get:
            return apology("enter valid stock symbol")

        if lookup(request.form.get("stock")) == None:
            return apology("stock not found")
        else:

            return redirect (url_for("quoted"))
    else:
        return render_template("quote.html")

# version 2
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get:
            return apology("enter valid stock symbol")

        stock = lookup(request.form.get("stock"))
        if stock == None:
            return apology("stock not found")
        else:
            quoted(stock)
            return redirect (url_for("quoted"))
    else:
        return render_template("quote.html")

# version 3
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get:
            return apology("enter valid stock symbol")

        stocks = lookup(request.form.get("stock"))
        if stocks == None:
            return apology("stock not found")
        else:
            #make variables for each item in stocks pass those variables to quoted, how??
            quoted(stocks)
    else:
        return render_template("quote.html")
# work on passin value correctly and creating additional tables
@app.route("/quoted")
@login_required
def quoted(stocks):
    """Display stock quote."""
    render_template("quoted.html", **stocks)


# lecture 1:15, make db table to store lookup() values. dump table after