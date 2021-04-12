"""
方法一
"""


def main():
    def step(n, total, count):
        if count == n:
            total += 1
            return total
        elif count > n:
            return total
        count += 1
        total = step(n, total, count)
        count -= 1

        count += 2
        total = step(n, total, count)
        count -= 2
        return total

    n = 10
    total = 0
    count = 0
    total = step(n, total, count)
    print(total)


if __name__ == '__main__':
    main()

"""
方法二
"""
# 斐波那契数列
