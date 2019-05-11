# -*- coding: utf-8 -*-

import csv
import os

import click
import requests
import simplejson as json
from tinydb import TinyDB

from whatportis.db import get_database, get_ports
from whatportis.utils import as_table


IANA_CSV_FILE = "https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv"


def update_db(ctx, param, value):
    """
    This callback downloads the official CSV file provided by IANA,
    parses it and populates the database as a JSON file.
    """
    if not value or ctx.resilient_parsing:
        return

    # Check if the file exists
    if not click.confirm('Previous database will be updated, do you want to continue?'):
        click.echo("Bye.")
        ctx.exit()

    # Download the csv
    click.echo("Downloading {}...".format(IANA_CSV_FILE))
    resp = requests.get(IANA_CSV_FILE).content.decode("utf-8")
    data = csv.reader(resp.splitlines())

    # Populate the json
    click.echo("Populating database...")
    ports = []
    for port in data:
        ports.append({
            "name": port[0] if port[0] else "---",
            "port": port[1] if port[1] else "---",
            "protocol": port[2] if port[2] else "---",
            "description": port[3] if port[3] else "---"
        })

    db = get_database()
    db.purge()
    db.insert_multiple(ports)
    db.close()

    click.echo("{} ports imported.".format(len(ports)))
    ctx.exit()


# Change the server help if flask is installed
server_help = "Start a RESTful server"
try:
    import flask
    server_help += " (format <host> <port>)."
except ImportError:
    server_help += " (requires Flask)."


@click.command()
@click.version_option()
@click.argument('PORT', required=False)
@click.option('--like', is_flag=True, default=False,
              help='Search ports containing the pattern.')
@click.option('--json', "use_json", is_flag=True, default=False,
              help='Format the output result as JSON.')
@click.option("--server", default=[None] * 2, type=click.Tuple([str, int]),
              help=server_help)
@click.option("--update", is_flag=True, callback=update_db,
              expose_value=False, is_eager=True)
def run(port, like, use_json, server):
    """Search port names and numbers."""
    if not port and not server[0]:
        raise click.UsageError("Please specify a port")

    if server[0]:
        try:
            from whatportis.server import app
            app.run(host=server[0], port=server[1])
        except ImportError:
            click.echo("Dependencies are missing, please use `pip install whatportis[server]`.")
        return

    ports = get_ports(port, like)
    if not ports:
        click.echo("No ports found for '{0}'".format(port))
        return

    if use_json:
        print(json.dumps(ports, indent=4))
    else:
        table = as_table(ports)
        print(table)
