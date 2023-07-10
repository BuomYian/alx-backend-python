#!/usr/bin/env python3
"""
asynchronous coroutine that takes in an integer argument
"""
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """
    Asynchronous coroutine that waits for a random delay

    Args:
        max_delay: The maximum delay in seconds (default: 10).

    Returns:
        The random delay as a float value.
    """
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
