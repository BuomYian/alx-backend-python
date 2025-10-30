#!/usr/bin/python3
"""
Test script for batch processing functionality
Demonstrates processing users in batches of 50 and filtering by age
"""

import sys
processing = __import__('1-batch_processing')

# Print processed users in a batch of 50
try:
    processing.batch_processing(50)
except BrokenPipeError:
    sys.stderr.close()
