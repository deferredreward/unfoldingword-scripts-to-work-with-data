import multiprocessing
import time
from functools import partial


def cpu_bound(number, strongs):
    print(strongs)
    return sum(i * i for i in range(number))


def find_sums(numbers):
    with multiprocessing.Pool() as pool:
        snum = 'H0120'
        myfunction = partial(cpu_bound, strongs = snum)
        pool.map(myfunction, numbers)


if __name__ == "__main__":
    numbers = [5_000_000 + x for x in range(20)]

    start_time = time.time()    
    find_sums(numbers)
    duration = time.time() - start_time
    print(f"Duration {duration} seconds")