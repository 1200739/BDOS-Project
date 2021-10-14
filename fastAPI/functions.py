import re
from params import db_schema, db_table, db_table_pred
from utils import logger, ML_VERSION
from classes import MysqlCursor
from textblob import TextBlob
from deep_translator import GoogleTranslator

def clean_tweet(tweet):
    """Normalize the tweet string"""
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())   


def store_tweet(tweet):
    """Store the raw tweet into the DB"""
    try:
        tweet = tweet.replace("'", "\\'" )
        query = f"insert into {db_schema}.{db_table} set tweet='{tweet}'"
        logger.info(f'QUERY: {query}') 
        with MysqlCursor() as cur:
            cur.execute(query)
            tweet_id = int(cur.lastrowid)
            logger.info(f'ID_TWEET: {tweet_id}') 
        return tweet_id
    except Exception as ex:
        logger.exception(ex)
        

def predict_tweet(tweet):
    """Predict the sentiment of the tweet"""
    text = TextBlob(tweet)
    
    if text.sentiment.polarity > 0:
        response = 'positive'
    elif text.sentiment.polarity == 0:
        response = 'neutral'
    else:
        response = 'negative'
    return text, response
        
        
def store_result(id_tweet, response, text):
    """Store the prediction into the DB"""
    try:
        # query = f"insert into {db_schema}.{db_table_pred} set id_tweet={id_tweet} and ml_version='0.1' and response='{prediction}'"
        query = f"insert into {db_schema}.{db_table_pred} values({id_tweet}, '{ML_VERSION}', '{response}', {text.polarity}, {text.subjectivity})"
        logger.info(f'QUERY: {query}')
        with MysqlCursor() as cur:
            cur.execute(query)
    except Exception as ex:
        logger.exception(ex)

def get_correct_tweet(tweet):
    """Spelling correction of the sentence"""
    text = TextBlob(tweet)
    return text.correct().raw

def get_translated_tweet(tweet, language='it'):
    """Translate the tweet to a specific language"""
    translated = GoogleTranslator(source='auto', target=language)
    return translated.translate(tweet)