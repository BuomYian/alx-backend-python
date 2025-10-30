#!/usr/bin/python3
"""
ALX Backend Python - Python Generators Project
Test script for memory-efficient aggregation
"""

import importlib
stream_ages = importlib.import_module('4-stream_ages')
average_age = stream_ages.average_age


if __name__ == "__main__":
    avg = average_age()
    if avg is not None:
        print(f"Average age of users: {avg}")
    else:
        print("No users found in the database")
