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
from classes import MysqlCursor

# =============================================================================
# FUNCTIONS
# =============================================================================
def get_data(range_time):
    try:
        query = f'select status_code, sentiment, polarity, subjectivity, elapsed_time from {db_schema}.{db_table} where current_timestamp() - log_timestamp < {range_time}'
        with MysqlCursor() as cur:
                cur.execute(query)
                data = cur.fetchall()
                columns = [col[0] for col in cur.description]
        try:
            logger.info(f'Query: OK; first row: {data[0]}')
        except Exception:
            logger.info(f'Query: OK; first row: []')
        return data, columns
    except mysql.connector.errors.InterfaceError:
        return None, None



