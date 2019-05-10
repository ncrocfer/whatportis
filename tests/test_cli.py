import re

from whatportis.__main__ import run


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


def test_search_str_port(runner):
    result = runner.invoke(run, ['redis'])
    assert result.exit_code == 0
    assert "redis" in result.output
    assert "6379" in result.output
    assert "tcp" in result.output
    assert "An advanced key-value cache and store" in result.output


def test_search_int_port(runner):
    result = runner.invoke(run, ['3306'])
    assert result.exit_code == 0
    assert result.output.count('mysql') == 1
    assert result.output.count('3306') == 1
    assert "tcp" in result.output
    assert "udp" in result.output


def test_search_str_like_port(runner):
    result = runner.invoke(run, ['mysql', '--like'])
    assert result.exit_code == 0
    assert result.output.count('mysql') == 6
    assert result.output.count('tcp') == 6
    assert result.output.count('udp') == 5


def test_search_int_like_port(runner):
    result = runner.invoke(run, ['3306', '--like'])
    assert result.exit_code == 0
    assert result.output.count('mysql') == 2
    assert result.output.count('tcp') == 2
    assert result.output.count('udp') == 2
