import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def log_function_call(func):
    async def wrapper(*args, **kwargs):
        if args and kwargs:
            user = args[1].from_user
            logger.info(f"Calling function: {func.__name__}\n"
                        f"user: {user.id}\n"
                        f"args: {args}\n"
                        f"kwargs: {kwargs}")
        result = await func(*args, **kwargs)
        logger.info(f"Function {func.__name__} returned: {result}\n")
        return result
    return wrapper
