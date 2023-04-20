from dash import Dash, Input, Output, State, dcc, html
import dash_bootstrap_components as dbc
from flask import Flask

# Set styles
css = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'

# App Instance
server = Flask(__name__)
app = Dash(server=server, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Investor's Dream"

########################## Navbar ##########################
# Input

# Output
navbar = dbc.NavbarSimple(
    children=[dbc.Nav([
	dbc.NavItem(dbc.NavLink("Current investments", href="#", active=True)),
	dbc.NavItem(dbc.NavLink("Historic investments", href="#")),
	dbc.NavItem(dbc.NavLink("Portfolio planner", href="#")),
	dbc.NavItem(dbc.NavLink("Account management", href="#")),
    ],pills=True)],
    brand="Investor's Dream",
    brand_href="#",
    color="dark",
    dark=True,
    fluid=True,
)

## Callbacks
#@app.callback(
#    output=[
#        Output(component_id="current_investments", component_property="is_open"),
#        Output(component_id="current-investments-popover", component_property="active")],
#    inputs=[
#        Input(component_id="current-investments-popover", component_property="n_clicks")],
#    state=[
#        State("current_investments", "is_open"), State("current-investments-popover", "active")]
#)
#
#def about_popover(n, is_open, active):
#    if n:
#        return not is_open, active
#    return is_open, active
#
########################### Body ##########################
## Input
##inputs = dbc.Form()
## Output
##body = dbc.Row([
##        ## input
##        dbc.Col(md=3),
##        ## output
##        dbc.Col(md=9)
##])
## Callbacks
##@app.callback()
##def function():
##    return 0
#
########################### App Layout ##########################
#app.layout = html.Div("This is the Dash app.")
app.layout = dbc.Container(children=[
#    html.H1("name", id="nav-pills"),
    navbar
#    html.Br(),html.Br(),html.Br(),
#    body
])

########################### Run ##########################
@server.route("/")
def home():
    return "<h1>Investor's Dream</h1>"

#if __name__ == "__main__":
#    app.run_server(debug=True, host="0.0.0.0")
