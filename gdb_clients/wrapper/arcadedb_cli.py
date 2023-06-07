# Author: HaotianXie (hotinexie@gmail.com)

import click

from arcadedb_client import ArcadeDBClient


@click.group()
def cli():
    pass


@cli.command()
@click.argument('gremlin_instruction')
def send_gremlin(gremlin_instruction: str):
    ArcadeDB_Client = ArcadeDBClient()
    response_content = ArcadeDB_Client.send_gremlin(gremlin=gremlin_instruction)
    #print(len(response_content["result"]))
    click.echo(response_content)


@cli.command()
def delete_graph():
    ArcadeDB_Client = ArcadeDBClient()
    ArcadeDB_Client.delete_all_graphs()


if __name__ == '__main__':
    cli()
