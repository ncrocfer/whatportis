# -*- coding: utf-8 -*-

"""
    command line interface for whatportis application.
"""

import click
import json as jsonmod

from prettytable import PrettyTable

from .core import get_ports, get_dict


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
@click.argument('PORT', required=True)
@click.option('--like', is_flag=True, default=False,
              help='Search ports containing the pattern.')
@click.option('--json', is_flag=True, default=False,
              help='Format the output result as JSON.')
def run(port, like, json):
    """Search port names and numbers."""
    ports = get_ports(port, like)
    if not ports:
        print("No ports found for '{0}'".format(port))
    if json:
        print(jsonmod.dumps(get_dict(ports), indent=4))
    else:
        table = get_table(ports)
        print(table)
