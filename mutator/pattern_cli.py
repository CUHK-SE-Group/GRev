import click
from mutator.pattern_transformer import *

@click.group()
def cli():
    pass

@cli.command()
@click.argument('pattern')
def trans(pattern: str):
    p = PatternTransformer()
    asg = p.pattern2asg(pattern)
    pattern1 = p.asg2pattern(asg)
    click.echo(pattern1)

if __name__ == '__main__':
    cli()