#!/usr/bin/env python3

### IMPORTS ###
import logging
import unittest

from kneedeepio.filters.bloom import SimpleBloomFilter

### GLOBALS ###
# pylint: disable=C0301
TEST_DATA = [
    {
        "size": 256,
        "seeds": [3, 5, 7],
        "values": ['abc', 'def', 'foo', 'bar'],
        "bit_vector": bytearray.fromhex("0800 4000 0000 1040 0040 0000 0000 0001 0012 4100 0000 0000 0000 8008 0000 0000")
    },
    {
        "size": 217,
        "seeds": [9, 12, 15],
        "values": ['abcd', 'ghij', 'moo', 'cow'],
        "bit_vector": bytearray.fromhex("0200 2900 0000 0090 0004 0008 0000 0400 0000 8000 0000 0200 0000 0200")
    }
]

TEST_MISSING_VALUES = [
    "abcdefghijklmnopqrstuvwxyz",
    "superunknown"
]

### FUNCTIONS ###
def empty_bit_vector(size: int) -> bytearray:
    num_bytes = int(size / 8)
    if (size % 8) != 0:
        num_bytes += 1
    result = bytearray(([0] * num_bytes))
    return result

### CLASSES ###
class TestSimpleBloomFilter(unittest.TestCase):
    def setUp(self):
        # Setup logging for the class
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.debug("setUp")

    def test_add_to_filter(self):
        self.logger.debug("test_add_to_filter")
        for item in TEST_DATA:
            dut_simple = SimpleBloomFilter(size = item["size"], seeds = item["seeds"])
            self.assertEqual(dut_simple.bit_vector, empty_bit_vector(item["size"]))
            for value in item["values"]:
                dut_simple.add(value)
            self.logger.debug("DUT Bit Vector (size: %d): %s", item["size"], dut_simple.bit_vector.hex())
            self.logger.debug("DUT Bit Vector (expected): %s", item["bit_vector"].hex())
            self.assertEqual(dut_simple.bit_vector, item["bit_vector"])

    def test_query_filter_positive(self):
        self.logger.debug("test_query_filter_positive")
        for item in TEST_DATA:
            dut_simple = SimpleBloomFilter(size = item["size"], seeds = item["seeds"])
            for value in item["values"]:
                dut_simple.add(value)
            for value in item["values"]:
                self.logger.debug("Querying Value: %s", value)
                self.assertTrue(dut_simple.query(value))

    def test_query_filter_negative(self):
        self.logger.debug("test_query_filter_negative")
        for item in TEST_DATA:
            dut_simple = SimpleBloomFilter(size = item["size"], seeds = item["seeds"])
            for value in item["values"]:
                dut_simple.add(value)
            for value in TEST_MISSING_VALUES:
                self.logger.debug("Querying Value: %s", value)
                self.assertFalse(dut_simple.query(value))
