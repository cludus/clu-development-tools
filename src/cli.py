import click


@click.group()
def cli():
    """A simple CLI application."""
    pass


@cli.command()
def hello():
    """Says hello."""
    click.echo("Hello, World!")