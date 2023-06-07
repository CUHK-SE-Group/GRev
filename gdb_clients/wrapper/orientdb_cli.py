# Author: HaotianXie (hotinexie@gmail.com)

import click

from orientdb_client import OrientDbClient


@click.group()
def cli():
    pass


@cli.command()
@click.argument('gremlin_instruction')
def send_gremlin(gremlin_instruction: str):
    OrientDb_Client = OrientDbClient()
    response_content = OrientDb_Client.send_gremlin(gremlin=gremlin_instruction)
    click.echo(response_content)


@cli.command()
def delete_graph():
    OrientDb_Client = OrientDbClient()
    OrientDb_Client.delete_all_graphs()


if __name__ == '__main__':
    cli()
