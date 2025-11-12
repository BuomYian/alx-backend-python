#!/usr/bin/env python3
"""Tests for client.GithubOrgClient class."""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
import requests
from unittest.mock import MagicMock

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

    @patch("client.GithubOrgClient._public_repos_url",
           new_callable=PropertyMock)
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json, mock_public_repos_url):
        """Test Tha public_repos returns the list of repository names.

        This test mocks both the get_json function and  the _public_repos_url
        to verify that public_repos returns the expected list of repository
        names.

        Args:
            mock_get_json (MagicMock): Mocked get_json function.
            mock_public_repos_url: Mocked _public_repos_url property.
        """
        test_repos_url = "https://api.github.com/orgs/google/repos"
        test_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo3", "license": None},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]

        mock_public_repos_url.return_value = test_repos_url
        mock_get_json.return_value = test_payload

        # Create client and call public_repos
        client = GithubOrgClient("google")
        result = client.public_repos()

        # Verify the results
        self.assertEqual(result, ["repo1", "repo3", "repo2"])
        mock_get_json.assert_called_once_with(test_repos_url)
        mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        (
            {"license": {"key": "my_license"}},
            "my_license",
            True,
        ),
        (
            {"license": {"key": "other_license"}},
            "my_license",
            False,
        ),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns the expected boolean value

        This test verifies the static method correctly checks if a repo
        has a specific license by comparing license keys.

        Args:
            repo: The repository dictionary with license info
            license_key: The license key to check for
            expected: The expected boolean return value
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


# Define fixtures for parameterized_class
TEST_PAYLOAD = [
    (
        {"repos_url": "https://api.github.com/orgs/google/repos"},
        [
            {
                "id": 7697149,
                "name": "episodes.dart",
                "license": {
                    "key": "bsd-3-clause",
                    "name": "BSD 3-Clause \"New\" or \"Revised\" License",
                    "spdx_id": "BSD-3-Clause",
                    "url": "https://api.github.com/licenses/bsd-3-clause",
                    "node_id": "MDc6TGljZW5zZTA="
                }
            },
            {
                "id": 7776515,
                "name": "cpp-netlib",
                "license": {
                    "key": "bsl-1.0",
                    "name": "Boost Software License 1.0",
                    "spdx_id": "BSL-1.0",
                    "url": "https://api.github.com/licenses/bsl-1.0",
                    "node_id": "MDc6TGljZW5zZTI4"
                }
            },
            {
                "id": 7968417,
                "name": "dagger",
                "license": {
                    "key": "apache-2.0",
                    "name": "Apache License 2.0",
                    "spdx_id": "Apache-2.0",
                    "url": "https://api.github.com/licenses/apache-2.0",
                    "node_id": "MDc6TGljZW5zZTI="
                }
            },
            {
                "id": 8165161,
                "name": "ios-webkit-debug-proxy",
                "license": {
                    "key": "other",
                    "name": "Other",
                    "spdx_id": "NOASSERTION",
                    "url": None,
                    "node_id": "MDc6TGljZW5zZTA="
                }
            },
            {
                "id": 8459994,
                "name": "google.github.io",
                "license": None
            },
            {
                "id": 8566972,
                "name": "kratu",
                "license": {
                    "key": "apache-2.0",
                    "name": "Apache License 2.0",
                    "spdx_id": "Apache-2.0",
                    "url": "https://api.github.com/licenses/apache-2.0",
                    "node_id": "MDc6TGljZW5zZTI="
                }
            },
            {
                "id": 8858648,
                "name": "build-debian-cloud",
                "license": {
                    "key": "other",
                    "name": "Other",
                    "spdx_id": "NOASSERTION",
                    "url": None,
                    "node_id": "MDc6TGljZW5zZTA="
                }
            },
            {
                "id": 9060347,
                "name": "traceur-compiler",
                "license": {
                    "key": "apache-2.0",
                    "name": "Apache License 2.0",
                    "spdx_id": "Apache-2.0",
                    "url": "https://api.github.com/licenses/apache-2.0",
                    "node_id": "MDc6TGljZW5zZTI="
                }
            },
            {
                "id": 9065917,
                "name": "firmata.py",
                "license": {
                    "key": "apache-2.0",
                    "name": "Apache License 2.0",
                    "spdx_id": "Apache-2.0",
                    "url": "https://api.github.com/licenses/apache-2.0",
                    "node_id": "MDc6TGljZW5zZTI="
                }
            }
        ],
        ['episodes.dart', 'cpp-netlib', 'dagger', 'ios-webkit-debug-proxy',
         'google.github.io', 'kratu', 'build-debian-cloud', 'traceur-compiler', 'firmata.py'],
        ['dagger', 'kratu', 'traceur-compiler', 'firmata.py'],
    )
]

org_payload = TEST_PAYLOAD[0][0]
repos_payload = TEST_PAYLOAD[0][1]
expected_repos = TEST_PAYLOAD[0][2]
apache2_repos = TEST_PAYLOAD[0][3]


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test cases for GithubOrgClient using fixtures"""

    @classmethod
    def setUpClass(cls):
        """Set up the test fixtures and mock requests.get

        This method patches requests.get to return mock responses
        based on the URL being requested, avoiding actual HTTP calls.
        """
        cls.get_patcher = patch("requests.get")
        mock_requests_get = cls.get_patcher.start()

        def side_effect_func(url, *args, **kwargs):
            """Return appropriate mock response based on URL"""
            mock_response = MagicMock()

            # Return org payload for org URL
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            # Return repos payload for repos URL
            elif url == cls.org_payload.get("repos_url"):
                mock_response.json.return_value = cls.repos_payload

            return mock_response

        mock_requests_get.side_effect = side_effect_func

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher after tests are complete

        This method stops the patch and cleans up the mock.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for GithubOrgClient.public_repos

        Verifies that public_repos returns the expected list of repositories
        when using real client methods (only mocking external HTTP calls).
        """
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test for GithubOrgClient.public_repos with license filter

        Verifies that public_repos with Apache 2.0 license filter
        returns only repos with Apache 2.0 license.
        """
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
