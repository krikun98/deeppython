import math
import multiprocessing
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path

test_func = math.cos
test_a = 0
test_b = math.pi/2


def integrate(f, a, b, *, n_iter=1000):
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def integrate_piece(f, a, i, step):
    return f(a + i*step) * step


def integrate_chunk(f, a, b, c, step):
    acc = 0
    for i in range(b, c):
        acc += integrate_piece(f, a, i, step)
    return acc


def integrate_par(f, a, b, *, executor, n_jobs=1, n_iter=10000):
    acc = 0
    step = (b - a) / n_iter
    b = 0
    b_step = int(n_iter/n_jobs)
    futures = []
    for i in range(n_jobs):
        futures.append(executor.submit(integrate_chunk, f, a, b, b+b_step, step))
        b += b_step
    for i in range(n_jobs):
        acc += futures[i].result()
    return acc


def bench_integrate(executor_type, n_jobs):
    with open("artifacts/medium_log.txt", "a") as logfile:
        print(f"Launching {executor_type} executor with {n_jobs} "
              f"{'threads' if executor_type == 'thread' else 'processes'} "
              f"at {time.perf_counter_ns()}", file=logfile)
    executor = ThreadPoolExecutor(n_jobs) if executor_type == "thread" else ProcessPoolExecutor(n_jobs)
    time_bef = time.perf_counter_ns()
    res = integrate_par(test_func, test_a, test_b, executor=executor)
    time_aft = time.perf_counter_ns()
    with open("artifacts/medium_log.txt", "a") as logfile:
        print(f"Finished {executor_type} executor with {n_jobs} "
              f"{'threads' if executor_type == 'thread' else 'processes'} "
              f"at {time.perf_counter_ns()}", file=logfile)
    return time_aft - time_bef


if __name__ == "__main__":
    Path("artifacts").mkdir(exist_ok=True)
    with open("artifacts/medium_log.txt", "w") as logfile:
        print(f"Starting at {time.perf_counter_ns()}", file=logfile)
    with open("artifacts/medium_res.txt", "w") as resfile:
        print(f"{'type':<10}{'jobs':<5}{'time':>20}", file=resfile)
        for type in ["thread", "process"]:
            for n in range(1, multiprocessing.cpu_count()*2+1):
                bench_time = bench_integrate(type, n)
                print(f"{type:<10}{n:<5}{bench_time:>20}", file=resfile)
