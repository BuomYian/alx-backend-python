#!/usr/bin/env python3
"""Unit tests for utils module using the parameterized testing."""

import unittest
from parameterized import parameterized


def access_nested_map(nested_map, path):
    """Access nested map with key path.
    parameters
    ----------
    nested_map: Mapping
        A nested map
    path: Sequence
        a sequence of key representing a path to the value

    Example
    >>> nested_map = {"a": {"b": {"c": 1}}}
    >>> access_nested_map(nested_map, ["a", "b", "c"])
    1
    """
    for key in path:
        if not isinstance(nested_map, dict):
            raise KeyError(key)
        nested_map = nested_map[key]
    return nested_map


class TestAccessNestedMap(unittest.TestCase):
    """TestAccessNestedMap class to test access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ["a"], 1),
        ({"a": {"b": 2}}, ["a"], {"b": 2}),
        ({"a": {"b": 2}}, ["a", "b"], 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map function with valid inputs."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a"), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_nested_map_exception(self, nested_map, path, expected_key):
        """Test access_nested_map function with invalid inputs.

        Verify that KeyError is raised with the correct key.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(context.exception.args[0], expected_key)


if __name__ == "__main__":
    unittest.main()
