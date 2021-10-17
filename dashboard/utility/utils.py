import dash_bootstrap_components as dbc
import logging
import dash_html_components as html
from datetime import datetime

FORMAT = '%(levelname)s - TIME: %(asctime)s, NAME: %(name)s, FUNC: %(funcName)s, MSG: %(message)s'
logging.basicConfig(
                    format=FORMAT, datefmt='%d-%m-%y %H:%M:%S', 
                    level=logging.INFO
                    )
logger = logging.getLogger(__name__)

external_stylesheets = [dbc.themes.MINTY]
RANGE_TIME = 60
REFRESH_TIME = 5
DASH_BASE_URL = '/'

CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
	
content = html.Div(id="page-content", style=CONTENT_STYLE)

TODAY = datetime.today()

fastAPI_host = 'ec2-3-88-87-239.compute-1.amazonaws.com' #'localhost'
fastAPI_port = 5000
fastAPI_url = f'http://{fastAPI_host}:{fastAPI_port}'
prediction_endpoint = f'{fastAPI_url}/getPredictedTweet'
correction_endpoint = f'{fastAPI_url}/getCorrectTweet'
translation_endpoint = f'{fastAPI_url}/getTranslatedTweet'
get_tweets_by_topic_endpoint = f'{fastAPI_url}/getTweetsByTopic'