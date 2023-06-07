# Author: HaotianXie (hotinexie@gmail.com)

import json
import requests
import logging
import os

from typing import List, Dict

class HugeGraphClient:
    def __init__(self,
                 hugegraph_serever_ip: str = '0.0.0.0',
                 hugegraph_serever_port: str = '8080',
                 graph: str = 'hugegraph'):
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
            'Content-Type': 'application/json'
        }
        self._hugegraph_serever_ip = hugegraph_serever_ip
        self._hugegraph_serever_port = hugegraph_serever_port
        self._host = 'http://' + self._hugegraph_serever_ip + ':' + self._hugegraph_serever_port
        self._graph = '/graphs/' + graph

    # 1.1
    def get_schema(self):
        url = self._host + self._graph + '/schema'
        response = requests.get(url=url)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 1.2.1
    def create_propertykey(self,
                           name: str,
                           data_type: str = 'TEXT', 
                           cardinality: str = 'SINGLE'):
        url = self._host + self._graph + '/schema/propertykeys'
        request_body = {
            'name': name,
            'data_type': data_type,
            'cardinality': cardinality
        }
        response = requests.post(url=url,
                                 data=json.dumps(request_body),
                                 headers=self._headers)
        if response.status_code != 202:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 1.2.2 add
    def add_userdata_for_propertykey(self, name: str, user_data: Dict):
        url = self._host + self._graph + '/schema/propertykeys/' + name + '?action=append'
        requests_body = {
            'name': name,
            'user_data': user_data
        }
        response = requests.put(url=url,
                                data=json.dumps(requests_body),
                                headers=self._headers)
        if response.status_code != 202:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 1.2.2 eliminate
    def eliminate_userdata_for_propertykey(self, name: str, user_data: Dict):
        url = self._host + self._graph + '/schema/propertykeys/' + name + '?action=eliminate'
        requests_body = {
            'name': name,
            'user_data': user_data
        }
        response = requests.put(url=url,
                                data=json.dumps(requests_body),
                                headers=self._headers)
        if response.status_code != 202:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 1.2.3
    def get_all_propertykeys(self):
        url = self._host + self._graph + '/schema/propertykeys'
        response = requests.get(url=url)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 1.2.4
    def get_propertykey_by_name(self, name: str):
        url = self._host + self._graph + '/schema/propertykeys/' + name
        response = requests.get(url=url)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 1.2.5
    def delete_propertykey_by_name(self, name: str):
        url = self._host + self._graph + '/schema/propertykeys/' + name
        response = requests.delete(url=url)
        if response.status_code != 202:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 1.3.1
    # TODO: add ttl feature support
    def create_vertexlabel(self,
                           name: str,
                           id_strategy: str = 'DEFAULT',
                           properties: List = [],
                           primary_keys: List = [],
                           enable_label_index: bool = False,
                           index_labels: List = [],
                           nullable_keys: List = [],
                           user_data: Dict = {}):
        url = self._host + self._graph + '/schema/vertexlabels'
        request_body = {
            'name': name,
            'id_strategy': id_strategy,
            'properties': properties,
            'primary_keys': primary_keys,
            'enable_label_index': enable_label_index,
            'index_labels': index_labels,
            'nullable_keys': nullable_keys,
            'user_data': user_data
        }
        response = requests.post(url=url,
                                 data=json.dumps(request_body),
                                 headers=self._headers)
        if response.status_code != 201:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 1.3.2 add properties
    def add_properties_for_vertexlabel(self,
                                       name: str,
                                       properties: List,
                                       nullable_keys: List = []):
        url = self._host + self._graph + '/schema/vertexlabels/' + name + '?action=append'
        request_body = {'name': name, 'properties': properties, 'nullable_keys': nullable_keys}
        response = requests.post(url=url,
                                 data=json.dumps(request_body),
                                 headers=self._headers)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 1.3.2 add userdata
    def add_userdata_for_vertexlabel(self,
                                     name: str,
                                     user_data: Dict):
        url = self._host + self._graph + '/schema/vertexlabels/' + name + '?action=append'
        request_body = {'name': name, 'user_data': user_data}
        response = requests.post(url=url,
                                 data=json.dumps(request_body),
                                 headers=self._headers)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 1.3.2 delet userdata
    def eliminate_userdata_for_vertexlabel(self,
                                           name: str,
                                           user_data: Dict):
        url = self._host + self._graph + '/schema/vertexlabels/' + name + '?action=eliminate'
        request_body = {'name': name, 'user_data': user_data}
        response = requests.post(url=url,
                                 data=json.dumps(request_body),
                                 headers=self._headers)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 1.3.3
    def get_all_vertexlabels(self):
        url = self._host + self._graph + '/schema/vertexlabels'
        response = requests.get(url=url)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)
    
    # 1.3.4
    def get_vertexlabel_by_name(self, name: str):
        url = self._host + self._graph + '/schema/vertexlabels/' + name
        response = requests.get(url=url)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)
    
    # 1.3.5
    def delete_vertexlabel_by_name(self, name: str):
        url = self._host + self._graph + '/schema/vertexlabels/' + name
        response = requests.delete(url=url)
        if response.status_code != 202:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 1.4.1
    # TODO: add ttl feature support
    def create_edgelabel(self,
                         name: str,
                         source_label: str,
                         target_label: str,
                         frequency: str = 'SINGLE',
                         properties: List = [],
                         sort_keys: List = [],
                         nullable_keys: List = [],
                         enable_label_index: bool = False):
        url = self._host + self._graph + '/schema/edgelabels'
        request_body = {
            'name': name,
            'source_label': source_label,
            'target_label': target_label,
            'frequency': frequency,
            'properties': properties,
            'sort_keys': sort_keys,
            'nullable_keys': nullable_keys,
            'enable_label_index': enable_label_index
        }
        response = requests.post(url=url,
                                 data=json.dumps(request_body),
                                 headers=self._headers)
        if response.status_code != 201:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 1.4.2 add properties
    def add_properties_for_edgelabel(self,
                                     name: str,
                                     properties: List,
                                     nullable_keys: List = []):
        url = self._host + self._graph + '/schema/edgelabels/' + name + '?action=append'
        request_body = {'name': name, 'properties': properties, 'nullable_keys': nullable_keys}
        response = requests.post(url=url,
                                 data=json.dumps(request_body),
                                 headers=self._headers)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 1.4.2 add userdata
    def add_userdata_for_edgelabel(self,
                                   name: str,
                                   user_data: Dict):
        url = self._host + self._graph + '/schema/edgelabels/' + name + '?action=append'
        request_body = {'name': name, 'user_data': user_data}
        response = requests.post(url=url,
                                 data=json.dumps(request_body),
                                 headers=self._headers)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 1.4.2 delet userdata
    def eliminate_userdata_for_edgelabel(self,
                                         name: str,
                                         user_data: Dict):
        url = self._host + self._graph + '/schema/edgelabels/' + name + '?action=eliminate'
        request_body = {'name': name, 'user_data': user_data}
        response = requests.post(url=url,
                                 data=json.dumps(request_body),
                                 headers=self._headers)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 1.4.3
    def get_all_edgelabels(self):
        url = self._host + self._graph + '/schema/edgelabels'
        response = requests.get(url=url)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)
    
    # 1.4.4
    def get_edgelabel_by_name(self, name: str):
        url = self._host + self._graph + '/schema/edgelabels/' + name
        response = requests.get(url=url)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)
    
    # 1.4.5
    def delete_edgelabel_by_name(self, name: str):
        url = self._host + self._graph + '/schema/edgelabels/' + name
        response = requests.delete(url=url)
        if response.status_code != 202:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 1.5.1
    def create_indexlabel(self,
                          name: str,
                          base_type: str,
                          base_value: str,
                          index_type: str,
                          fields: List):
        url = self._host + self._graph + '/schema/indexlabels'
        request_body = {
            'name': name,
            'base_type': base_type,
            'base_value': base_value,
            'index_type': index_type,
            'fields': fields
        }
        response = requests.post(url=url, data=json.dumps(request_body), headers=self._headers)
        if response.status_code != 202:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 1.5.2
    def get_all_indexlabels(self):
        url = self._host + self._graph + '/schema/indexlabels'
        response = requests.get(url=url)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)
    
    # 1.5.3
    def get_indexlabel_by_name(self, name: str):
        url = self._host + self._graph + '/schema/indexlabels/' + name
        response = requests.get(url=url)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)
    
    # 1.5.4
    def delete_indexlabel_by_name(self, name: str):
        url = self._host + self._graph + '/schema/indexlabels/' + name
        response = requests.delete(url=url)
        if response.status_code != 202:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 5.1.1
    def create_or_update_variable(self, key: str, value: str):
        url = self._host + self._graph + '/variables/' + key
        request_body = {
            'data': value
        }
        response = requests.put(url=url, data=request_body, headers=self._headers)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)
    
    # 5.1.2
    def get_all_variables(self):
        url = self._host + self._graph + '/variables'
        response = requests.get(url=url)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)
    
    # 5.1.3
    def get_variable(self, variable: str):
        url = self._host + self._graph + '/variables/' + variable
        response = requests.get(url=url)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)
    
    # 5.1.4
    def delete_variable(self, variable: str):
        url = self._host + self._graph + '/variables/' + variable
        response = requests.delete(url=url)
        if response.status_code != 204:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 6.1.1
    def get_all_graphs(self):
        url = self._host + '/graphs'
        response = requests.get(url=url)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)

    # 6.1.3
    def delete_graph(self):
        url = self._host + self._graph + '/clear?confirm_message=I%27m+sure+to+delete+all+data'
        response = requests.get(url=url)
        if response.status_code != 204:
            logging.error(json.loads(response.content))
            raise ValueError
        return json.loads(response.content)


    # 8.1
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

