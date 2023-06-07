import os
from database_tests.helper import parse_query_file
import re
import subprocess


folder_path='query_producer/logs/composite'
file_paths = []
for dirpath, dirnames, filenames in os.walk(folder_path):
    for file in filenames:
        if 'cur.log' in file:
            file_path = os.path.join(dirpath, file)
            file_paths.append(file_path)

       
for path in file_paths:
    dir = path.split('/')
    subprocess.check_output(["java", "-jar", "./query_producer/Cypher2GremlinFile.jar", path, "query_producer/gremlin/"+dir[-1]], universal_newlines=True)
        