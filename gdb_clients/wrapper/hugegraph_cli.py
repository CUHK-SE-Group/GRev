# Author: HaotianXie (hotinexie@gmail.com)

import click

from hugegraph_gremlin_client_plus import HugeGraphClient


@click.group()
def cli():
    pass


@cli.command()
@click.argument('gremlin_instruction')
def send_gremlin(gremlin_instruction: str):
    hugegraph_client = HugeGraphClient()
    response_content = hugegraph_client.send_gremlin(gremlin=gremlin_instruction)
    click.echo(response_content)


@cli.command()
def delete_graph():
    hugegraph_client = HugeGraphClient()
    hugegraph_client.delete_all_graphs()


if __name__ == '__main__':
    cli()
