#!/usr/bin/env python3
"""
Asynchronous routine that spawns wait_random n times
"""
import asyncio
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Asynchronous routine that spawns wait_random n times

    Args:
        n: The number of times to spawn wait_random.
        max_delay: The maximum delay in seconds for wait_random.

    Returns:
        A list of the delays (float values) in ascending order.
    """
    tasks = [wait_random(max_delay) for _ in range(n)]
    results = await asyncio.gather(*tasks)
    return sorted(results)
