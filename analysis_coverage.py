#!/usr/bin/env python3

### IMPORTS ###
import logging
import os
import sys
import coverage

### GLOBALS ###

### FUNCTIONS ###

### CLASSES ###

### MAIN ###
def main():
    logging.basicConfig(level = logging.DEBUG)

    base_path = os.path.dirname(os.path.abspath(__file__))
    source_paths = [
        os.path.join(base_path, 'kneedeepio/filters/bloom'),
        # Add libraries here
        os.path.join(base_path, 'tests')
    ]
    report_path = os.path.join(base_path, 'coverage_report')
    if not os.path.isdir(report_path):
        os.mkdir(report_path)

    cov = coverage.Coverage(source = source_paths)
    cov.start()

    # Ugly import is needed to get accurate test coverage reporting
    from tests import run_all_tests  # pylint: disable = wrong-import-position, import-outside-toplevel

    success = run_all_tests()

    cov.stop()

    cov.html_report(directory = report_path)

    logging.shutdown()

    if success is False:
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    main()
