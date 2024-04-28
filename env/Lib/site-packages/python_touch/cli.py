import click
from pathlib import Path
from . import PythonTouch


@click.command()
@click.argument("directory")
def main(directory):
    x = PythonTouch()
    x.touch(directory)
