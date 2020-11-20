import random

FILE_NAME = 'stream.csv'
LOWER_BOUND = 100
UPPER_BOUND = 100_000


def make_stream():
    with open(FILE_NAME, 'w+') as f:

        # Random bits for beginning of stream
        for _ in range(random.randint(LOWER_BOUND, UPPER_BOUND)):
        # for _ in range(10):
            f.write(f'{random.randint(0, 1)},')

        # Simple pattern appended random number of times to simulate infinity
        pattern = '0110'  # haha jeep
        period = len(pattern)
        pattern = ','.join(pattern)
        for _ in range(UPPER_BOUND // period):
            f.write(pattern + ',')

        # write one more time so file does not end in comma
        f.write(pattern)


if __name__ == '__main__':
    make_stream()
