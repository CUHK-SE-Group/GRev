import requests
import click
from configs import config

@click.group()
def cli():
    pass


@cli.command()
@click.argument('cypher_instruction')
def command(query):
    print(cypher2gremlin(query))

def cypher2gremlin(query):
    url = f'http://{config.get("cypher2gremlin", "host")}:8080/transform'
    headers = {'Content-Type': 'application/json'}
    data = {
        "query": query
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['query']

if __name__ == '__main__':
    cli()
