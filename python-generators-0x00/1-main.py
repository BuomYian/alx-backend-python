#!/usr/bin/python3
"""
Test script to demonstrate the stream_users generator.
Prints the first 6 users from the database.
"""

from itertools import islice
stream_users = __import__('0-stream_users')

# Iterate over the generator function and print only the first 6 rows
for user in islice(stream_users.stream_users(), 6):
    print(user)
