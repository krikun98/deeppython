import codecs
import multiprocessing as mp
import time
from time import sleep


def process_a(queue, pipe_in, active):
    while active.value:
        # print("a_cycle")
        if not queue.empty():
            pipe_in.send(queue.get_nowait().lower())
        sleep(5)
    pipe_in.send("")


def process_b(pipe_out, pipe_in, active):
    while active.value:
        # print("b_cycle")
        data = pipe_out.recv()
        pipe_in.send(codecs.encode(data, "rot13"))


if __name__ == "__main__":
    q = mp.Queue()
    from_a, to_b = mp.Pipe()
    from_b, to_main = mp.Pipe()
    active = mp.Value('i', True)
    a = mp.Process(target=process_a, args=(q, from_a, active, ))
    b = mp.Process(target=process_b, args=(to_b, from_b, active, ))
    a.start()
    b.start()
    while active.value:
        message = input(f"{time.perf_counter():<10} Input message: ")
        print(f"{time.perf_counter():<10} Input finished")
        if message == "exit":
            active.value = False
            break
        q.put(message)
        encoded = to_main.recv()
        print(f"{time.perf_counter():<10} Encoded message: {encoded}")
    a.join()
    b.join()

