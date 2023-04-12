from flask import Flask, render_template, request, redirect


#Configure App
app = Flask(__name__)

#Variables
portfolio = ["test"]
portfolio_name = ""
initial_menu = ["Historical Investment Data", "Current Investment Data", "Portfolio Planner", "Account Manager" ]
menu = ""

@app.route("/")
def index():
    return render_template ("main_menu.html", menu0 = initial_menu[0], menu1 =  initial_menu[1], menu2 =  initial_menu[2], menu3 =  initial_menu[3])




@app.route ("/my_portfolios", methods = ["POST", "GET"])
def tickers():
    
    ticker = request.form.get("ticker")
    portfolio_name = request.form.get("portfolio_name")
    if not ticker:
        return "failure"
    portfolio.append(ticker)
    return render_template("my_portfolios.html", portfolio=portfolio, portfolio_name = portfolio_name)





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