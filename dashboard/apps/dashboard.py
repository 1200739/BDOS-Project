import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import mysql.connector
import logging
from params import db_user, db_password, db_host, db_schema, db_table
from utils import logger, REFRESH_TIME, RANGE_TIME, external_stylesheets
from functions import get_data

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

fig = px.bar()
fig2 = px.box()
fig3 = px.violin()

app.layout = html.Div([
    html.H1(children='MONITORING DASHBOARD'),

    html.Div([
        html.Div('Dashboard for realtime monitoring of Tweets-Dispatcher service.', style={'width': '40%', 'display': 'inline-block'}),
        html.Div('Refresh time', style={'width': '20%', 'display': 'inline-block'}),
        html.Div('Range time', style={'width': '20%', 'display': 'inline-block'}),
        ]),
    html.Div([
        html.Div('', style={'width': '40%', 'display': 'inline-block'}),
        dcc.Input(id='refresh_time_input', type='number', value=REFRESH_TIME, style={'width': '20%', 'display': 'inline-block'}),
        # html.Div('', style={'width': '10%', 'display': 'inline-block'}),
        dcc.Input(id='range_time_input', type='number', value=RANGE_TIME, style={'width': '20%', 'display': 'inline-block'})
        ]),
    html.Div([
        dcc.Graph(
            id='histogram',
            figure=fig
        )], style={'width': '50%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(
            id='ecdf',
            figure=fig2
        )], style={'width': '50%', 'display': 'inline-block'}),
    dcc.Graph(
        id='density-function',
        figure=fig3
    ),
    dcc.Interval(
            id='interval-component',
            interval=REFRESH_TIME * 1000, # in milliseconds
            n_intervals=0
        )
    ])
             
    
# =============================================================================
# CALLBACK
# =============================================================================
@app.callback(
    Output('interval-component', 'interval'),
    Input('refresh_time_input', 'value')
    )
def update_interval(value):
    logger.info('update_interval: NEW: {value * 1000}')
    return value * 1000

@app.callback(
    [Output('histogram', 'figure'),
      Output('ecdf', 'figure'),
      Output('density-function', 'figure'),],
      Input('interval-component', 'n_intervals'),
      State('range_time_input', 'value')
      )
def update_figure(n, range_time):
    try:
        data, columns = get_data(range_time)
        df = pd.DataFrame(data, columns=columns)
        logger.info(df.head())
        # df_mod = df.copy().groupby(['Service','Status']).count().reset_index().rename(columns = {'Elapsed_Time':'count'}).astype({'Status': 'str'})
        df_mod = df.copy().groupby(['Status']).count().reset_index().rename(columns = {'Elapsed_Time':'count'}).astype({'Status': 'str'})        

        # STATUS CODE BARPLOT
        # fig = px.bar(df_mod, x = 'Service', y = 'count', color = 'Status', barmode='group', title = 'HISTOGRAM')
        fig = px.bar(df_mod, x = 'Status', y = 'count', color = 'Status', barmode='group', title = 'HISTOGRAM')
        # ELAPSED TIME BOXPLOT
        # fig2 = px.ecdf(df, x = "Elapsed_Time", color = 'Service', title = 'ECDF')
        fig2 = px.box(df, y = "Elapsed_Time", title = 'ECDF', points="all")
        # SENTIMENT BARPLOT
        fig3 = px.violin(df, y="Elapsed_Time", color="Service", box=True, points="all", hover_data=df.columns, title = 'VIOLIN & BOXPLOT')
        # POLARITY DENSE PLOT
        fig4 = px.violin(df, y="Elapsed_Time", color="Service", box=True, points="all", hover_data=df.columns, title = 'VIOLIN & BOXPLOT')
        # SUBJECTIVITY DENSE PLOT
        fig5 = px.violin(df, y="Elapsed_Time", color="Service", box=True, points="all", hover_data=df.columns, title = 'VIOLIN & BOXPLOT')
        logger.info('OK fig1, fig2, fig3')
    
        return fig, fig2, fig3
    except Exception as ex:
        logger.exception(ex)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)


