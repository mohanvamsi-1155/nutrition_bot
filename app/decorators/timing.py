import time
from functools import wraps
from app.helper.utils.logger import Logger
logger = Logger(name="timing_logger", level="INFO")


def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        logger.info(f"[{func.__name__}] executed in {end - start:.4f} seconds")
        return result

    return wrapper
