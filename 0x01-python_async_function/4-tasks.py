#!/usr/bin/env python3

"""
Asynchronous routine that spawns task_wait_random n times
"""

import asyncio
from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    Asynchronous routine that spawns task_wait_random n times

    Args:
        n: The number of times to spawn task_wait_random.
        max_delay: The maximum delay in seconds for task_wait_random.

    Returns:
        A list of the delays (float values) in ascending order.
    """
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    results = await asyncio.gather(*tasks)
    return sorted(results)
