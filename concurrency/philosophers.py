"""
Testing code from a LeetCode problem.
"""

import threading


class DiningPhilosophers:

    def __init__(self):
        self.table_lock = threading.Lock()

    # call the functions directly to execute, for example, eat()
    def wantsToEat(self,
                   philosopher: int,
                   pickLeftFork: 'Callable[[], None]',
                   pickRightFork: 'Callable[[], None]',
                   eat: 'Callable[[], None]',
                   putLeftFork: 'Callable[[], None]',
                   putRightFork: 'Callable[[], None]') -> None:

        """Dumb inefficient implementation"""
        with self.table_lock.acquire():
            pickLeftFork()
            pickRightFork()
        
            eat()

            putLeftFork()
            putRightFork()


def main():
    dp = DiningPhilosophers()
    # Simulate philosophers wanting to eat
    for i in range(5):
        dp.wantsToEat(i, lambda: print(f"Philosopher {i} picked left fork"),
                      lambda: print(f"Philosopher {i} picked right fork"),
                      lambda: print(f"Philosopher {i} is eating"),
                      lambda: print(f"Philosopher {i} put down left fork"),
                      lambda: print(f"Philosopher {i} put down right fork"))


if __name__ == "__main__":
    main()