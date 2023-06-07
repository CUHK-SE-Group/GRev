import requests
import click

@click.group()
def cli():
    pass


@cli.command()
@click.argument('cypher_instruction')
def command(query):
    print(cypher2gremlin(query))

def cypher2gremlin(query):
    url = 'http://127.0.0.1:8085/greeting'
    headers = {'Content-Type': 'application/json'}
    data = {
        "query": query
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['query']

if __name__ == '__main__':
    cli()
