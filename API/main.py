from fastapi import FastAPI
import uvicorn

from utils import logger, HOST, PORT
from functions import (store_tweet, clean_tweet, store_result, 
                       get_correct_tweet, predict_tweet, 
                       get_translated_tweet, get_tweets_by_topic)


app = FastAPI()
  

@app.get("/getPredictedTweet")
async def predict_tweet_endpoint(tweet: str, topic: str):
    """Tweet prediction endpoint"""    
    id_tweet = store_tweet(tweet, topic)
    
    # PRE PROCESSING
    logger.info(f'ORIGINAL TWEET: {tweet}')
    tweet = clean_tweet(tweet)
    logger.info(f'CLEAN TWEET: {tweet}')
    response, polarity, subjectivity = predict_tweet(tweet) 
    logger.info*(f'SENTIMENT: {response}, POLARITY: {polarity}, SUBJETIVITY: {subjectivity}')          
    store_result(id_tweet, response, polarity, subjectivity)
    logger.info(f'SENTIMENT: {response}')
    
    return {
            'id_tweet': id_tweet, 
            'sentiment': response,
            'polarity': polarity,
            'subjectivity': subjectivity
        } 

     
@app.get("/getCleanTweet")
async def clean_tweet_endpoint(tweet: str):
    """Tweet cleaner endpoint"""
    logger.info(f'CALLED: "getCleanTweet", TWEET: {tweet}')
    return dict(
        tweet=clean_tweet(tweet)
        ) 


@app.get("/getCorrectTweet")
async def get_correct_tweet_endpoint(tweet: str):
    """Tweet correction endpoint"""
    logger.info(f'CALLED: "getCorrectTweet", TWEET: {tweet}')
    return dict(
         correct_tweet=get_correct_tweet(tweet)
         ) 


@app.get("/getTranslatedTweet")
async def get_translated_tweet_endpoint(tweet: str):
    """Tweet translation endpoint"""
    logger.info(f'CALLED: "getTranslatedTweet", TWEET: {tweet}')
    return dict(
         translated_tweet=get_translated_tweet(tweet)
         ) 

@app.get("/getTweetsByTopic")
async def get_tweets_by_topic_endpoint(topic: str, start_date: str, end_date: str):
    """Endpoint for tweets retrieving by topic"""
    logger.info(f'CALLED: "getTTweetsByTopic", TOPIC: {topic}')
    tweets, columns = get_tweets_by_topic(topic, start_date, end_date)
    return dict(
         tweets=tweets,
         columns=columns
         ) 


# =============================================================================
# MAIN
# =============================================================================
if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)