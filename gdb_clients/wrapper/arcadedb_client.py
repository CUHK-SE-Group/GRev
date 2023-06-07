# Author: HaotianXie (hotinexie@gmail.com)

import json
import requests
import logging
import os

from typing import List, Dict

class ArcadeDBClient:
    def __init__(self,
                 arcadedb_serever_ip: str = '0.0.0.0',
                 arcadedb_serever_port: str = '3480'):
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
            'Content-Type': 'application/json',
        }
        self._arcadedb_serever_ip = arcadedb_serever_ip
        self._arcadedb_serever_port = arcadedb_serever_port
        self._graph = '/graph'
        self._host = 'http://' + self._arcadedb_serever_ip + ':' + self._arcadedb_serever_port + '/api/v1/command' + self._graph

    def send_gremlin(self, gremlin: str):
        url = self._host
        request_body = {'language': 'gremlin', 'command': gremlin}
        response = requests.post(
            url=url,
            data=json.dumps(request_body),
            headers=self._headers,
            auth=('root', 'playwithdata'),
        )
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    def delete_all_graphs(self):
        url = self._host
        request_body = {'language': 'gremlin', 'command': 'g.V().drop().iterate()'}
        response = requests.post(
            url=url,
            data=json.dumps(request_body),
            headers=self._headers,
            auth=('root', 'playwithdata'),
        )
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)
