import click

from k8s.main import create_cluster

@click.group()
def cludt():
    pass

@cludt.group()
def k8s():
    pass

@k8s.group()
def init():
    pass

@init.command()
def local():
    create_cluster()