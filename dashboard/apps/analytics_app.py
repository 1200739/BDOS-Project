import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
from datetime import date
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import requests
import base64
from utility.utils import (logger, prediction_endpoint, TODAY, 
                           correction_endpoint, translation_endpoint)
from utility.params import topic
from utility.functions import get_data
from main import app
from wordcloud import WordCloud, STOPWORDS


layout = html.Div([
        html.H1(children='ANALYTICS DASHBOARD'),
        dcc.Tabs([
            dcc.Tab(label='Topic', children=[
                html.Div([
                    html.Div('Analyzie data by topic.', style={'width': '40%', 'display': 'inline-block'}),
                    html.Div('Topic', style={'width': '20%', 'display': 'inline-block'}),
                    html.Div('Range time', style={'width': '20%', 'display': 'inline-block'}),
                    ]),
                html.Div([
                    html.Div('', style={'width': '40%', 'display': 'inline-block'}),
                    dbc.Input(id='topic_input_analytics', type='text', value=topic, style={'width': '20%', 'display': 'inline-block'}),
                    # html.Div('', style={'width': '10%', 'display': 'inline-block'}),
                    # dbc.Input(id='date_range_analytics', type='number', value=RANGE_TIME, style={'width': '20%', 'display': 'inline-block'})
                    dcc.DatePickerRange(
                        display_format='YYYY-MM-DD',
                        start_date_placeholder_text="Start Period",
                        end_date_placeholder_text = "End Period",
                        initial_visible_month = date(TODAY.year, TODAY.month, 1),
                        min_date_allowed = date(2021, 9, 1),
                        max_date_allowed = TODAY
                    ),
                    dbc.Button('Submit', id='submit-topic-button', 
                           outline=False, color="primary", n_clicks=0,  className="mr-1"),
                    ]),
                html.Div([
                    html.Div('Tweets count:'),
                    html.Div('-', id='tweets-count-id'),
                    dcc.Graph(id='barplot-sentence-count'),
                    ], style={'width': '40%', 'display': 'inline-block'}),
                html.Div([
                    html.Img(id='world-cloud-img')
                    ], style={'width': '60%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(
                        id='density-polarity-topic'
                    )], style={'width': '50%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(
                        id='density-subjectivity-topic'
                    )], style={'width': '50%', 'display': 'inline-block'}),
            ]),
        dcc.Tab(label='Tweet', children=[
            html.Div([
                html.Div('Insert your tweet:'),
                # dbc.Input(id='topic_input_analytics_2', type='text', placeholder='Insert Here...'),
                dbc.Textarea(
                    id='textarea-state',
                    placeholder='Put your tweet here...',
                    bs_size="lg",
                    style={'width': '100%', 'height': 100},
                ),
                dbc.Button('Submit', id='textarea-state-button', 
                           outline=False, color="primary", n_clicks=0,  className="mr-1"),
                html.Div(style={'width': '100%', 'height': 50}),
                html.Div('Correct tweet:'),
                html.Div('-', id='correct-tweet'),
                html.Div(style={'width': '100%', 'height': 50}),
                html.Div('Translation:'),
                html.Div('-', id='translated-tweet'),
                html.Div(style={'width': '100%', 'height': 50}),
                ], style={'width': '50%', 'display': 'inline-block'}),
            html.Div([
                daq.Gauge(
                    id='gauge-analytics-1',
                    value=-1,
                    label='Polarity',
                    max=1,
                    min=-1,
                ),
                daq.Gauge(
                    id='gauge-analytics-2',
                    value=0,
                    label='Subjectivity',
                    max=1,
                    min=0,
                )
                ], style={'width': '50%', 'display': 'inline-block'}),
            ])
        ])
    ])
             
    
# =============================================================================
# CALLBACK
# =============================================================================
@app.callback(
    [Output('correct-tweet', 'children'),
     Output('translated-tweet', 'children'),
     Output('gauge-analytics-1', 'value'),
     Output('gauge-analytics-2', 'value'),],
     Input('textarea-state-button', 'n_clicks'),
     State('textarea-state', 'value')
    )
def update_tweet(n, text):
    try:
        logger.info(f'INPUT TEXT: {text}, TYPE: {type(text)}')
        payload = dict(tweet=text)
        
        # CORRECT TWEET
        correct_text = requests.get(correction_endpoint, params=payload).json()['correct_tweet']
        logger.info(f'CLEAN TEXT: {correct_text}')
        payload = dict(tweet=correct_text)
        
        # TRANSLATED TWEET
        translated_text = requests.get(translation_endpoint, params=payload).json()['translated_tweet']
        logger.info(f'TRANSLATED TEXT: {translated_text}')
        
        # PREDICTED TWEET
        prediction = requests.get(prediction_endpoint, params=payload).json()
        logger.info(f'RESPONSE: {prediction}')
        polarity, subjectivity = prediction['polarity'], prediction['subjectivity']
        
        return correct_text, translated_text, polarity, subjectivity
    
    except Exception as ex:
        logger.exception(ex)
    
    
@app.callback(
    [Output('tweets-count-id', 'children'),
     Output('barplot-sentence-count', 'figure'),
     Output('world-cloud-img', 'src'),
     Output('density-polarity-topic', 'figure'),
     Output('density-subjectivity-topic', 'figure'),
     ],
     Input('submit-topic-button', 'n_clicks'),
     State('range_time_input', 'value')
     )
def update_figure(n, range_time):
    try:
        data, columns = get_data(range_time)
        df = pd.DataFrame(data, columns=columns)
        logger.info(df.head())
        tweets_count = len(df)
        polarities = df['polarity'].to_numpy()
        subjectivities = df['subjectivity'].to_numpy()
        df_mod = df.copy().groupby(['sentence']).agg(count=('sentence', 'count'))   
        logger.info(df_mod.head())

        # SENTIMENT BARPLOT
        fig = px.bar(df_mod, x = 'sentence', y = 'count', barmode='group', title = 'Sentence barplot')
        
        # WORD CLOUD
        wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(df['tweet'])
        wordcloud.to_file("word_cloud_image.jpeg")
        encoded_image = base64.b64encode(open("word_cloud_image.jpeg", 'rb').read())
        fig2 = 'data:image/png;base64,{}'.format(encoded_image)
        
        # POLARITY DENSE PLOT
        fig3 = ff.create_distplot([polarities], ['Polarity'], show_hist=False, colors=['#37AA9C'])
        
        # SUBJECTIVITY DENSE PLOT
        fig4 = ff.create_distplot([subjectivities], ['subjectivity'], show_hist=False, colors=['#94F3E4'])
    
        return tweets_count, fig, fig2, fig3, fig4
    
    except Exception as ex:
        logger.exception(ex)