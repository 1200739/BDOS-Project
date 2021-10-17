import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import plotly.express as px
import pandas as pd
import requests
import base64
from utility.utils import (logger, prediction_endpoint, TODAY, 
                           correction_endpoint, translation_endpoint,
                           get_tweets_by_topic_endpoint)
from utility.params import topic
# from utility.functions import get_data
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
                    dbc.Input(id='topic-input-analytics', type='text', value=topic, style={'width': '20%', 'display': 'inline-block'}),
                    # html.Div('', style={'width': '10%', 'display': 'inline-block'}),
                    # dbc.Input(id='date_range_analytics', type='number', value=RANGE_TIME, style={'width': '20%', 'display': 'inline-block'})
                    dcc.DatePickerRange(
                        id='range-time-input',
                        display_format='YYYY-MM-DD',
                        start_date_placeholder_text="Start Period",
                        end_date_placeholder_text = "End Period",
                        initial_visible_month = date(TODAY.year, TODAY.month, 1),
                        min_date_allowed = date(2021, 9, 1),
                        max_date_allowed = TODAY,
                        minimum_nights = 0 
                    ),
                    dbc.Button('Submit', id='submit-topic-button', 
                           outline=False, color="primary", n_clicks=0,  className="mr-1"),
                    ]),
                html.Div([
                    # html.H2('Tweets count:'),
                    # html.Div('-', id='tweets-count-id'),
                    daq.LEDDisplay(
                        id='tweets-count-id',
                        label=dict(
                            label="Tweets count",
                            style={'width': '100'}
                            ),
                        value='0',
                        size=150
                        #color="#FF5E5E"
                    )
                    ], style={'width': '40%', 'display': 'inline-block'}),
                html.Div([
                    html.Br(),
                    # dcc.Markdown("", id='world-cloud-img', style={'width': '100%'})
                    html.Img(src="", id='world-cloud-img', width='100%')
                    ], style={'width': '60%', 'display': 'inline-block'}),
                # html.Div([], style={'width': '40%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(id='barplot-sentence-count'),
                    ], style={'width': '50%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(id='piechart-sentence-count'),
                    ], style={'width': '50%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(
                        id='hist-polarity-topic'
                    )], style={'width': '50%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(
                        id='hist-subjectivity-topic'
                    )], style={'width': '50%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(
                        id='box-polarity-topic'
                    )], style={'width': '50%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(
                        id='box-subjectivity-topic'
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
    if n > 0:
        try:
            logger.info(f'INPUT TEXT: {text}, TYPE: {type(text)}')
            
            # CORRECT TWEET
            payload = dict(tweet=text)
            correct_text = requests.get(correction_endpoint, params=payload).json()['correct_tweet']
            logger.info(f'CLEAN TEXT: {correct_text}')
            
            # TRANSLATED TWEET
            payload = dict(tweet=correct_text)
            translated_text = requests.get(translation_endpoint, params=payload).json()['translated_tweet']
            logger.info(f'TRANSLATED TEXT: {translated_text}')
            
            # PREDICTED TWEET
            payload = dict(tweet=correct_text, topic='None')
            prediction = requests.get(prediction_endpoint, params=payload).json()
            logger.info(f'RESPONSE: {prediction}')
            polarity, subjectivity = prediction['polarity'], prediction['subjectivity']
            
            return correct_text, translated_text, polarity, subjectivity
        
        except Exception as ex:
            logger.exception(ex)
    
    
@app.callback(
    [Output('tweets-count-id', 'value'),
     Output('barplot-sentence-count', 'figure'),
     Output('piechart-sentence-count', 'figure'),
     Output('world-cloud-img', 'src'),
     Output('hist-polarity-topic', 'figure'),
     Output('hist-subjectivity-topic', 'figure'),
     Output('box-polarity-topic', 'figure'),
     Output('box-subjectivity-topic', 'figure'),
     ],
     [Input('submit-topic-button', 'n_clicks')],
     [State('topic-input-analytics', 'value'),
     State('range-time-input', 'start_date'),
     State('range-time-input', 'end_date')]
     )
def update_figure(n, topic, start_date, end_date):
    if n > 0:
        try:
            end_date = (datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
            payload = dict(topic=topic, start_date=start_date, end_date=end_date)
            logger.info(f'GTBT PAYLOAD: {payload}')
            out = requests.get(get_tweets_by_topic_endpoint, params=payload).json()
            data, columns = out['tweets'], out['columns']
            df = pd.DataFrame(data, columns=columns)
            logger.info(df.head())
            tweets_count = str(len(df))
            df_mod = df.copy().groupby(['sentence']).agg(count=('sentence', 'count')).reset_index()  
            logger.info(df_mod.head())
    
            # SENTIMENT BARPLOT
            fig = px.bar(df_mod, x = 'sentence', 
                         y = 'count', 
                         color = 'sentence', 
                         barmode='group', 
                         title = 'Sentence Barplot',
                         color_discrete_map={'positive':'lightcyan',
                                              'negative':'cyan',
                                              'neutral':'royalblue'})
            fig.update_layout({
                'plot_bgcolor': 'rgba(0, 0, 0, 0)'
                })
            
            # SENTIMENT BARPLOT
            fig1 = px.pie(df_mod, 
                          names='sentence', 
                          values='count', 
                          title='Sentence Piechart', 
                          color= 'sentence',
                          # color_discrete_sequence=px.colors.sequential.RdBu)
                          color_discrete_map={'positive':'lightcyan',
                                              'negative':'cyan',
                                              'neutral':'royalblue'})
            fig.update_layout({
                'plot_bgcolor': 'rgba(0, 0, 0, 0)'
                })
            
            # WORD CLOUD
            stopwords = set(STOPWORDS)
            wordcloud = WordCloud(max_font_size=50, 
                                  max_words=100, 
                                  stopwords=stopwords, 
                                  background_color="white").generate(" ".join(df['tweet']))
            wordcloud.to_file("word_cloud_image.png")
            encoded_image = base64.b64encode(open("word_cloud_image.png", 'rb').read())
            img = "{}".format(encoded_image)[2:-1]
            # fig2 = '![word_cloud](data:image/png;base64,{})'.format(img)
            fig2 = 'data:image/png;base64,{}'.format(img)
            
            # POLARITY DENSE PLOT
            fig3 = px.histogram(df, x='polarity') #ff.create_distplot([polarities], ['Polarity'], show_hist=False, colors=['#37AA9C'])
            fig3.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)'
            })
             
            # SUBJECTIVITY DENSE PLOT
            fig4 = px.histogram(df, x='subjectivity') #ff.create_distplot([subjectivities], ['subjectivity'], show_hist=False, colors=['#94F3E4'])
            fig4.update_layout({
                'plot_bgcolor': 'rgba(0, 0, 0, 0)'
                })
            
            # POLARITY BOX PLOT
            fig5 = px.box(df, x='polarity', title="Polarity Boxplot", points="all") 
            fig5.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)'
            })
             
            # SUBJECTIVITY BOX PLOT
            fig6 = px.box(df, x='subjectivity', title="Subjectivity Boxplot", points="all")  
            fig6.update_layout({
                'plot_bgcolor': 'rgba(0, 0, 0, 0)'
                })
            
            return tweets_count, fig, fig1, fig2, fig3, fig4, fig5, fig6
        
        except Exception as ex:
            logger.exception(ex)