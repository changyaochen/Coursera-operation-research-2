"""Collection of decorators."""
import logging
import time
from functools import wraps


def timeit(function):
    """A decorator to measure the execution time of a function."""

    @wraps(function)
    def inner_function(*args, **kwargs):
        t_start = time.time()
        output = function(*args, **kwargs)
        t_end = time.time()
        logging.info(
            f"{function.__qualname__} took {(t_end - t_start) * 1000:.3f} ms to execute.")
        return output

    return inner_function
