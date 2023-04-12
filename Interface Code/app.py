from flask import Flask, render_template, request, redirect


#Configure App
app = Flask(__name__)

#Variables
symbols= []
portfolio_name = ""
menu = ""

@app.route("/")
def index():
    return render_template ("main_menu.html")




@app.route ("/my_portfolios", methods = ["POST", "GET"])
def tickers():
    
    
    ticker = request.form.get("ticker")
    portfolio_name = request.form.get("portfolio_name")
    if request.form.get("View Portfolio") == "View Portfolio":
        return render_template("my_portfolios.html", symbols=symbols, portfolio_name = portfolio_name)
    if not ticker and request.form.get("View Portfolio") != "View Portfolio":
        return "failure"
    if request.form.get("View Portfolio") != "View Portfolio":                 
        symbols.append(ticker)
        return render_template("my_portfolios.html", symbols=symbols, portfolio_name = portfolio_name)





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

    # if request.form.get("main_menu") == "menu0":
    #     return render_template ("historical_investment_data.html")
    # elif request.form.get("main_menu") == "menu1":
    #     return render_template("current_investment_data.html")
    # elif request.form.get("main_menu") == "menu2":
    #     return render_template("portfolio_planner.html")
    # elif request.form.get("main_menu") == "menu3":
    #     return render_template("account_manager.html")
    

    # return render_template("plan_portfolio.html", menu = request.form)
    
    #action ="/my_portfolios"