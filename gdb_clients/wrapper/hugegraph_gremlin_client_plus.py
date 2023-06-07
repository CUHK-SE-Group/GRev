# Author: HaotianXie (hotinexie@gmail.com)

import json
import requests
import logging
import os

from typing import List, Dict

class HugeGraphClient:
    def __init__(self,
                 hugegraph_serever_ip: str = '0.0.0.0',
                 hugegraph_serever_port: str = '7777',
                 graph: str = 'hugegraph'):
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
            'Content-Type': 'application/json'
        }
        self._hugegraph_serever_ip = hugegraph_serever_ip
        self._hugegraph_serever_port = hugegraph_serever_port
        self._host = 'http://' + self._hugegraph_serever_ip + ':' + self._hugegraph_serever_port
        self._graph = '/graphs/' + graph

    def get_schema(self):
        url = self._host + self._graph + '/schema'
        response = requests.get(url=url)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    def get_all_graphs(self):
        url = self._host + '/graphs'
        response = requests.get(url=url)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    def send_gremlin(self,
                     gremlin: str,
                     bindings: Dict = {},
                     language: str = 'gremlin-groovy',
                     aliases: Dict = {}):
        url = self._host + '/gremlin'
        request_body = {
            "gremlin": gremlin,
            "bindings": bindings,
            "language": language,
            "aliases": aliases
        }
        response = requests.post(url=url, data=json.dumps(request_body), headers=self._headers)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    
    def delete_all_graphs(self):
        url = self._host + self._graph + '/clear?confirm_message=I%27m+sure+to+delete+all+data'
        response = requests.delete(url=url)
        if response.status_code != 204:
            logging.error(json.loads(response.content))
            raise ValueError
