#!/usr/bin/env python3

### IMPORTS ###

### GLOBALS ###

### FUNCTIONS ###

### CLASSES ###
class BloomFilterException(Exception):
    pass

class TooManyCountsException(BloomFilterException):
    pass

class TooFewCountsException(BloomFilterException):
    pass
