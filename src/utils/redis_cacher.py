import time
from functools import wraps

import redis


REDIS_CACHE = redis.Redis(host="localhost", port=6379, db=0)


def cache(function=None):
    @wraps(function)
    def wrapper(*args, **kwargs):
        num = args[0]

        val = REDIS_CACHE.get(str(num))

        if val:
            print("cached Value")
            return val
        else:

            _ = function(*args, **kwargs)
            REDIS_CACHE.set(str(num), str(_))
            return _

    return wrapper


@cache
def compute(num):
    num = num * num
    time.sleep(4)
    return num * num


def main():
    from timeit import default_timer as timer

    start = timer()
    val = compute(445)
    print(val)
    end = timer()
    print(end - start)

    start = timer()
    val = compute(445)
    print(val)
    end = timer()
    print(end - start)


if __name__ == "__main__":
    main()
