# Historic Stock Data Dashboard

# Imports
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from dash.dependencies import Output, Input, State
import pandas_datareader.data as web
from datetime import datetime as dt
import pandas as pd
import numpy as np

app = dash.Dash(__name__)
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# Main Div (1st level)
app.layout = html.Div([

    # Sub-Div (2nd level)
    # Dashboard Title
    html.Div([html.H1(children='Stock Price Dashboard',
                      className='twelve columns',
                      style={'text-align': 'center',
                             'margin': '2% 0% 3% 0%',
                             'letter-spacing': 2})
              ], className='row'),

    # Sub-Div (2nd level)
    # DropDown
    html.Div([dcc.Dropdown(id='symbols-dropdown',
                           multi=True,
                           placeholder="Please select a stock",
                           style={'height': '40px',
                                  'fontSize': 20,
                                  'margin': '2% 0% 7% 0%',
                                  'textAlign': 'center'})
              ], style={'align': 'center'}, className='row six columns offset-by-three'),

    # Sub-Div (2nd level)
    # Date picker and Button
    html.Div([
        # Sub-Div (3rd level)
        # Date Picker
        html.Div([dcc.DatePickerRange(id='date-picker-range',
                                      min_date_allowed=dt(2015, 1, 1),
                                      max_date_allowed=dt(2018, 9, 30),
                                      initial_visible_month=dt(2018, 6, 1),
                                      end_date=dt(2018, 6, 30))
                  ], style={'text-align': 'center'}, className='three columns offset-by-three'),
        # Update Button
        html.Button(id='update-button',
                    children='Update',
                    n_clicks=0,
                    style={'fontSize': 20,
                           'fontWeight': 'normal',
                           'height': '50px',
                           'width': '150px',
                           'marginLeft': '25px',
                           'marginTop': '1.5%'},
                    className='two columns button-primary')

    ], style={'margin': '6% 0% 6% 12.5%', 'float': 'center'}, className='row'),

    # Sub-Div (2nd level)
    # Stocks Graph
    html.Div([dcc.Graph(id='data-plot')], className='row')

], className='ten columns offset-by-one')

# Getting the stock names & symbols and also cleaning the data
symbols = web.get_iex_symbols()
symbols_list = pd.DataFrame({'symbol': symbols['symbol'], 'name': symbols['name']})
symbols_list['name'].replace('', np.nan, inplace=True)
symbols_list['symbol'].replace('', np.nan, inplace=True)
symbols_list.dropna(inplace=True)

# Removing stocks with very long names
mask = symbols_list['name'].str.len() < 40
symbols_list = symbols_list.loc[mask]
symbols_list = symbols_list.reset_index(drop=True)


# Callback functions for updating the dashboard components
@app.callback(Output('symbols-dropdown', 'options'),
              [Input('symbols-dropdown', 'value')])
def symbols_names_callback(value):
    options_list = [{'label': symbols_list.iloc[i]['name'],
                     'value': symbols_list.iloc[i]['symbol']} for i in range(0, len(symbols_list))]

    return options_list


@app.callback(Output('data-plot', 'figure'),
              [Input('update-button', 'n_clicks')],
              [State('symbols-dropdown', 'value'),
               State('date-picker-range', 'start_date'),
               State('date-picker-range', 'end_date')])
def graph_callback(n_clicks, selected_symbols, start_date, end_date):
    if n_clicks > 0:
        try:
            df_list = [web.DataReader(symbol, 'iex', start_date, end_date) for symbol in selected_symbols]

            # Naming the DataFrames
            for i in range(0, len(df_list)):
                df_list[i].name = selected_symbols[i]

            # Formatting a graph title
            symbols = ""
            for symbol in selected_symbols:
                symbols = symbols + "'" + symbol + "', "
            symbols = symbols[:-2]

            # Making a list of all the available dates in the range selected
            dates = [i for i in df_list[0].index]

            data = [go.Scatter(x=dates, y=df['close'], mode='lines', name=df.name) for df in df_list]
            layout = go.Layout(title='{} closing prices'.format(symbols),
                               xaxis={'title': 'Date'},
                               yaxis={'title': 'Closing Price'},
                               font={'family': 'verdana', 'size': 15, 'color': '#606060'})
            fig = dict(data=data, layout=layout)
            return fig

        except Exception as e:
            print(e)


# Running the server
if __name__ == '__main__':
    app.run_server(debug=True)
