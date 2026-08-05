import sys
import click
from main import create_app
from extensions import db

app = create_app()


@click.group()
def cli():
    pass


@cli.command("initdb")
def initdb_command():
    """Initialize the database (create tables)."""
    db.create_all()
    click.echo("Initialized the database.")


@cli.command("seed")
def seed_command():
    """Seed the database with sample data from seed.py"""
    from seed import seed_database
    seed_database()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli()
    else:
        app.run(host="0.0.0.0", port=5000)
