# Import dependencies
from .nav_bar import navbar
from dash import html, register_page
from flask import session
import dash_bootstrap_components as dbc

# Register page with Dash app
register_page(
    __name__,
    name="Account management"
)

# Define page layout
def layout():
    return html.Div(
        children=[
            html.H1(["Welcome, "+session.get('user')['userinfo']['given_name']]),
            html.H3(children="Here you will manage your account.")
        ]
    )