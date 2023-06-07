# Author: HaotianXie (hotinexie@gmail.com)

import json
import requests
import logging
import os

from typing import List, Dict

class JanusGraphClient:
    def __init__(self,
                 janusgraph_serever_ip: str = '0.0.0.0',
                 janusgraph_serever_port: str = '10086'):
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
            'Content-Type': 'application/json',
        }
        self._janusgraph_serever_ip = janusgraph_serever_ip
        self._janusgraph_serever_port = janusgraph_serever_port
        self._host = 'http://' + self._janusgraph_serever_ip + ':' + self._janusgraph_serever_port

    def send_gremlin(self, gremlin: str):
        url = self._host
        request_body = {'gremlin': gremlin}
        response = requests.post(url=url, data=json.dumps(request_body), headers=self._headers)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    def delete_all_graphs(self):
        url = self._host
        self.send_gremlin("g.V().properties().drop().iterate()")
        self.send_gremlin("g.E().properties().drop().iterate()")
        request_body = {'gremlin': 'g.V().drop().iterate()'}
        response = requests.post(url=url, data=json.dumps(request_body), headers=self._headers)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)


client = JanusGraphClient()
print(client.send_gremlin('g.V().find()'))
# client.delete_all_graphs()