#!/usr/bin/env python3

"""
Measures the total execution time for wait_n(n, max_delay)
"""

import time
from typing import Union
from asyncio import run
from time import perf_counter

wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    Measures the total execution time for wait_n(n, max_delay)

    Args:
        n: The number of times to call wait_n.
        max_delay: The maximum delay in seconds for wait_n.

    Returns:
        The average execution time per call in seconds as a float.
    """
    start_time = time.perf_counter()
    run(wait_n(n, max_delay))
    end_time = time.perf_counter()
    total_time = end_time - start_time
    return total_time / n
