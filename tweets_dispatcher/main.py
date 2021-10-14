from tweepy import Stream, API, OAuthHandler
import argparse

from classes import Listener
from params import  (consumer_key, consumer_secret, access_token,
                     access_token_secret, topic)

		
if name == '__main__':	
    # GET ARGS FROM CLI		
	parser = argparse.ArgumentParser()
	parser.add_argument('--topic', type=str, default=topic, help='Topic for the twitterAPI')
    args = parser.parse_args()
    topic = [args.topic]
    
    # GET AUTHORIZATION
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = API(auth)

    #RUN LISTENER
	stream_listener = Listener()
	stream = Stream(auth=api.auth, listener=stream_listener)
	stream.filter(track=topic, is_async=True)