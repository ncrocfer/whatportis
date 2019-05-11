whatportis
==========

.. image:: https://travis-ci.org/ncrocfer/whatportis.svg?branch=master
   :target: https://travis-ci.org/ncrocfer/whatportis

.. image:: https://badge.fury.io/py/whatportis.svg
   :target: https://pypi.python.org/pypi/whatportis/

.. image:: https://img.shields.io/badge/python-2.x%20|%C2%A03.x-blue.svg
   :target: https://pypi.python.org/pypi/whatportis/

.. image:: https://img.shields.io/github/license/ncrocfer/whatportis.svg
   :target: https://github.com/ncrocfer/whatportis/blob/master/LICENSE.txt

It's a common task to search the default port number of a service. Some ports are available in the :code:`/etc/services` file, but the list is not complete and this solution is not portable.

Whatportis is a simple tool that downloads the `Iana.org <http://www.iana.org/assignments/port-numbers>`_ database and uses it to explore the official list of ports.

Usage
-----

Whatportis allows you to find what port is associated with a service:

.. code-block:: shell

    $ whatportis redis
    +-------+------+----------+---------------------------------------+
    | Name  | Port | Protocol | Description                           |
    +-------+------+----------+---------------------------------------+
    | redis | 6379 |   tcp    | An advanced key-value cache and store |
    +-------+------+----------+---------------------------------------+

Or, conversely, what service is associated with a port number:

.. code-block:: shell

    $ whatportis 5432
    +------------+------+----------+---------------------+
    | Name       | Port | Protocol | Description         |
    +------------+------+----------+---------------------+
    | postgresql | 5432 | tcp, udp | PostgreSQL Database |
    +------------+------+----------+---------------------+

You can also search a pattern without knowing the exact name by adding the :code:`--like` option:

.. code-block:: shell

    $ whatportis mysql --like
    +----------------+-------+----------+-----------------------------------+
    | Name           |  Port | Protocol | Description                       |
    +----------------+-------+----------+-----------------------------------+
    | mysql-cluster  |  1186 | tcp, udp | MySQL Cluster Manager             |
    | mysql-cm-agent |  1862 | tcp, udp | MySQL Cluster Manager Agent       |
    | mysql-im       |  2273 | tcp, udp | MySQL Instance Manager            |
    | mysql          |  3306 | tcp, udp | MySQL                             |
    | mysql-proxy    |  6446 | tcp, udp | MySQL Proxy                       |
    | mysqlx         | 33060 |   tcp    | MySQL Database Extended Interface |
    +----------------+-------+----------+-----------------------------------+

Installation
------------

.. code-block:: shell

    $ pip install whatportis

Whatportis uses a local JSON file (:code:`~/.whatportis_db.json`) to explore the list of ports. You can synchronize it using the :code:`--update` option :

.. code-block:: shell

    $ whatportis --update
    Previous database will be updated, do you want to continue? [y/N]: y
    Downloading https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv...
    Populating database...
    14145 ports imported.

JSON output
-----------

You can display the results as JSON, using the :code:`--json` option :

.. code-block:: shell

    $ whatportis 5432 --json
    [
        {
            "name": "postgresql",
            "port": "5432",
            "protocol": "tcp, udp",
            "description": "PostgreSQL Database"
        }
    ]

REST API
--------

Whatportis can also be started as a RESTful API server. This feature is not enabled by default, you must install an extra package :

.. code-block:: shell

    $ pip install whatportis[server]
    $ whatportis --server localhost 8080
     * Serving Flask app "whatportis.server" (lazy loading)
     * Environment: prod
     * Debug mode: off
     * Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)

The endpoints are :code:`/ports` for the whole list (can be long) and :code:`/ports/<search>` to search a specific port :

.. code-block:: shell

    $ curl http://127.0.0.1:8080/ports/3306
    {"ports":[{"description":"MySQL","name":"mysql","port":"3306","protocol":"tcp, udp"}]}

    $ curl http://localhost:8080/ports/redis
    {"ports":[{"description":"An advanced key-value cache and store","name":"redis","port":"6379","protocol":"tcp"}]}

You can use the :code:`?like` parameter to search a pattern.
