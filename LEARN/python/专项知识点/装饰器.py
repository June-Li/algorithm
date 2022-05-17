import time


def use_time(func):
    def wrapper(*args):
        start = time.time()
        result = func(*args)
        print('use time: ', time.time()-start)
        return result
    return wrapper


@use_time
def count_even(num):
    count = 0
    for i in range(num):
        if i % 2 == 0:
            count += 1
    return count


out = count_even(200000)
print(out)
