import _thread
import signal
import threading
import time


class FunctionTimeoutError(Exception):
    pass


def timeout_handler(signum, frame):
    raise FunctionTimeoutError("Function execution timed out.")


def timeout_decorator2(timeout):
    def decorator(func):
        def wrapper(*args, **kwargs):
            timer = threading.Timer(timeout, lambda: _thread.interrupt_main())
            timer.start()
            try:
                result = func(*args, **kwargs)
            except KeyboardInterrupt:
                timer.cancel()
                raise TimeoutError("Function execution timed out.")
            else:
                timer.cancel()
                return result

        return wrapper

    return decorator


def timeout_decorator(timeout):
    def decorator(func):
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout)
            try:
                result = func(*args, **kwargs)
            except TimeoutError as e:
                print(e)
                result = None
            finally:
                signal.alarm(0)  # 取消闹钟
            return result

        return wrapper

    return decorator


@timeout_decorator(timeout=2)
def my_function():
    print("Starting function...")
    time.sleep(12)  # 休眠 12 秒，模拟长时间运行的函数
    print("Function completed.")
    return "Success"


if __name__ == "__main__":
    result = my_function()
    print("Result:", result)
