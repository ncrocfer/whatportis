from whatportis.db import merge_protocols


def test_merge_protocols_different_ports():
    ports = [{
        "description": "My description 1",
        "name": "MyName 1",
        "port": "1234",
        "protocol": "udp"
    }, {
        "description": "My description 2",
        "name": "MyName 2",
        "port": "5678",
        "protocol": "tcp"
    }]
    result = merge_protocols(ports)
    assert sorted(result, key=lambda p: p["name"]) == sorted(ports, key=lambda p: p["name"])


def test_merge_protocols_same_port():
    ports = [{
        "description": "My description",
        "name": "MyName",
        "port": "1234",
        "protocol": "udp"
    }, {
        "description": "My description",
        "name": "MyName",
        "port": "1234",
        "protocol": "tcp"
    }]
    result = merge_protocols(ports)
    assert result == [{
        "description": "My description",
        "name": "MyName",
        "port": "1234",
        "protocol": "udp, tcp"
    }]
