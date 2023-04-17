# Import dependencies
from .nav_bar import navbar
from dash import ALL, dcc, html, register_page, callback, ctx, Input, MATCH, Output, Patch, State
from dash.exceptions import PreventUpdate
from dotenv import find_dotenv, load_dotenv
from flask import session
from imports import delete_from_assets_portfolios, insert_into_assets, insert_into_assets_portfolios, insert_into_portfolios, select_all_portfolio_data
from os import environ as env
import dash_bootstrap_components as dbc
import json
import pandas as pd
import requests
import sqlalchemy as db

# Register page with Dash app
register_page(
    __name__,
    name="Portfolio planner"
)

# Set database credentials
db_user = env.get('DB_USER')
db_pass = env.get('DB_PASS')

# Connect to database
engine = db.create_engine("postgresql://"+db_user+":"+db_pass+"@localhost:5432/fintech1_db")

# Get ticker data
all_ticker_data = requests.get("https://api.polygon.io/v3/reference/tickers?active=true&apiKey=YmhJNFUowVSt0vCIk3atG9vlr9gzNi6p")
all_ticker_data = all_ticker_data.json()
all_ticker_data = pd.DataFrame(all_ticker_data['results'])
all_ticker_info = all_ticker_data[['ticker', 'name']]

# Define page layout
def layout():
    return html.Div(
        children=[
            dcc.Store(id='ticker_list'),
            dcc.Store(id='portfolio_data'),
            dcc.Store(id='loaded_portfolio_store'),
            dcc.Store(id='portfolio_name_store'),
            dcc.Store(id='load_portfolio_store'),
            dcc.Store(id='save_portfolio_store'),
            html.H2(["Portfolio planner"], className='mx-3 my-3'),
            html.Div(
                [
                    dbc.Row([
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody([
                                    dbc.Row([
                                        dbc.Col([
                                            html.H4("Build your portfolio", className='card-title'),
                                        ]),
                                        dbc.Col(
                                            [
                                                dbc.Button("Load saved portfolio", id='load_portfolio_button', class_name='align-self-end', n_clicks=0),
                                                dbc.Modal(
                                                    [
                                                        dbc.ModalHeader(
                                                            dbc.ModalTitle("Load portfolio"),
                                                        ),
                                                        dbc.ModalBody(
                                                            dcc.Dropdown(
                                                                id='portfolio_dropdown',
                                                            ),
                                                        ),
                                                        dbc.ModalFooter(
                                                            dbc.Button("Load", id="select_portfolio_button", n_clicks=0, disabled=True),
                                                        ),
                                                    ],
                                                    id="load_portfolio_modal",
                                                    is_open=False,
                                                ),
                                            ],
                                            class_name='text-end'
                                        ),
                                    ]),
                                    dbc.InputGroup(
                                        [
                                            dbc.FormFloating([
                                                dbc.Input(placeholder="Ticker", id="ticker_input", style={'text-transform':'uppercase'}),
                                                dbc.Label("Ticker"),
                                            ]),
                                            dbc.Button("Add ticker", id="ticker_button", n_clicks=0),
                                        ],
                                        class_name='mt-3',
                                    ),
                                    dbc.Collapse(
                                        html.Div([
                                            dbc.Label("Ticker is invalid"),
                                        ]),
                                        id="ticker_collapse",
                                        is_open=False,
                                        style={'color':'#e74c3c'},
                                    ),
                                    dbc.ListGroup(id="ticker_group", className='mt-3'),
                                    # dbc.Label(id="test"),
                                    dbc.FormFloating([
                                        dbc.Input(placeholder="Portfolio name", id="portfolio_name_input"),
                                        dbc.Label("Portfolio name"),
                                    ],
                                    class_name='mt-3'),
                                    dbc.ButtonGroup(
                                        [
                                            dbc.Button("Save portfolio", id='save_portfolio_button', color='success', disabled=True, n_clicks=0),
                                            dbc.Alert(
                                                id="portfolio_saved_alert",
                                                color='success',
                                                is_open=False,
                                                dismissable=True,
                                                duration=5000,
                                                style={"position": "fixed", "bottom": "0px", "text-align": "center", "width": "100%"},
                                            ),
                                            dbc.Button("Clear portfolio", id='clear_portfolio_button', color='danger', n_clicks=0, outline=True),
                                            dbc.Modal(
                                                [
                                                    dbc.ModalHeader(
                                                        dbc.ModalTitle("Clear portfolio")
                                                    ),
                                                    dbc.ModalBody("Are you sure you wish to clear the current portfolio data?"),
                                                    dbc.ModalFooter(
                                                        dbc.Button(
                                                            "Confirm", id="confirm_clear_portfolio_button", color="danger", n_clicks=0, outline=True
                                                        )
                                                    ),
                                                ],
                                                id="clear_portfolio_modal",
                                                is_open=False,
                                            ),
                                        ],
                                        class_name='mt-3',
                                        style={'width':'100%'},
                                        vertical=True,
                                    )
                                ])
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody([
                                    html.H4("Run portfolio simulations:", className='card-title'),
                                    dbc.FormFloating(
                                        [
                                            dbc.Input(placeholder="Investment period (years)", id="investment_period", type='number'),
                                            dbc.Label("Enter investment period (years)"),
                                        ],
                                        class_name='mt-4',
                                    ),
                                    dbc.ListGroup(id="weight_group", className='mt-3'),
                                    dbc.Button("Run simulation", class_name='mt-3', color='primary', style={'width':'100%'}),
                                    dbc.Label(id="test")
                                ])
                            )
                        )
                    ])
                ]
            )
        ]
    )

# Define callback function for loading saved profiles
@callback(
    Output("load_portfolio_modal", "is_open", allow_duplicate=True),
    Output("portfolio_dropdown", "options"),
    Output('portfolio_data', 'data'),
    Input("load_portfolio_button", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks):
    if n_clicks==0:
        return PreventUpdate
    portfolio_data = select_all_portfolio_data(engine)
    portfolio_names = portfolio_data['portfolio_name'].unique()
    portfolio_list = []
    for name in portfolio_names:
        portfolio_list.append({'label':name, 'value':name})
    return True, portfolio_list, portfolio_data.to_json()

# Define callback function for selecting portfolio to be loaded
@callback(
    Output('select_portfolio_button', 'disabled'),
    Input('portfolio_dropdown', 'value'),
    prevent_initial_call=True,
)
def select_portfolio(selected_portfolio):
    if selected_portfolio:
        return False
    else:
        return True

# Define callback function for loading a saved portfolio
@callback(
    Output('portfolio_name_input', 'value', allow_duplicate=True),
    Output('investment_period', 'value', allow_duplicate=True),
    Output('ticker_group', 'children', allow_duplicate=True),
    Output('weight_group', 'children', allow_duplicate=True),
    Input('loaded_portfolio_store', 'data'),
    prevent_initial_call=True,
)
def load_portfolio(loaded_portfolio):
    if loaded_portfolio:
        portfolio_name = ''
        investment_period = 0
        ticker_list = []
        loaded_portfolio = pd.read_json(loaded_portfolio)
        patched_ticker_children = Patch()
        patched_weight_children = Patch()

        for i in range(len(loaded_portfolio)):
            portfolio_name = loaded_portfolio.loc[i, 'portfolio_name']
            ticker = loaded_portfolio.loc[i, 'ticker']
            ticker_name = loaded_portfolio.loc[i, 'ticker_name']
            weight = loaded_portfolio.loc[i, 'weight']
            investment_period = loaded_portfolio.loc[i, 'investment_period']
            ticker_list.append(ticker)
            new_ticker = dbc.ListGroupItem(ticker + " - " + ticker_name, id={'ticker':ticker, 'ticker_name':ticker_name})
            patched_ticker_children.append(new_ticker)
            new_weight = dbc.ListGroupItem(
                dbc.InputGroup([
                    dbc.Input(disabled=True, style={'width':'60%'}, value="Portfolio weight (in decimals) for "+ticker),
                    dbc.Input(id={'type':'weight', 'ticker':ticker}, type='number', value=weight)
                ])
            )
            patched_weight_children.append(new_weight)
        return portfolio_name, investment_period, patched_ticker_children, patched_weight_children
    else:
        return None, None, [], []

# Define callback function for validating ticker input
@callback(
    Output('ticker_input', 'invalid'),
    Output('ticker_input', 'valid'),
    Output('ticker_input', 'value'),
    Output('ticker_collapse', 'is_open'),
    Input('ticker_input', 'value'),
    prevent_initial_call=True
)
def validate_ticker_input(ticker):
    if ticker:
        ticker = ticker.upper()
        if ticker in all_ticker_info['ticker'].to_list():
            invalid = False
            valid = True
            collapse = False
        elif ticker == '':
            invalid = False
            valid = False
            collapse = False
        else:
            invalid = True
            valid = False
            collapse = True
        return invalid, valid, ticker, collapse
    else:
        return None, None, None, False

# Define callback function for adding ticker to portfolio
@callback(
    Output('ticker_group', 'children'),
    Output('weight_group', 'children'),
    Output('ticker_input', 'value', allow_duplicate=True),
    Output('ticker_list', 'data', allow_duplicate=True),
    Input('ticker_button', 'n_clicks'),
    State('ticker_input', 'value'),
    State('ticker_group', 'children'),
    State('weight_group', 'children'),
    State('ticker_list', 'data'),
    prevent_initial_call=True
)
def add_ticker(n_clicks, ticker, ticker_children, weight_children, ticker_list):
    if n_clicks==0:
        raise PreventUpdate
    
    if not ticker_list:
        ticker_list = []
    if ticker in all_ticker_info['ticker'].to_list() and ticker not in ticker_list:
        patched_ticker_children = Patch()
        ticker_name = ''
        for i in range(len(all_ticker_info)):
            if all_ticker_info.loc[i, "ticker"]==ticker:
                ticker_name = all_ticker_info.loc[i, 'name']
        new_ticker = dbc.ListGroupItem(ticker + " - " + ticker_name, id={'ticker':ticker, 'ticker_name':ticker_name})
        patched_ticker_children.append(new_ticker)
        ticker_list.append(ticker)
        patched_weight_children = Patch()
        new_weight = dbc.ListGroupItem(
            dbc.InputGroup([
                dbc.Input(value="Portfolio weight (in decimals) for "+ticker, disabled=True, style={'width':'60%'}),
                dbc.Input(id={'type':'weight', 'ticker':ticker}, type='number')
            ])
        )
        patched_weight_children.append(new_weight)
        return patched_ticker_children, patched_weight_children, None, ticker_list
    else:
        return ticker_children, weight_children, ticker, ticker_list

# Define callback function for displaying modal to confirm clearing portfolio
@callback(
    Output('clear_portfolio_modal', 'is_open', allow_duplicate=True),
    Input('clear_portfolio_button', 'n_clicks'),
    prevent_initial_call=True,
)
def close_portfolio_modal(n_clicks):
    if n_clicks==0:
        return PreventUpdate
    
    return True

# Define callback function for clearing portfolio
@callback(
    Output('ticker_input', 'value', allow_duplicate=True),
    Output('portfolio_name_input', 'value', allow_duplicate=True),
    Output('investment_period', 'value', allow_duplicate=True),
    Output('ticker_group', 'children', allow_duplicate=True),
    Output('weight_group', 'children', allow_duplicate=True),
    Output('clear_portfolio_modal', 'is_open'),
    Output('load_portfolio_modal', 'is_open'),
    Output('ticker_list', 'data'),
    Output('loaded_portfolio_store', 'data'),
    Output('portfolio_dropdown', 'value'),
    Output('portfolio_data', 'data', allow_duplicate=True),
    Input('confirm_clear_portfolio_button', 'n_clicks'),
    Input('select_portfolio_button', 'n_clicks'),
    State('portfolio_dropdown', 'value'),
    State('portfolio_data', 'data'),
    prevent_initial_call=True,
)
def clear_portfolio(clear_n, select_n, selected_portfolio, portfolio_data):
    if clear_n==0 and select_n==0:
        return PreventUpdate
    
    trigger = ctx.triggered_id
    loaded_portfolio = None
    if trigger=='select_portfolio_button':
        portfolio_data = pd.read_json(portfolio_data)
        loaded_portfolio = portfolio_data[portfolio_data['portfolio_name'].str.match(selected_portfolio)]
        print(loaded_portfolio)
        return None, None, None, [], [], False, False, None, loaded_portfolio.to_json(), None, None
    else:
        return None, None, None, [], [], False, False, None, loaded_portfolio, None, None

# Define callback function for enabling button to save portfolio
@callback(
    Output('save_portfolio_button', 'disabled'),
    Input('ticker_group', 'children'),
    Input({'type':'weight', 'ticker':ALL}, 'value'),
    Input('portfolio_name_input', 'value'),
    Input('investment_period', 'value'),
    prevent_initial_call=True,
)
def enable_save_portfolio(tickers, weights, portfolio_name, investment_period):
    total_weight = 0
    for weight in weights:
        if weight:
            total_weight += weight
        else:
            return True
    if total_weight==1 and tickers and portfolio_name and investment_period:
        return False
    else:
        return True

# Define callback function for saving portfolio
@callback(
    Output('portfolio_name_store', 'data'),
    Output('portfolio_saved_alert', 'is_open'),
    Output('portfolio_saved_alert', 'children'),
    Input('save_portfolio_button', 'n_clicks'),
    State('portfolio_name_input', 'value'),
    State('investment_period', 'value'),
    State('ticker_group', 'children'),
    State({'type':'weight', 'ticker':ALL}, 'value'),
    prevent_initial_call=True,
)
def save_portfolio(n_clicks, portfolio_name, investment_period, ticker_group, weight_group):
    if n_clicks==0:
        return PreventUpdate
    
    asset_group = []
    for ticker in ticker_group:
        ticker_symbol = ticker['props']['id']['ticker']
        ticker_name = ticker['props']['id']['ticker_name']
        asset_id = insert_into_assets(ticker_symbol, ticker_name, engine)
        asset_group.append(asset_id['asset_id'][0])
    portfolio_id = insert_into_portfolios(portfolio_name, investment_period, engine)
    portfolio_id = portfolio_id['portfolio_id'][0]
    delete_from_assets_portfolios(portfolio_id, engine)
    for i in range(len(asset_group)):
        insert_into_assets_portfolios(portfolio_id, asset_group[i], weight_group[i], engine)
    notice = 'Portfolio "'+portfolio_name+'" has been saved.'
    return portfolio_name, True, notice