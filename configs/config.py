import logging
import configparser

config = configparser.ConfigParser()
config.read('configs/config.ini')

# 读取DEFAULT下的debug配置
global_env = config.get('GLOBAL', 'env')
log_level = config.getint('LOG', 'level')
log_file = config.get('LOG', 'file')
lark_token = config.get('lark', 'token')

concurrency = config.getint('neo4j', 'concurrency')
timeout = config.getint('neo4j', 'timeout')
neo4j_uri = config.get('neo4j', 'uri')
neo4j_username = config.get('neo4j', 'username')
neo4j_passwd = config.get('neo4j', 'passwd')
query_len = config.getint('neo4j', 'query_len')
input_path = config.get('neo4j', 'input_path')

logger = logging.getLogger()
logger.setLevel(log_level)
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(message)s')
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
