import logging
import mysql.connector
from params import file_log_name
# LOGGING CONFIG
FORMAT = '%(levelname)s - TIME: %(asctime)s, NAME: %(name)s, FUNC: %(funcName)s, MSG: %(message)s'
logging.basicConfig(
                    format=FORMAT, datefmt='%d-%m-%y %H:%M:%S', 
                    level=logging.INFO
                    )
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG) 

fh = logging.FileHandler(file_log_name)
fh.setLevel(logging.DEBUG)
fh.setFormatter(
    logging.Formatter(FORMAT)
    )
logger.addHandler(fh)