from gdb_clients.tinkerpop import Tinkerpop
from reproduce.test_helper import run_test_from_file


if __name__ == "__main__":
    client = Tinkerpop()

    # 2961
    run_test_from_file(client=client,
                       create_statements_file="./reproduce/tinkerpop/tinkerpop-2961.log",
                       query_statements=[
                           f'g.V().match(__.as("n2").out().as("n1"),__.as("n2").in().in().in().both().in().as("n1"),__.as("n2").both().in().in().as("n3"),__.as("n3").in().both().as("n2"),__.as("n2").in().in().in().in().both().as("n4"),__.as("n2").out().both().in().as("n4"),__.as("n3").both().as("n4"),__.as("n1").in().both().both().both().as("n5")).dedup().count()',
                           f'g.V().match(__.as("n2").out().as("n1"), __.as("n2").in().in().in().both().in().as("n1"), __.as("n2").both().in().in().as("n3"), __.as("n3").in().both().as("n2"), __.as("n4").both().out().out().out().out().as("n2"), __.as("n2").out().both().in().as("n4"), __.as("n3").both().as("n4"), __.as("n1").in().both().both().both().as("n5")).dedup().count()'
                       ], message="Running Tinkerpop-2961:")
