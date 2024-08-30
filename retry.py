import time
from random import randint
from functools import wraps


def retry(retries=3, delay=1, backoff=2, stop_exceptions=()):
    """
    装饰器，用于对函数调用进行重试。

    参数:
    - retries: 最大重试次数。
    - delay: 初始重试延迟时间（秒）。
    - backoff: 每次重试时延迟时间的递增倍数。
    - stop_exceptions: 如果抛出这些异常，则停止重试。

    返回值:
    - 返回被装饰函数的结果。
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (SystemExit, KeyboardInterrupt):
                    # 如果捕获到系统退出或键盘中断异常，则重新抛出
                    raise
                except stop_exceptions as e:
                    # 如果捕获到指定的停止异常，则直接重新抛出
                    raise e
                except Exception as e:
                    # 如果是其他异常，进行重试
                    if attempt + 1 == retries:
                        # 如果达到最大重试次数，抛出异常
                        raise e
                    # 打印错误信息并进行延迟后重试
                    print(f"重试第 {attempt + 1} 次失败，错误：{e}，等待 {current_delay} 秒后重试...")
                    time.sleep(current_delay + randint(0, 3))  # 增加随机延迟
                    current_delay *= backoff  # 增加延迟时间

        return wrapper

    return decorator
