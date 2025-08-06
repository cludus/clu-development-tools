import click

@click.group()
def cli():
    """A simple CLI application."""
    pass

@cli.command()
def k8s():
    """Says hello."""
    click.echo("Hello, World!")