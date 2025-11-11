#!/usr/bin/env python3
"""Tests for client.GithubOrgClient class."""
import unittest
from unittest.mock import patch, PropertyMock
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

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns the correct URL.

        This test mocks the org property to return a known payload
        and verifies that _public_repos_url extracts the correct URL.

        Args:
            mock_org (PropertyMock): Mocked org property.
        """
        expected_repos_url = "https://api.github.com/orgs/google/repos"
        mock_org.return_value = {"repos_url": expected_repos_url}

        client = GithubOrgClient("google")
        self.assertEqual(
            client._public_repos_url, expected_repos_url)


if __name__ == "__main__":
    unittest.main()
