#!/usr/bin/env python3
"""
Use mypy to validate the following piece of code and apply any necessary changes.
"""

from typing import Tuple, List


def zoom_array(lst: Tuple[int, ...], factor: int = 2) -> Tuple[int, ...]:
    """Zoom in the elements of a tuple by repeating them."""
    zoomed_in: List[int] = [
        item
        for item in lst
        for _ in range(factor)
    ]
    return tuple(zoomed_in)


array: Tuple[int, int, int] = (12, 72, 91)

zoom_2x: Tuple[int, int, int, int, int, int] = zoom_array(array)

zoom_3x: Tuple[int, int, int, int, int, int,
               int, int, int] = zoom_array(array, 3)
