import dash_core_components as dcc
import dash_html_components as html


layout = html.Div([
    html.Div(style={'width': '100%', 'display': 'inline-block'}),
    # html.Div(style={'width': '10%', 'display': 'inline-block'}),
    html.Div([
        dcc.Markdown("""# WELCOME!
## To the coolest twitter Analytics
                     """) ,
        html.Br(),
        html.Br(),
        dcc.Markdown("""
#### What can you do:
    
    
##### 1. Real time sentiment analysis
##### 2. Focused analysis by topic
##### 3. Tweet correction
##### 4. Tweet translation
                     """)
        ], style={'width': '45%', 'display': 'inline-block'}),
    html.Div([
        html.Div(style={'width': '100%', 'display': 'inline-block'} ),
        dcc.Markdown("""
                     ![Analytics_logo](https://www.webmarketinggarden.it/wp-content/uploads/2017/09/WebAnalytics.jpg)
                     
                 """)        
        ], style={'width': '45%', 'display': 'inline-block'})
    ])
