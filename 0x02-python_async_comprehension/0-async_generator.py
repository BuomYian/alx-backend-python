#!/usr/bin/env python3
"""
A coroutine that take no arguments
"""

import asyncio
import random
from typing import AsyncIterator


async def async_generator() -> AsyncIterator[float]:
    """
    Coroutine that generates random numbers asynchronously.
    Yields:
        float: Random number between 0 and 10.
    """
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
