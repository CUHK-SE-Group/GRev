import logging
import logging.handlers
import configparser
import os
from pythonjsonlogger import jsonlogger
import json

print(os.getcwd())
config = configparser.ConfigParser()
config.read('configs/config.ini')

global_env = config.get('GLOBAL', 'env')
log_level = config.getint('LOG', 'level')
log_file = config.get('LOG', 'file')

concurrency = config.getint('neo4j', 'concurrency')
timeout = config.getfloat('neo4j', 'timeout')
neo4j_uri = config.get('neo4j', 'uri')
neo4j_username = config.get('neo4j', 'username')
neo4j_passwd = config.get('neo4j', 'passwd')
query_len = config.getint('neo4j', 'query_len')
input_path = config.get('neo4j', 'input_path')

def new_logger(file, enable_elk=False):
    logger = logging.getLogger()
    logger.setLevel(log_level)
    jsonformatter = jsonlogger.JsonFormatter('%(asctime)s %(filename)s %(lineno)d %(message)s')

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    file_handler = logging.FileHandler(file)
    file_handler.setFormatter(jsonformatter)
    file_handler.setLevel(logging.INFO)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger

