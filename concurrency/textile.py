"""
From ChatGPT

Problem: Multi-Stage Textile Factory Simulation
You are tasked with simulating a multi-stage textile factory using concurrency. The factory has three stages of processing:

Spinners - Spin raw cotton into thread.
Weavers - Weave thread into cloth.
Packagers - Fold and package the cloth.
The factory must obey the following constraints:

There are:
S Spinner threads
W Weaver threads
P Packager threads

A spinner produces one thread unit at a time.
A weaver consumes two thread units to produce one cloth unit.
A packager consumes one cloth unit to produce one package.

The simulation must run continuously, with each worker looping infinitely (or until a specified total number of packages is made, for testability).

Concurrency Constraints:
Semaphores must be used to manage access to shared buffers:
- A thread buffer (bounded buffer of max size T) for holding thread units.
- A cloth buffer (bounded buffer of max size C) for holding cloth units.
You must avoid:
- Race conditions (i.e., protect buffer accesses)
- Deadlocks
- Resource starvation
Workers should block if they can't continue their work (e.g., a weaver must block if there are fewer than two threads available).
Efficient use of threads — workers should not spin-wait.
"""

import random
import threading
import time


class ThreadBuffer:
    def __init__(self):
        self.buffer = []
        self.lock = threading.Lock()
        self.total_seen = {}

    def enqueue(self, thread_color: str):
        with self.lock:
            # Add item to buffer
            self.buffer.append(thread_color)
            if thread_color not in self.total_seen:
                self.total_seen[thread_color] = 0
            self.total_seen[thread_color] += 1
            print(f'Thread buffer total enqueued: {self.total_seen}')

    def try_dequeue(self) -> list:
        with self.lock:
            if len(self.buffer) > 1:
                print(f'Dequeuing threads from buffer of {len(self.buffer)} threads')
                return [self.buffer.pop(), self.buffer.pop()]
            return []

class ClothBuffer:
    def __init__(self):
        self.buffer = []
        self.lock = threading.Lock()

    def enqueue(self, cloth_color: str):
        with self.lock:
            # Add item to buffer
            self.buffer.append(cloth_color)

    def try_dequeue(self):
        with self.lock:
            if len(self.buffer) > 0:
                print(f'Dequeuing cloth from buffer of {len(self.buffer)} cloths')
                return [self.buffer.pop()]
            return []
        
class PackageBuffer:
    def __init__(self):
        self.buffer = []
        self.lock = threading.Lock()
    
    def enqueue(self, package_color: str):
        with self.lock:
            # Add item to buffer
            self.buffer.append(package_color)
            print(f'Package buffer total enqueued: {len(self.buffer)}')

class Spinner:
    def __init__(self, thread_buffer, color):
        self.thread_buffer = thread_buffer
        self.color = color
        self.max_threads = 10
        self.num_threads = 0

    def run(self, tb: ThreadBuffer):
        print(f'Starting up spinner!')
        while True:
            threads = self._produce_threads()
            if len(threads) > 0:
                for t in threads:
                    self.thread_buffer.enqueue(t)
            else:
                return
    
    def _produce_threads(self):
        if self.num_threads >= self.max_threads:
            print(f'Spinner is out of threads - shutting down')
            return []
        time.sleep(random.random()) # Simulate delay for thread production
        self.num_threads += 1
        return [self.color]

class Weaver:
    def __init__(self, thread_buffer, cloth_buffer):
        self.thread_buffer = thread_buffer
        self.cloth_buffer = cloth_buffer

    def run(self):
        print(f'Starting up weaver!')
        while True:
            threads = self.thread_buffer.try_dequeue()
            if len(threads) == 2:
                cloth_color: str = self._weave_cloth()
                self.cloth_buffer.enqueue(cloth_color=cloth_color)
            else:
                # Block until we have enough threads
                time.sleep(random.random())
    
    def _weave_cloth(self):
        cloth_color = random.choice(['red', 'blue', 'green'])
        time.sleep(random.random()*2) # Simulate delay for cloth production
        return cloth_color

class Packager:
    def __init__(self, cloth_buffer, package_buffer):
        self.cloth_buffer = cloth_buffer
        self.package_buffer = package_buffer

    def run(self):
        while True:
            cloth = self.cloth_buffer.try_dequeue()
            if len(cloth) == 1:
                self._package_cloth(cloth[0])
            else:
                # Block until we have enough cloth
                time.sleep(random.random())

    def _package_cloth(self, cloth_color):
        time.sleep(random.random()*3)
        self.package_buffer.enqueue(cloth_color)
        print(f'Packaged {cloth_color} cloth!')

def main():

    num_weavers = 2
    num_packagers = 4

    thread_buffer = ThreadBuffer()
    cloth_buffer = ClothBuffer()
    package_buffer = PackageBuffer()

    spinners = [
        Spinner(thread_buffer, 'red'),
        Spinner(thread_buffer, 'blue'),
        Spinner(thread_buffer, 'green'),
        Spinner(thread_buffer, 'yellow'),
    ]
    weavers = [Weaver(thread_buffer, cloth_buffer) for _ in range(num_weavers)]
    packagers = [Packager(cloth_buffer, package_buffer) for _ in range(num_packagers)]
    threads = []
    for spinner in spinners:
        t = threading.Thread(target=spinner.run, args=(thread_buffer,))
        threads.append(t)
        t.start()
    for weaver in weavers:
        t = threading.Thread(target=weaver.run)
        threads.append(t)
        t.start()
    for packager in packagers:
        t = threading.Thread(target=packager.run)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print('Simulation complete!')

if __name__ == "__main__":
    main()
