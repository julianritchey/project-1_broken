# Import dependencies
from .nav_bar import navbar
from dash import html, register_page
from flask import session
import dash_bootstrap_components as dbc
import json
import pandas as pd

# Register page with Dash app
register_page(
    __name__,
    name="Historic investments"
)

table1_header = [html.Thead(
        html.Tr([
                html.Th("Portfolio/ticker"),
                html.Th("Open date"),
                html.Th("Open price"),
                html.Th("Current PnL")
            ]))]

table1_body = [html.Tbody([
    html.Tr([html.Td("AAPL"), html.Td(pd.Timestamp.today()), html.Td("$50.00"), html.Td("$6.00")]),
    html.Tr([html.Td("GOOG"), html.Td(pd.Timestamp.today()), html.Td("$50.00"), html.Td("$7.00")]),
    html.Tr([html.Td("SPY"), html.Td(pd.Timestamp.today()), html.Td("$50.00"), html.Td("$8.00")]),
    html.Tr([html.Td("TSLA"), html.Td(pd.Timestamp.today()), html.Td("$50.00"), html.Td("$9.00")])
])]

table2_header = [html.Thead(
        html.Tr([
                html.Th("Portfolio/ticker"),
                html.Th("Open date"),
                html.Th("Open price"),
                html.Th("Current PnL")
            ]))]

table2_body = [html.Tbody([
    html.Tr([html.Td("SPY"), html.Td(pd.Timestamp.today()), html.Td("$50.00"), html.Td("$8.00")]),
    html.Tr([html.Td("TSLA"), html.Td(pd.Timestamp.today()), html.Td("$50.00"), html.Td("$9.00")]),
    html.Tr([html.Td("GOOG"), html.Td(pd.Timestamp.today()), html.Td("$50.00"), html.Td("$7.00")]),
    html.Tr([html.Td("AAPL"), html.Td(pd.Timestamp.today()), html.Td("$50.00"), html.Td("$6.00")])
])]

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Table(
                # using the same table as in the above example
                table1_header + table1_body,
                bordered=True,
                dark=True,
                hover=True,
                responsive=True,
                striped=True,
            )
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Table(
                # using the same table as in the above example
                table2_header + table2_body,
                bordered=True,
                dark=True,
                hover=True,
                responsive=True,
                striped=True,
            )
        ]
    ),
    className="mt-3",
)

# Define page Layout
def layout():
    return html.Div(
        children=[
            html.H2(["Historic investments"], className='mx-3 my-3'),
            dbc.Tabs(
                [
                    dbc.Tab(tab1_content, label="Account 1"),
                    dbc.Tab(tab2_content, label="Account 2"),
                ],
                active_tab="tab-0"
            )
        ]
    )
