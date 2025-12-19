import pytest
from django.test import TestCase


class BasicTestCase(TestCase):
    def test_basic_truth(self):
        """
        Simple test to ensure the test framework is working.
        """
        self.assertTrue(True)
