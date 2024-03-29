from flask import Flask, render_template, request, redirect


#Configure App
app = Flask(__name__)

#Variables
symbols= []
portfolio_name = ""
menu = ""
run_analyses = False



@app.route("/")
def index():
    return render_template ("main_menu.html")




@app.route ("/my_portfolios", methods = ["POST", "GET"])
def tickers():
    
    ticker = request.form.get("ticker")
    portfolio_name = request.form.get("portfolio_name")
    timeframe = request.form.get("timeframe")
    if 
    
    if request.form.get("View Portfolio") == "View Portfolio":
        return render_template("my_portfolios.html", symbols=symbols, portfolio_name = portfolio_name, timeframe = timeframe)
    
    if request.form.get("Run Analyses") == "Run Analyses":
        run_analyses = True
        return render_template("my_portfolios.html", symbols=symbols, portfolio_name = portfolio_name, run_analyses = True, timeframe = timeframe)
    
    if not ticker and request.form.get("View Portfolio") != "View Portfolio" and request.form.get("Run Analyses") != "Run Analyses" and request.form.get("Delete Ticker") != "Delete Ticker":
        return "failure"
    
    if request.form.get("Delete Ticker") == "Delete Ticker":
        symbols.remove(ticker)
        return render_template("my_portfolios.html", symbols=symbols, portfolio_name = portfolio_name, timeframe = timeframe)
    
    if request.form.get("View Portfolio") != "View Portfolio":                 
        symbols.append(ticker)
        return render_template("my_portfolios.html", symbols=symbols, portfolio_name = portfolio_name, timeframe = timeframe)





@app.route ("/portfolio_planner", methods = ["POST", "GET"])
def portfolio_planner():
    #TO DO
    return render_template("portfolio_planner.html")

@app.route ("/historical_investment_data", methods = ["POST", "GET"])
def historical_investment_data():
    #TO DO
    return render_template("historical_investment_data.html")

@app.route ("/current_investment_data", methods = ["POST", "GET"])
def current_investment_data():
    #TO DO
    return render_template("current_investment_data.html")

@app.route ("/account_manager", methods = ["POST", "GET"])
def account_manager():
    #TO DO
    return render_template("account_manager.html")

