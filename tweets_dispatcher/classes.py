import requests
from tweepy.streaming import StreamListener
from tweepy import Stream, API, OAuthHandler
import logging
import time
import argparse
import mysql.connector
from utils import logger
from params import  (consumer_key, consumer_secret, access_token,
                     access_token_secret, file_log_name,
                     service_url, topic,
                     db_user, db_password, db_host, db_schema, db_table)


class Listener(StreamListener):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.service_url = service_url

    def on_status(self, status):
        logger.info(f'CALLING {self.service_url}, TWEET: {status.text}')

        logger.info(f'CALLING {name}')
        request_params = dict(tweet=status.text)
        time_ = time.time()
        try:
            response = requests.get(self.service_url, params=request_params)
            response.raise_for_status() # Raise an http error if occured
            status_code = response.status_code
            service_res = response.json()
        except requests.exceptions.HTTPError as e:
            logger.exception(e)
            status_code = response.status_code
            service_res = {}
        except requests.exceptions.Timeout as e:
            logger.exception(e)
            status_code = 408
            service_res = {}
        except requests.exceptions.RequestException as e:
            logger.exception(e)
            status_code = 500
            service_res = {}
            
        elapsed_time = time.time() - time_ 
        self.store_response(name, status_code, elapsed_time, service_res)
        logger.info(f'STATUS: {status_code}, ELAPSED_TIME: {elapsed_time}')

    def on_error(self, status_code):
        if status_code == 420:
            return False

	def store_response(self,status_code, elapsed_time, service_res):
		try:
			query = f"insert into {db_schema}.{db_table}(status_code, elapsed_time, response, polarity, subjectivity) values({status_code}, {elapsed_time},'{service_res['SENTIMENT'}', {service_res['POLARITY']}, {service_res['SUBJECTIVITY']})"
			logger.info(f'QUERY: {query}')
			with MysqlCursor() as cur:
				cur.execute(query)
        except KeyError:
            query = f"insert into {db_schema}.{db_table}(status_code, elapsed_time, response, polarity, subjectivity) values({status_code}, {elapsed_time}, NULL, NULL, NULL)"
			logger.info(f'QUERY: {query}')
			with MysqlCursor() as cur:
				cur.execute(query)
		except Exception as ex:
			logger.exception(ex)


class MysqlCursor:
    def __init__(self, commit=True):
        self.commit = commit
        
    def __enter__(self):
        self.connection = mysql.connector.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            database=db_schema,
            use_pure=True
            )
        self.cursor = self.connection.cursor()
        
        return self.cursor
    
    def __exit__(self, *args, **kwargs):
        if self.commit:
            self.connection.commit()
        self.cursor.close()
        self.connection.close()
        