#!/usr/bin/env python3

"""
Creates an asyncio Task that wraps the wait_random coroutine.
"""

import asyncio

wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """
    Creates an asyncio Task that wraps the wait_random coroutine.

    Args:
        max_delay: The maximum delay in seconds for wait_random.

    Returns:
        An asyncio Task object.
    """
    return asyncio.create_task(wait_random(max_delay))
