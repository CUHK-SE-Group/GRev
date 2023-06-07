# Author: HaotianXie (hotinexie@gmail.com)

import click

from tinkergraph_client import TinkerGraphClient


@click.group()
def cli():
    pass


@cli.command()
@click.argument('gremlin_instruction')
def send_gremlin(gremlin_instruction: str):
    TinkerGraph_Client = TinkerGraphClient()
    response_content = TinkerGraph_Client.send_gremlin(gremlin=gremlin_instruction)
    click.echo(response_content)


@cli.command()
def delete_graph():
    TinkerGraph_Client = TinkerGraphClient()
    TinkerGraph_Client.delete_all_graphs()


if __name__ == '__main__':
    cli()
