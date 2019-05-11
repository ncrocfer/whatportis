# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify

from whatportis.db import get_database, get_ports


app = Flask(__name__)


@app.route("/ports", methods=["GET"])
def all_ports():
    """Returns all ports"""
    return jsonify({"ports": get_database().all()})


@app.route("/ports/<pattern>", methods=["GET"])
def specific_ports(pattern):
    """Returns all ports matching the given pattern"""
    like = "like" in request.args
    return jsonify({"ports": get_ports(pattern, like)})
