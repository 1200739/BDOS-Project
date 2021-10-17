import requests
from tweepy.streaming import StreamListener
import time
import mysql.connector
from utils import logger
from params import  (service_url, db_user, db_password, 
                     db_host, db_schema, db_table, topic)


class Listener(StreamListener):
    def __init__(self, *args, **kwargs):
        self.service_url = service_url
        self.topic = kwargs.get('topic', topic)
        super().__init__()
      

    def on_status(self, status):
        logger.info(f'CALLING {self.service_url}, TWEET: {status.text}')

        request_params = dict(tweet=status.text, topic=self.topic)
        time_ = time.time()
        try:
            response = requests.get(self.service_url, params=request_params)
            response.raise_for_status() # Raise an http error if occured
            status_code = response.status_code
            service_res = response.json()
            logger.info(f'API RESPONSE: {service_res}')
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
        self.store_response(status_code, elapsed_time, service_res)
        logger.info(f'STATUS: {status_code}, ELAPSED_TIME: {elapsed_time}')

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def store_response(self,status_code, elapsed_time, service_res):
        try:
            query = f"insert into {db_schema}.{db_table}(status_code, elapsed_time, response, polarity, subjectivity) values({status_code}, {elapsed_time},'{service_res['sentiment']}', {service_res['polarity']}, {service_res['subjectivity']})"
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
        