#!/usr/bin/env python3

### IMPORTS ###
import logging
import xxhash

from typing import List

from .exceptions import TooFewCountsException, TooManyCountsException

### GLOBALS ###

### FUNCTIONS ###

### CLASSES ###
class CountingBloomFilter:
    """
    This is a counting bloom filter based on the article https://codeconfessions.substack.com/p/bloom-filters-and-beyond
    """
    def __init__(self, size: int = 4096, seeds: List[int] = None, ignore_errors: bool = False):
        self.logger = logging.getLogger(type(self).__name__)

        self.size: int = size
        self.seeds: List[int] = seeds if not None else [3, 5, 7]
        self.ignore_errors: bool = ignore_errors

        # ByteArray containing counters for Counting Bloom Filter
        # NOTE: This implementation is limited to 255 items per location.
        self.bit_vector = bytearray(([0] * self.size))

    def _hash(self, data: str, seed: int) -> int:
        hasher = xxhash.xxh64(seed = seed)
        hasher.update(data)
        result = hasher.intdigest()
        return result % self.size

    def add(self, item: str):
        for seed in self.seeds:
            index = self._hash(item, seed = seed)
            if self.bit_vector[index] >= 255:
                if not self.ignore_errors:
                    raise TooManyCountsException("Index {} already at 255 for item {}".format(index, item))
                self.logger.warning("Index %d already at 255 for item %s", index, item)
                continue
            self.bit_vector[index] += 1

    def remove(self, item: str):
        for seed in self.seeds:
            index = self._hash(item, seed = seed)
            if self.bit_vector[index] <= 0:
                if not self.ignore_errors:
                    raise TooFewCountsException("Index {} already at 0 for item {}".format(index, item))
                self.logger.warning("Index %d already at 0 for item %s", index, item)
                continue
            self.bit_vector[index] -= 1

    def query(self, item: str) -> bool:
        for seed in self.seeds:
            index = self._hash(item, seed = seed)
            if self.bit_vector[index] == 0:
                return False
        return True
