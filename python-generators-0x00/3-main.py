#!/usr/bin/python3
"""
Test script for lazy pagination functionality.
"""
import sys
lazy_paginator = __import__('2-lazy_paginate').lazy_pagination


try:
    for page in lazy_paginator(100):
        for user in page:
            print(user)

except BrokenPipeError:
    sys.stderr.close()
