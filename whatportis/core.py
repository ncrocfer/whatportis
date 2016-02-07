# -*- coding: utf-8 -*-

"""
    Provides functionality to search a port
    database for specific applications and
    their ports.
"""

import os
import sqlite3
from collections import namedtuple

__BASE_PATH__ = os.path.dirname(os.path.abspath(__file__))
__DATABASE_PATH__ = os.path.join(__BASE_PATH__, 'ports.db')
__BASE_SQL__ = "SELECT name, port, protocol, description FROM ports WHERE "

Port = namedtuple("Port", ["name", "port", "protocol", "description"])


def get_ports(port, like=False):
    """
    This function creates the SQL query depending on the specified port and
    the --like option.

    :param port: the specified port
    :param like: the --like option
    :return: all ports matching the given ``port``
    :rtype: list
    """
    conn = sqlite3.connect(__DATABASE_PATH__)
    cursor = conn.cursor()

    where_field = "port" if isinstance(port, int) else "name"
    where_value = "%{}%".format(port) if like else port

    cursor.execute(__BASE_SQL__ + where_field + " LIKE ?", (where_value,))
    return [Port(*row) for row in cursor]
