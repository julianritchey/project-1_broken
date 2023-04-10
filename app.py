from flask import Flask, render_template, request, redirect

#Configure App
app = Flask(__name__)

#Variables
portfolio = ["test"]
portfolio_name = ""


@app.route("/")
def index():
    return render_template ("index.html")

@app.route ("/my_portfolios", methods = ["POST"])
def tickers():
    ticker = request.form.get("ticker")
    portfolio_name = request.form.get("portfolio_name")
    if not ticker:
        return "failure"
    portfolio.append(ticker)
    return render_template("my_portfolio.html", portfolio=portfolio, portfolio_name = portfolio_name)

@app.route ("/portfolio_planner", methods = ["POST"])
def portfolios():
    #TO DO
    return render_template("portfolio_planner.html")
    print (portfolio)
    
    
