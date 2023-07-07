#!/usr/bin/env python3

"""
This module provides a function to zoom in the elements of a tuple by repeating them.
"""

from typing import Tuple, List


def zoom_array(lst: Tuple[int, ...], factor: int = 2) -> Tuple[int, ...]:
    """
    Zoom in the elements of a tuple by repeating them.

    Args:
        lst (Tuple[int, ...]): The input tuple.
        factor (int, optional): The zoom factor. Defaults to 2.

    Returns:
        Tuple[int, ...]: The zoomed-in tuple.
    """
    zoomed_in: List[int] = [
        item
        for item in lst
        for _ in range(factor)
    ]
    return tuple(zoomed_in)
