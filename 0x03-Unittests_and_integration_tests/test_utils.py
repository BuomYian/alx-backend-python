#!/usr/bin/env python3
"""Unit tests for utils module using parameterized testing."""

import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized
from utils import memoize


def access_nested_map(nested_map, path):
    """Access nested map with key path.

    Parameters
    ----------
    nested_map: Mapping
        A nested map
    path: Sequence
        a sequence of key representing a path to the value

    Example
    -------
    >>> nested_map = {"a": {"b": {"c": 1}}}
    >>> access_nested_map(nested_map, ["a", "b", "c"])
    1
    """
    for key in path:
        if not isinstance(nested_map, dict):
            raise KeyError(key)
        nested_map = nested_map[key]
    return nested_map


def get_json(url):
    """Get JSON from remote URL.

    Parameters
    ----------
    url: str
        The URL to fetch JSON from
    returns
    -------
    dict
        The JSON response as a dictionary
    """
    import requests
    response = requests.get(url)
    return response.json()


class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map with parameterized inputs.

        Verify that access_nested_map returns the expected value for
        various nested dictionary structures and path sequences.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test access_nested_map raises KeyError for invalid paths.

        Verify that access_nested_map raises KeyError with the correct
        key when accessing non-existent keys or invalid paths.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{expected_key}'")


class TestGetJson(unittest.TestCase):
    """Test class for get_json function with mocked HTTP calls."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test get_json with mocked requests.get.

        Verify that get_json returns the expected payload when
        requests.get is mocked to return specific JSON data.
        """
        mock_get.return_value = MagicMock()
        mock_get.return_value.json.return_value = test_payload

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test class for memoize decorator."""

    def test_memoize(self):
        """Test that memoize decorator caches method results.

        Verify that when a memoized property is accessed multiple times,
        the underlying method is called only once due to caching.
        """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42):
            test_obj = TestClass()
            # Call the memoized property twice
            result1 = test_obj.a_property
            result2 = test_obj.a_property

            # Verify both calls return the correct result
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Verify that a_method was called only once
            test_obj.a_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
