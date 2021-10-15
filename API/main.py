from fastapi import FastAPI
import uvicorn

from utils import logger, HOST, PORT
from functions import (store_tweet, clean_tweet, store_result, 
                       get_correct_tweet, predict_tweet, get_translated_tweet)


app = FastAPI()
  

@app.get("/getPredictedTweet")
async def predict_tweet_endpoint(tweet: str):
    """Tweet prediction endpoint"""
    if tweet is None:
        out = None
    else:
        id_tweet = store_tweet(tweet)
        
        # PRE PROCESSING
        logger.info(f'ORIGINAL TWEET: {tweet}')
        tweet = clean_tweet(tweet)
        logger.info(f'CLEAN TWEET: {tweet}')
        text, response = predict_tweet(tweet)
            
    store_result(id_tweet, text, response)
    logger.info(f'SENTIMENT: {response}')
    
    return {
            'id_tweet': id_tweet, 
            'sentiment': response,
            'polarity': text.sentiment.polarity,
            'subjectivity': text.sentiment.subjectivity
        } 

     
@app.get("/getCleanTweet")
async def clean_tweet_endpoint(tweet: str):
    """Tweet cleaner endpoint"""
    return dict(
        tweet=clean_tweet(tweet)
        ) 


@app.get("/getCorrectTweet")
async def geT_correct_tweet_endpoint(tweet: str):
    """Tweet correction endpoint"""
    return dict(
         correct_tweet=get_correct_tweet(tweet)
         ) 


@app.get("/getTranslatedTweet")
async def geT_correct_tweet_endpoint(tweet: str):
    """Tweet translation endpoint"""
    return dict(
         translated_tweet=get_translated_tweet(tweet)
         ) 


# =============================================================================
# MAIN
# =============================================================================
if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)