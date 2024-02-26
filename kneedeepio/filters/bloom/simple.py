#!/usr/bin/env python3

### IMPORTS ###
import logging
import xxhash

from typing import List

### GLOBALS ###

### FUNCTIONS ###

### CLASSES ###
class SimpleBloomFilter:
    """
    This is a simple bloom filter based on the article https://codeconfessions.substack.com/p/bloom-filters-and-beyond
    """
    def __init__(self, size: int = 4096, seeds: List[int] = None):
        self.logger = logging.getLogger(type(self).__name__)

        self.size: int = size
        self.seeds: List[int] = seeds if not None else [3, 5, 7]

        # ByteArray containing Bits for Bloom Filter
        num_bytes: int = (size + 7) // 8
        self.bit_vector = bytearray(([0] * num_bytes))

    def _hash(self, data: str, seed: int) -> int:
        hasher = xxhash.xxh64(seed = seed)
        hasher.update(data)
        result = hasher.intdigest()
        return result % self.size

    def add(self, item: str):
        for seed in self.seeds:
            index = self._hash(item, seed = seed)
            byte_index, bit_index = divmod(index, 8)
            mask = 1 << bit_index
            self.bit_vector[byte_index] |= mask

    def query(self, item: str) -> bool:
        for seed in self.seeds:
            index = self._hash(item, seed = seed)
            byte_index, bit_index = divmod(index, 8)
            mask = 1 << bit_index
            if (self.bit_vector[byte_index] & mask) == 0:
                return False
        return True
