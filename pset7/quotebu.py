
# this version is stable
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
            return render_template("quoted.html", stock = stocks)
    else:
        return render_template("quote.html")