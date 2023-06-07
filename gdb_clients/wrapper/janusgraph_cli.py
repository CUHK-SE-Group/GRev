# Author: HaotianXie (hotinexie@gmail.com)

import click

from janusgraph_client import JanusGraphClient


@click.group()
def cli():
    pass


@cli.command()
@click.argument('gremlin_instruction')
def send_gremlin(gremlin_instruction: str):
    JanusGraph_Client = JanusGraphClient()
    response_content = JanusGraph_Client.send_gremlin(gremlin=gremlin_instruction)
    #print(len(response_content["result"]))
    click.echo(response_content)


@cli.command()
def delete_graph():
    JanusGraph_Client = JanusGraphClient()
    JanusGraph_Client.delete_all_graphs()


if __name__ == '__main__':
    cli()
