import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import mysql.connector
import logging
from params import db_user, db_password, db_host, db_schema, db_table
from utils import logger


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
