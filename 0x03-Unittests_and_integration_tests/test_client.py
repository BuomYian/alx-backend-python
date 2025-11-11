#!/usr/bin/env python3
"""Tests for client.GithubOrgClient class."""
import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient."""
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the expected value.

        Args:
            org_name (str): The organization name to test.
            mock_get_json (MagicMock): Mocked get_json function.
        """
        expected_org = {"login": org_name, "id": 1234}
        mock_get_json.return_value = expected_org

        # Create client and call org property
        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_org)


if __name__ == "__main__":
    unittest.main()
