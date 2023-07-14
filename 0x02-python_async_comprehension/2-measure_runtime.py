#!/usr/bin/env python3
"""
Module documentation: measure runtime
"""

import asyncio
from time import perf_counter

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    Coroutine that executes async_comprehension 4 times in parallel

    returns:
        float: Total runtime of executing async comprehension 
    """
    start_time = perf_counter()

    await asyncio.gather(*[async_comprehension() for _ in range(4)])

    end_time = perf_counter()

    return end_time - start_time
