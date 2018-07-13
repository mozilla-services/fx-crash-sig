from __future__ import print_function

import logging
import sys


def print_err(*args, **kwargs):
    log_format = '%(asctime)-15s - %(message)s'
    logging.basicConfig(filename='fx-crash-sig.log', format=log_format)
    logging.error(args[0])
    print(*args, file=sys.stderr, **kwargs)
