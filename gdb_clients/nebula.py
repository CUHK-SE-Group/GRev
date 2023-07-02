

import time
from nebula3.common.ttypes import ErrorCode
import pandas as pd
from nebula3.gclient.net import Connection
from nebula3.gclient.net.SessionPool import SessionPool
from nebula3.gclient.net.Session import Session
from nebula3.Config import SessionPoolConfig
from nebula3.common import *
from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config
from gdb_clients import GdbFactory
from nebula3.data.ResultSet import ResultSet
from typing import Dict


def result_to_df(result: ResultSet) -> Dict:
    # assert result.is_succeeded()
    columns = result.keys()
    d: Dict[str, list] = {}
    for col_num in range(result.col_size()):
        col_name = columns[col_num]
        col_list = result.column_values(col_name)
        d[col_name] = [x.cast() for x in col_list]
    print(f'Result size = {len(d)}')
    return d

class Nebula(GdbFactory):
    def __init__(self,database="defaultdb", reset=True):
        self.database = database
        config = Config()
        connection_pool = ConnectionPool()
        ok = connection_pool.init([('graphd', 9669)], config)
        if reset:
            with connection_pool.session_context('root', 'nebula') as session:
                session.execute(f'DROP SPACE IF EXISTS {self.database}')
                result = result_to_df(session.execute(f'CREATE SPACE IF NOT EXISTS {self.database} (vid_type=FIXED_STRING(30))'))
                assert result != None
        self.get_session()

    def get_session(self):
        sessionPoolConfig = SessionPoolConfig()
        self.sessionPool = SessionPool("root", "nebula", self.database, [("graphd", 9669)])
        ok = self.sessionPool.init(sessionPoolConfig)
        if not ok:
            exit(1)

    def run(self, query):
        print("query len:", len(query))
        try:
            result = self.sessionPool.execute(query)            
        except Exception as ex:
            self.get_session()
            raise
        if not result.is_succeeded():
            raise Exception(result._resp)
        df = result_to_df(result)
        return df, result.latency()
    
    def batch_run(self, query):
        for q in query:
            self.sessionPool.execute(q)

    def clear(self):
        # Do nothing in this case
        pass
        # with self.get_session() as session:
        #     result = result_to_df(session.execute(f'CLEAR SPACE {self.database}'))
        #     assert result != None


if __name__ == '__main__':
    nb = Nebula("nbtest")

    with open('./gdb_clients/graph.log', 'r') as f:
        while True:
            statement = f.readline()
            if statement == '':
                break
            if statement.startswith("SLEEP"):
                time.sleep(10)
            else:
                assert(nb.run(statement)[0] != None)


    # nb.clear()
