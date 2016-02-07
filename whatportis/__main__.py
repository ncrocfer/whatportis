# -*- coding: utf-8 -*-

"""
    command line interface for whatportis application.
"""

import click
from prettytable import PrettyTable

from .core import get_ports


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
def run(port, like):
    """Search port names and numbers."""
    ports = get_ports(port, like)
    if not ports:
        print("No ports found for '{0}'".format(port))
    else:
        table = get_table(ports)
        print(table)
