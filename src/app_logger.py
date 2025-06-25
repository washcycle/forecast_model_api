import functools
import logging
import os


log_level = os.environ.get("LOG_LEVEL", "DEBUG").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.DEBUG))
logger = logging.getLogger()


# To make this more production ready, i'd recommend using a more sophisticated logging configuration that handles converting objects to JSON objects.
def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            logger.info(
                f"Function {func.__name__} executed successfully with args: {args}, kwargs: {kwargs}, result: {result}"
            )
            return result
        except Exception as e:
            logger.exception(
                f"Exception raised in {func.__name__}. exception: {str(e)}"
            )
            raise e

    return wrapper
