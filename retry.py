import time
from random import randint
from functools import wraps


def retry(retries=3, delay=1, backoff=2, stop_exceptions=()):
    """
    装饰器：用于对函数进行重试操作

    参数:
    retries (int): 最大重试次数，默认为 3 次
    delay (int): 初始延迟时间（秒），默认为 1 秒
    backoff (int): 延迟时间的增长因子，默认为 2（每次重试后延迟时间乘以此因子）
    stop_exceptions (tuple): 指定哪些异常会导致停止重试，默认为空元组（即不停止）

    返回:
    函数: 包含重试逻辑的包装函数
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(retries):
                try:
                    # 尝试调用被装饰的函数
                    return func(*args, **kwargs)
                except (SystemExit, KeyboardInterrupt):
                    # 如果捕获到 SystemExit 或 KeyboardInterrupt 异常，直接抛出
                    raise
                except stop_exceptions as e:
                    # 如果捕获到 stop_exceptions 中的异常，直接抛出
                    raise e
                except Exception as e:
                    # 捕获其他异常，执行重试逻辑
                    if attempt + 1 == retries:
                        # 如果已达到最大重试次数，抛出异常
                        raise e
                    print(f"重试第 {attempt + 1} 次失败，错误：{e}，等待 {current_delay} 秒后重试...")
                    # 等待一段时间后重试，增加随机性以避免过于频繁的重试
                    time.sleep(current_delay + randint(0, 3))
                    # 增加延迟时间
                    current_delay *= backoff
        return wrapper
    return decorator
