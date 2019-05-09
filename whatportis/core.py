# -*- coding: utf-8 -*-

"""
    Provides functionality to search a port
    database for specific applications and
    their ports.
"""

import os
from tinydb import TinyDB, where
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from collections import namedtuple

Port = namedtuple("Port", ["name", "port", "protocol", "description"])

__BASE_PATH__ = os.path.dirname(os.path.abspath(__file__))
__DATABASE_PATH__ = os.path.join(__BASE_PATH__, 'ports.json')
__DB__ = TinyDB(__DATABASE_PATH__, storage=CachingMiddleware(JSONStorage))


def merge_protocols(ports=[]):
    """
    This function merge rows having the exact same data (port, name,
    description) but a different protocol.

    :param ports: the list of ports
    :return: all ports with merged protocols
    :rtype: list
    """
    keys = {}
    for port in ports:
        key = "{}-{}-{}".format(port.get("description"), port.get("name"), port.get("port"))
        if key not in keys:
            keys[key] = port
        else:
            keys[key]["protocol"] += ", {}".format(port.get("protocol"))
    return list(keys.values())


def get_ports(port, like=False):
    """
    This function creates the SQL query depending on the specified port and
    the --like option.

    :param port: the specified port
    :param like: the --like option
    :return: all ports matching the given ``port``
    :rtype: list
    """
    where_field = "port" if port.isdigit() else "name"
    if like:
        ports = __DB__.search(where(where_field).search(port))
    else:
        ports = __DB__.search(where(where_field) == port)

    ports = merge_protocols(ports)
    return [Port(**port) for port in ports] # flake8: noqa (F812)
