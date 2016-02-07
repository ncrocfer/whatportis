# -*- coding: utf-8 -*-

"""
    command line interface for whatportis application.
"""

import sys
import click
import json

from prettytable import PrettyTable

from .core import get_ports, get_dict
from .server import app


def get_table(ports):
    """
    This function returns a pretty table used to display the port results.

    :param ports: list of found ports
    :return: the table to display
    """
    table = PrettyTable(["Name", "Port", "Protocol", "Description"])
    table.align["Name"] = "l"
    table.align["Description"] = "l"
    table.padding_width = 1

    for port in ports:
        table.add_row(port)

    return table


@click.command()
@click.version_option()
@click.argument('PORT', required=False)
@click.option('--like', is_flag=True, default=False,
              help='Search ports containing the pattern.')
@click.option('--json', "use_json", is_flag=True, default=False,
              help='Format the output result as JSON.')
@click.option("--server", type=(str, int), default=(None, None),
              help="Start a RESTful server (Format <host> <port>).")
def run(port, like, use_json, server):
    """Search port names and numbers."""
    if not port and not server[0]:
        raise click.UsageError("Please specify a port")

    if server[0]:
        app.run(host=server[0], port=server[1])
        return

    ports = get_ports(port, like)
    if not ports:
        sys.stderr.write("No ports found for '{0}'\n".format(port))
        return

    if use_json:
        print(json.dumps(get_dict(ports), indent=4))
    else:
        table = get_table(ports)
        print(table)
