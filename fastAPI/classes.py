import mysql.connector
from pydantic import BaseModel

from params import db_user, db_password, db_host, db_schema


class Tweet(BaseModel):
    """Base tweet data classes"""
    tweet: str


class MysqlCursor:
    """Mysql Connector"""
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
