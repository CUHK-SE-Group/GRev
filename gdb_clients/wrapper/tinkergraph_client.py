# Author: HaotianXie (hotinexie@gmail.com)

import json
import requests
import logging
import os
# from func_timeout import func_set_timeout
from typing import List, Dict

class TinkerGraphClient:
    def __init__(self,
                 janusgraph_serever_ip: str = '10.26.1.146',
                 janusgraph_serever_port: str = '11109'):
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
        # print('before')
        response = requests.post(url=url, data=json.dumps(request_body), headers=self._headers)
        # print('after')
        if response.status_code != 200:
            raise ValueError(response.content)
        return json.loads(response.content)

    def delete_all_graphs(self):
        url = self._host
        request_body = {'gremlin': 'g.V().drop()'}
        response = requests.post(url=url, data=json.dumps(request_body), headers=self._headers)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

client = TinkerGraphClient()
# print('test')
# # print(client.send_gremlin('JanusGraphFactory.getGraphNames()'))
# print(client.send_gremlin('g.V().count()'))
