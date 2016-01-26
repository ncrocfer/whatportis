import unittest
import re

import click
from click.testing import CliRunner
from whatportis.main import run


class WhatportisTestCase(unittest.TestCase):
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
        self.assertTrue("An advanced key-value cache and store" in result.output)

    def test_search_int_port(self):
        result = self.runner.invoke(run, ['3306'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.count('mysql'), 2)
        self.assertEqual(result.output.count('3306'), 2)
        self.assertTrue("tcp" in result.output)
        self.assertTrue("udp" in result.output)

    def test_search_str_like_port(self):
        result = self.runner.invoke(run, ['mysql', '--like'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.count('mysql'), 11)
        self.assertEqual(result.output.count('tcp'), 6)
        self.assertEqual(result.output.count('udp'), 5)

    def test_search_int_like_port(self):
        result = self.runner.invoke(run, ['3306', '--like'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.count('mysql'), 3)
        self.assertEqual(result.output.count('tcp'), 2)
        self.assertEqual(result.output.count('udp'), 2)


if __name__ == '__main__':
    unittest.main()