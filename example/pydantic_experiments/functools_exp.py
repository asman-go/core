import functools


if __name__ == '__main__':
    items = [1, 2, 3, 4, 5]
    items = [1, 2]
    items = [1]

    print(functools.reduce(
        lambda x, y: x + y,
        items
    ))
