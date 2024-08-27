#!/usr/bin/env python3

### IMPORTS ###
import math

### GLOBALS ###

### FUNCTIONS ###
# Per the section of the article here: https://codeconfessions.substack.com/i/136634414/tuning-a-bloom-filter
def false_positive_rate(size: int, num_hashes: int, num_items: int) -> float:
    # Calculate the false positive rate of a bloom filter
    fp_rate = 1 - math.exp(-1 * math.pow(num_hashes * num_items / size, num_hashes))
    return fp_rate

def optimal_number_of_hashes(size: int, num_items: int) -> int:
    # Calculate the optimal number of hashes based on the size and number of items
    num_hashes = (size / num_items) * math.log(2)
    return int(num_hashes)

def optimal_size_of_filter(fp_rate: float, num_items: int) -> int:
    # Calculate the optimal size of a bloom filter
    bf_size = -1 * (num_items * math.log(fp_rate)) / (math.pow(math.log(2), 2))
    return int(bf_size)

### CLASSES ###
