import random

FILE_NAME = 'stream.csv'
UPPER_BOUND = 10_000


def make_stream():
    with open(FILE_NAME, 'w+') as f:

        # Random bits for beginning of stream
        for _ in range(random.randint(0, UPPER_BOUND)):
            f.write(f'{random.randint(0, 1)},')

        # Simple pattern appended random number of times to simulate infinity
        pattern = '0110'  # haha jeep
        pattern = ','.join(pattern)
        for _ in range(random.randint(0, UPPER_BOUND)):
            f.write(pattern + ',')

        f.write(pattern)
