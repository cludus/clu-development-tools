import click

from k8s.main import create_cluster

@click.group()
def cli():
    """A simple CLI application."""
    pass

@cli.command()
def k8s():
    create_cluster()