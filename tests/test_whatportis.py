import unittest
import re

from click.testing import CliRunner
from whatportis.__main__ import run
from whatportis.core import merge_protocols


class CliTestCase(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def tearDown(self):
        pass

    def test_search_with_no_arg(self):
        result = self.runner.invoke(run, [])
        regex = re.compile('^Usage:')
        self.assertEqual(result.exit_code, 2)
        self.assertTrue(regex.match(result.output))

    def test_search_with_multiple_args(self):
        result = self.runner.invoke(run, ['foo', 'bar'])
        regex = re.compile('^Usage:')
        self.assertEqual(result.exit_code, 2)
        self.assertTrue(regex.match(result.output))

    def test_search_str_port(self):
        result = self.runner.invoke(run, ['redis'])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue("redis" in result.output)
        self.assertTrue("6379" in result.output)
        self.assertTrue("tcp" in result.output)
        output = "An advanced key-value cache and store"
        self.assertTrue(output in result.output)

    def test_search_int_port(self):
        result = self.runner.invoke(run, ['3306'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.count('mysql'), 1)
        self.assertEqual(result.output.count('3306'), 1)
        self.assertTrue("tcp" in result.output)
        self.assertTrue("udp" in result.output)

    def test_search_str_like_port(self):
        result = self.runner.invoke(run, ['mysql', '--like'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.count('mysql'), 6)
        self.assertEqual(result.output.count('tcp'), 6)
        self.assertEqual(result.output.count('udp'), 5)

    def test_search_int_like_port(self):
        result = self.runner.invoke(run, ['3306', '--like'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.count('mysql'), 2)
        self.assertEqual(result.output.count('tcp'), 2)
        self.assertEqual(result.output.count('udp'), 2)


class UtilsTestCase(unittest.TestCase):
    def test_merge_protocols_different_ports(self):
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
        self.assertEqual(result, ports)

    def test_merge_protocols_same_port(self):
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
        self.assertEqual(result, [{
            "description": "My description",
            "name": "MyName",
            "port": "1234",
            "protocol": "udp, tcp"
        }])


if __name__ == '__main__':
    unittest.main()
