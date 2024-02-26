#!/usr/bin/env python3

### IMPORTS ###
import glob
#import logging
import os
import sys
import unittest

### GLOBALS ###

### FUNCTIONS ###
def build_test_suites(test_glob):
    test_files = glob.glob(test_glob)
    suites = []
    for tmp_test_file in test_files:
        tmp_test_file_replace = tmp_test_file.replace('/', '.')
        tmp_test_file_replace = tmp_test_file_replace.replace('\\', '.')
        tmp_mod_str = "tests.{}".format(tmp_test_file_replace[0:len(tmp_test_file_replace) - 3])
        suites.append(unittest.defaultTestLoader.loadTestsFromName(tmp_mod_str))
    return suites

def run_all_tests():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    suites = []
    #suites.extend(build_test_suites("test_*.py"))
    suites.extend(build_test_suites("bloom/test_*.py"))
    test_suite = unittest.TestSuite(suites)
    # Run the test suite containing all the tests from all the modules
    test_runner = unittest.TextTestRunner()
    result = test_runner.run(test_suite)
    if result.wasSuccessful():
        return True
    return False

### CLASSES ###

### MAIN ###
if __name__ == '__main__':
    if run_all_tests() is False:
        sys.exit(1)
    sys.exit(0)
