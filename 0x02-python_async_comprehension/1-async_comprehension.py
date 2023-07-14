#!/usr/bin/env python3
"""
Module documentation: Async comprehension
"""

from typing import List

async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """
    Coroutine that collects 10 random numbers using async

    returns:
        List[float]: List of 10 random numbers.
    """
    return [i async for i in async_generator()]
