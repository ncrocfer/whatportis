import os
import sqlite3

import click
from prettytable import PrettyTable


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_PATH, 'ports.db')
BASE_SQL = "SELECT name, port, protocol, description FROM ports WHERE "


def valid_port(ctx, param, value):
    """
    This function tries to cast the port to integer. If it's not possible, the
    initial string value is returned.

    :param ctx: the click context
    :param param: the click param
    :param value: the port name or number
    :return: the port as a string or integer
    """
    try:
        value = int(value)
    except ValueError:
        pass

    return value


def get_ports(port, like=False):
    """
    This function creates the SQL query depending on the specified port and
    the --like option.

    :param port: the specified port
    :param like: the --like option
    :return: the sqlite3 cursor
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    where_field = "port" if isinstance(port, int) else "name"
    where_value = "%{}%".format(port) if like else port

    cursor.execute(BASE_SQL + where_field + " LIKE ?", (where_value,))

    return cursor


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

    for p in ports:
        table.add_row(p)

    return table


@click.command()
@click.version_option()
@click.argument('PORT', required=True, callback=valid_port)
@click.option('--like', is_flag=True, default=False,
              help='Search ports containing the pattern.')
def run(port, like):
    """Search port names and numbers."""
    ports = get_ports(port, like)
    table = get_table(ports)
    print(table)
