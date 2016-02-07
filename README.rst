Whatportis: a command to search port names and numbers
======================================================

.. image:: https://travis-ci.org/ncrocfer/whatportis.svg?branch=master
    :target: https://travis-ci.org/ncrocfer/whatportis

It often happens that we need to find the default port number for a specific service, or what service is listening on a given port.

Usage
-----

This tool allows you to find what port is associated with a service :

.. code-block:: shell

    $ whatportis redis
    +-------+------+----------+---------------------------------------+
    | Name  | Port | Protocol | Description                           |
    +-------+------+----------+---------------------------------------+
    | redis | 6379 |   tcp    | An advanced key-value cache and store |
    +-------+------+----------+---------------------------------------+

Or, conversely, what service is associated with a port number :

.. code-block:: shell

    $ whatportis 5432
    +------------+------+----------+---------------------+
    | Name       | Port | Protocol | Description         |
    +------------+------+----------+---------------------+
    | postgresql | 5432 |   tcp    | PostgreSQL Database |
    | postgresql | 5432 |   udp    | PostgreSQL Database |
    +------------+------+----------+---------------------+

Or, start whatportis as a RESTful API server:

.. code-block:: shell

   $ whatportis --server localhost 8080
    * Running on http://localhost:8080/ (Press CTRL+C to quit)

   $ curl http://localhost:8080/ports
   "ports": [
     {
       "description": "Description",
       "name": "Service Name",
       "port": "Port Number",
       "protocol": "Transport Protocol"
     },
   ...

   $ curl http://localhost:8080/ports/3306
   {
     "ports": [
       [
         "mysql",
         "3306",
         "tcp",
         "MySQL"
       ],
       [
         "mysql",
         "3306",
         "udp",
         "MySQL"
       ]
     ]
   }

   $ curl http://localhost:8080/ports/mysql\?like
   {
     "ports": [
       [
         "mysql-cluster",
         "1186",
         "tcp",
         "MySQL Cluster Manager"
       ],
       [
         "mysql-cluster",
         "1186",
         "udp",
         "MySQL Cluster Manager"
       ],
       ...


Installation
------------

.. code-block:: shell

    $ pip install whatportis


Notes
-----

- You can search a pattern without knowing the exact name by adding the :code:`--like` option :

.. code-block:: shell

    $ whatportis mysql --like
    +----------------+-------+----------+-----------------------------------+
    | Name           |  Port | Protocol | Description                       |
    +----------------+-------+----------+-----------------------------------+
    | mysql-cluster  |  1186 |   tcp    | MySQL Cluster Manager             |
    | mysql-cluster  |  1186 |   udp    | MySQL Cluster Manager             |
    | mysql-cm-agent |  1862 |   tcp    | MySQL Cluster Manager Agent       |
    | mysql-cm-agent |  1862 |   udp    | MySQL Cluster Manager Agent       |
    | mysql-im       |  2273 |   tcp    | MySQL Instance Manager            |
    | mysql-im       |  2273 |   udp    | MySQL Instance Manager            |
    | mysql          |  3306 |   tcp    | MySQL                             |
    | mysql          |  3306 |   udp    | MySQL                             |
    | mysql-proxy    |  6446 |   tcp    | MySQL Proxy                       |
    | mysql-proxy    |  6446 |   udp    | MySQL Proxy                       |
    | mysqlx         | 33060 |   tcp    | MySQL Database Extended Interface |
    +----------------+-------+----------+-----------------------------------+

- "Why not use :code:`grep <port> /etc/services`" ? Simply because I want a portable command that display the output in a nice format (a pretty table).

- You can also display the results as JSON, using the :code:`--json` option:

.. code-block:: shell

    $ whatportis 5432 --json
    [
        {
            "description": "PostgreSQL Database",
            "protocol": "tcp",
            "name": "postgresql",
            "port": "5432"
        },
        {
            "description": "PostgreSQL Database",
            "protocol": "udp",
            "name": "postgresql",
            "port": "5432"
        }
    ]

- The tool uses the `Iana.org <http://www.iana.org/assignments/port-numbers>`_ website to get the official list of ports. A private script has been created to fetch regularly the website and update the **ports.json** file. For this reason, an :code:`update` command will be created in a future version.
