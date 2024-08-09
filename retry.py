import time
from random import randint
from functools import wraps


def retry_on_exception(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"重试第 {attempt + 1} 次失败，错误：{e}，等待 {delay} 秒后重试...")
                    time.sleep(delay)
            raise Exception(f"达到最大重试次数 {max_retries}，最后错误: {last_exception}")

        return wrapper

    return decorator


def retry(func, max_retries=3, delay=1):
    last_exception = None
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            last_exception = e
            print(f"重试第 {attempt + 1} 次失败，错误：{e}，等待 {delay} 秒后重试...")
            time.sleep(delay)
    raise Exception(f"自动重试达到最大次数：{max_retries}\n错误信息：{last_exception}")

# retry_autodailyattendance


def retry_autodailyattendance(retries=3, delay=1, backoff=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (SystemExit, KeyboardInterrupt):
                    raise
                except Exception as e:
                    if attempt + 1 == retries:
                        raise e
                    time.sleep(current_delay + randint(0, 3))
                    current_delay *= backoff
        return wrapper
    return decorator
