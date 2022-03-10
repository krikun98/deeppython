from multiprocessing import Process
from pathlib import Path
from threading import Thread

from fib import fib_gen
from time import perf_counter_ns
from random import randint

val = 10000
repeat = 10


def bench_sync(large):
    results = []
    time_bef = perf_counter_ns()
    for i in range(repeat):
        results.append(fib_gen(large))
    time_aft = perf_counter_ns()
    return time_aft - time_bef


def bench_thread(large):
    threads = []
    result = 0
    for _ in range(repeat):
        threads.append(Thread(target=fib_gen, args=(large, )))
    time_bef = perf_counter_ns()
    for i in range(repeat):
        threads[i].start()
    for i in range(repeat):
        result = threads[i].join()
    time_aft = perf_counter_ns()
    return time_aft - time_bef


def bench_proc(large):
    processes = []
    for _ in range(repeat):
        processes.append(Process(target=fib_gen, args=(large, )))
    time_bef = perf_counter_ns()
    for i in range(repeat):
        processes[i].start()
    for i in range(repeat):
        processes[i].join()
    time_aft = perf_counter_ns()
    return time_aft - time_bef


if __name__ == "__main__":
    large = randint(val, val * 100)
    Path("artifacts").mkdir(exist_ok=True)
    with open("artifacts/easy.txt", "w") as file:
        print(f"Synchronous time in ns: {bench_sync(large)}", file=file)
        print(f"Thread time in ns: {bench_thread(large)}", file=file)
        print(f"Multiprocessing time in ns: {bench_proc(large)}", file=file)
