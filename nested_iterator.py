"""Iterator that flattens arbitrarily nested lists of integers."""

from __future__ import annotations

from collections.abc import Iterator
from typing import TypeAlias

NestedInt: TypeAlias = int | list["NestedInt"]


class NestedIterator(Iterator[int]):
    """Lazily iterate through nested integers in left-to-right order.

    Example:
        >>> data = [1, [2, [3, 4], 5], 6]
        >>> list(NestedIterator(data))
        [1, 2, 3, 4, 5, 6]
    """

    def __init__(self, nested: list[NestedInt]) -> None:
        # Store values in reverse order so pop() returns left-most elements first.
        self._stack: list[NestedInt] = list(reversed(nested))

    def __iter__(self) -> "NestedIterator":
        return self

    def __next__(self) -> int:
        while self._stack:
            current = self._stack.pop()
            if isinstance(current, int):
                return current

            # current is a nested list; reverse to preserve original traversal order.
            self._stack.extend(reversed(current))

        raise StopIteration
