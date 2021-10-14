import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from utility.utils import logger, REFRESH_TIME, RANGE_TIME
from utility.functions import get_data
from main import app

fig1 = px.bar()
fig1.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)'
    })

fig2 = px.box()
fig2.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)'
    })

fig3 = px.violin()
fig3.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)'
    })

fig4 = px.violin()
fig4.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)'
    })

fig5 = px.violin()
fig5.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)'
    })

layout = html.Div([
    html.H1(children='MONITORING DASHBOARD'),

    html.Div([
        html.Div('Dashboard for realtime monitoring of Tweets-Dispatcher service.', style={'width': '40%', 'display': 'inline-block'}),
        html.Div('Refresh time', style={'width': '20%', 'display': 'inline-block'}),
        html.Div('Range time', style={'width': '20%', 'display': 'inline-block'}),
        ]),
    html.Div([
        html.Div('', style={'width': '40%', 'display': 'inline-block'}),
        dbc.Input(id='refresh_time_input', type='number', value=REFRESH_TIME, style={'width': '15%', 'display': 'inline-block'}),
        html.Div('', style={'width': '5%', 'display': 'inline-block'}),
        dbc.Input(id='range_time_input', type='number', value=RANGE_TIME, style={'width': '15%', 'display': 'inline-block'})
        ]),
    html.Div([
        dcc.Graph(
            id='fig1',
            figure=fig1
        )], style={'width': '34%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(
            id='fig2',
            figure=fig2
        )], style={'width': '33%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(
            id='fig3',
            figure=fig3
            )], style={'width': '33%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(
            id='fig4',
            figure=fig4
            )], style={'width': '50%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(
            id='fig5',
            figure=fig5
            )], style={'width': '50%', 'display': 'inline-block'}),
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
    [Output('fig1', 'figure'),
     Output('fig2', 'figure'),
     Output('fig3', 'figure'),
     Output('fig4', 'figure'),
     Output('fig5', 'figure'),],
     Input('interval-component', 'n_intervals'),
     State('range_time_input', 'value')
    )
def update_figure(n, range_time):
    try:
        data, columns = get_data(range_time)
        df = pd.DataFrame(data, columns=columns)
        logger.info(df.head())
        df_mod = df.copy().groupby(['Status']).count().reset_index().rename(columns = {'Elapsed_Time':'count'}).astype({'Status': 'str'})        

        # STATUS CODE BARPLOT
        # fig = px.bar(df_mod, x = 'Service', y = 'count', color = 'Status', barmode='group', title = 'HISTOGRAM')
        fig1 = px.bar(
            df_mod, 
            x = 'Status', 
            y = 'count', 
            color = 'Status', 
            barmode='group', 
            title = 'HISTOGRAM'
            )
        fig1.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)'
            })
        
        # ELAPSED TIME BOXPLOT
        # fig2 = px.ecdf(df, x = "Elapsed_Time", color = 'Service', title = 'ECDF')
        fig2 = px.box(
            df, 
            y = "Elapsed_Time", 
            title = 'ECDF', 
            points="all"
            )
        fig2.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)' 
            })
        
        # SENTIMENT BARPLOT
        fig3 = px.violin(
            df, 
            y="Elapsed_Time", 
            color="Service", 
            box=True, points="all", 
            hover_data=df.columns, 
            title = 'VIOLIN & BOXPLOT'
            )
        fig3.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)'
            })
        
        # POLARITY DENSE PLOT
        fig4 = px.violin(df, 
                         y="Elapsed_Time", 
                         color="Service", 
                         box=True, points="all", 
                         hover_data=df.columns, 
                         title = 'VIOLIN & BOXPLOT'
                         )
        fig4.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)'
            })
        
        # SUBJECTIVITY DENSE PLOT
        fig5 = px.violin(df, 
                         y="Elapsed_Time", 
                         color="Service", 
                         box=True, points="all", 
                         hover_data=df.columns, 
                         title = 'VIOLIN & BOXPLOT'
                         )
        fig5.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)'
            })
    
        return fig1, fig2, fig3, fig4, fig5
    
    except Exception as ex:
        logger.exception(ex)