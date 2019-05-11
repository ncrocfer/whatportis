import json
import re

from whatportis.cli import run


def test_search_with_no_arg(runner):
    result = runner.invoke(run, [])
    regex = re.compile('^Usage:')
    assert result.exit_code == 2
    assert regex.match(result.output)


def test_search_with_multiple_args(runner):
    result = runner.invoke(run, ['foo', 'bar'])
    regex = re.compile('^Usage:')
    assert result.exit_code == 2
    assert regex.match(result.output)


def test_search_str_port(runner, create_ports):
    create_ports([["foo", "1234", "My description", "tcp"]])
    result = runner.invoke(run, ['foo'])
    assert result.exit_code == 0
    assert "foo" in result.output
    assert "1234" in result.output
    assert "My description" in result.output
    assert "tcp" in result.output


def test_search_int_port(runner, create_ports):
    create_ports([["foo", "1234", "My description", "tcp"]])
    result = runner.invoke(run, ['1234'])
    assert result.exit_code == 0
    assert "foo" in result.output
    assert "1234" in result.output
    assert "My description" in result.output
    assert "tcp" in result.output


def test_search_str_like_port(runner, create_ports):
    create_ports([
        ["foo", "1", "My description", "tcp"],
        ["foobar", "2", "My description", "udp"],
        ["baz", "3", "My description", "tcp"]
    ])

    result = runner.invoke(run, ['foo', '--like'])
    assert result.exit_code == 0
    assert result.output.count('foo') == 2

    result = runner.invoke(run, ['bar', '--like'])
    assert result.exit_code == 0
    assert result.output.count('bar') == 1


def test_search_int_like_port(runner, create_ports):
    create_ports([
        ["foo", "8", "My description", "tcp"],
        ["foobar", "9", "My description", "udp"],
        ["baz", "80", "My description", "tcp"]
    ])

    result = runner.invoke(run, ['8', '--like'])
    assert result.exit_code == 0
    assert result.output.count('8') == 2


def test_search_port_returns_json(runner, create_ports):
    create_ports([["foo", "1234", "My description", "tcp"]])
    result = runner.invoke(run, ['--json', 'foo'])

    result = json.loads(result.output)
    wanted = [{
        'description': 'My description',
        'name': 'foo',
        'port': '1234',
        'protocol': 'tcp'
    }]
    assert sorted(result, key=lambda p: p["name"]) == sorted(wanted, key=lambda p: p["name"])
