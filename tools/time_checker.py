import time


def checkTime(func, *args, **kwargs):
    start_time = time.time()
    population_seq = func(*args, **kwargs)
    end_time = time.time()
    sequence_time = end_time-start_time
    return population_seq, sequence_time

