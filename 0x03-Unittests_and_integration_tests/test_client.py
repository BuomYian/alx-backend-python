#!/usr/bin/env python3
"""A module for testing the client module.
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests the `test_org` function"""
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json', autospec=True)
    def test_org(self, org_name, mock_get_json):
        """Tests the `org` method."""
        # Create a GithubOrgClient instance
        client = GithubOrgClient(org_name)

        # Call the org method
        result = client.org()

        # Ensure that get_json is called once with the expected URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")

        # Ensure that get_json is not executed
        mock_get_json.return_value = None

        # Ensure that the result is correct
        self.assertEqual(result, mock_get_json.return_value)
