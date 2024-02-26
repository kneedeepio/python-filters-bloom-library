#!/usr/bin/env python3

### IMPORTS ###
import logging
import unittest

from kneedeepio.filters.bloom import CountingBloomFilter
from kneedeepio.filters.bloom import TooFewCountsException, TooManyCountsException

### GLOBALS ###
# pylint: disable=C0301
TEST_DATA = [
    {
        "size": 256,
        "seeds": [3, 5, 7],
        "values": ["abc", "def", "foo", "bar"],
        "byte_vector": bytearray.fromhex(
            "0000 0001 0000 0000 0000 0000 0000 0000 0000 0000 0000 0100 0000 0000 0000 0000"
            "0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0100 0000 0000 0000 0000 0100"
            "0000 0000 0000 0000 0000 0000 0000 0100 0000 0000 0000 0000 0000 0000 0000 0000"
            "0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0100 0000 0000 0000"
            "0000 0000 0000 0000 0001 0000 0100 0000 0100 0000 0000 0100 0000 0000 0000 0000"
            "0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000"
            "0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0001 0000 0001 0000 0000"
            "0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000"
        )
    },
    {
        "size": 217,
        "seeds": [9, 12, 15],
        "values": ["abcd", "ghij", "moo", "cow", "moo"],
        "byte_vector": bytearray.fromhex(
            "0001 0000 0000 0000 0000 0000 0000 0000 0100 0002 0001 0000 0000 0000 0000 0000"
            "0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0100 0001"
            "0000 0000 0000 0000 0000 0100 0000 0000 0000 0000 0000 0000 0000 0002 0000 0000"
            "0000 0000 0000 0000 0000 0000 0000 0000 0000 0200 0000 0000 0000 0000 0000 0000"
            "0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0001 0000 0000 0000 0000"
            "0000 0000 0000 0000 0000 0000 0000 0000 0001 0000 0000 0000 0000 0000 0000 0000"
            "0000 0000 0000 0000 0000 0000 0000 0000 0001 0000 0000 0000 00"
        )
    }
]

TEST_MISSING_VALUES = [
    "abcdefghijklmnopqrstuvwxyz",
    "superunknown"
]

### FUNCTIONS ###

### CLASSES ###
class TestSimpleBloomFilter(unittest.TestCase):
    def setUp(self):
        # Setup logging for the class
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.debug("setUp")

    def test_add_to_filter(self):
        self.logger.debug("test_add_to_filter")
        for item in TEST_DATA:
            dut_simple = CountingBloomFilter(size = item["size"], seeds = item["seeds"])
            self.assertEqual(dut_simple.bit_vector, bytearray(([0] * item["size"])))
            for value in item["values"]:
                dut_simple.add(value)
            self.logger.debug("DUT Byte Vector (size: %d): %s", item["size"], dut_simple.bit_vector.hex())
            self.logger.debug("DUT Byte Vector (expected): %s", item["byte_vector"].hex())
            self.assertEqual(dut_simple.bit_vector, item["byte_vector"])

    def test_query_filter_positive(self):
        self.logger.debug("test_query_filter_positive")
        for item in TEST_DATA:
            dut_simple = CountingBloomFilter(size = item["size"], seeds = item["seeds"])
            for value in item["values"]:
                dut_simple.add(value)
            for value in item["values"]:
                self.logger.debug("Querying Value: %s", value)
                self.assertTrue(dut_simple.query(value))

    def test_query_filter_negative(self):
        self.logger.debug("test_query_filter_negative")
        for item in TEST_DATA:
            dut_simple = CountingBloomFilter(size = item["size"], seeds = item["seeds"])
            for value in item["values"]:
                dut_simple.add(value)
            for value in TEST_MISSING_VALUES:
                self.logger.debug("Querying Value: %s", value)
                self.assertFalse(dut_simple.query(value))

    def test_remove_from_filter(self):
        self.logger.debug("test_remove_from_filter")
        for item in TEST_DATA:
            dut_simple = CountingBloomFilter(size = item["size"], seeds = item["seeds"])
            self.assertEqual(dut_simple.bit_vector, bytearray(([0] * item["size"])))
            for value in item["values"]:
                dut_simple.add(value)
            self.assertEqual(dut_simple.bit_vector, item["byte_vector"])
            for value in item["values"]:
                dut_simple.remove(value)
            self.assertEqual(dut_simple.bit_vector, bytearray(([0] * item["size"])))

    def test_add_too_many_exception(self):
        self.logger.debug("test_add_too_many_exception")
        for item in TEST_DATA:
            with self.assertRaises(TooManyCountsException):
                dut_simple = CountingBloomFilter(size = item["size"], seeds = item["seeds"])
                for _ in range(256):
                    dut_simple.add(item["values"][0])

    def test_add_too_many_ignore(self):
        self.logger.debug("test_add_too_many_ignore")
        for item in TEST_DATA:
            dut_simple = CountingBloomFilter(size = item["size"], seeds = item["seeds"], ignore_errors = True)
            for _ in range(256):
                dut_simple.add(item["values"][0])

    def test_remove_too_many_exception(self):
        self.logger.debug("test_remove_too_many_exception")
        for item in TEST_DATA:
            with self.assertRaises(TooFewCountsException):
                dut_simple = CountingBloomFilter(size = item["size"], seeds = item["seeds"])
                dut_simple.add(item["values"][0])
                dut_simple.remove(item["values"][0])
                dut_simple.remove(item["values"][0])

    def test_remove_too_many_ignore(self):
        self.logger.debug("test_remove_too_many_ignore")
        for item in TEST_DATA:
            dut_simple = CountingBloomFilter(size = item["size"], seeds = item["seeds"], ignore_errors = True)
            dut_simple.add(item["values"][0])
            dut_simple.remove(item["values"][0])
            dut_simple.remove(item["values"][0])
