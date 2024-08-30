import time
from random import randint
from functools import wraps


def retry(retries=3, delay=1, backoff=2, stop_exceptions=()):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (SystemExit, KeyboardInterrupt):
                    raise
                except stop_exceptions as e:
                    raise e
                except Exception as e:
                    if attempt + 1 == retries:
                        raise e
                    print(f"重试第 {attempt + 1} 次失败，错误：{e}，等待 {current_delay} 秒后重试...")
                    time.sleep(current_delay + randint(0, 3))
                    current_delay *= backoff
        return wrapper
    return decorator
