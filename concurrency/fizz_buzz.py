"""
Testing code from a LeetCode problem.
"""
import threading

class FizzBuzz:
    def __init__(self, n: int):
        self.n = n
        self.i = 0
        self.call_cnt = 0

        self.fizzlock = threading.Lock()
        self.buzzlock = threading.Lock()
        self.fizzbuzzlock = threading.Lock()
        self.nlock = threading.Lock()

        self.fizzlock.acquire()
        self.buzzlock.acquire()
        self.fizzbuzzlock.acquire()

    # printFizz() outputs "fizz"
    def fizz(self, printFizz: 'Callable[[], None]') -> None:
        while True:
            self.fizzlock.acquire()
            if self.i > self.n:
                break
            printFizz()
            self.call_cnt += 1
            self.nlock.release()

    # printBuzz() outputs "buzz"
    def buzz(self, printBuzz: 'Callable[[], None]') -> None:
        while True:
            self.buzzlock.acquire()
            if self.i > self.n:
                break
            printBuzz()
            self.call_cnt += 1
            self.nlock.release()

    # printFizzBuzz() outputs "fizzbuzz"
    def fizzbuzz(self, printFizzBuzz: 'Callable[[], None]') -> None:
        while True:
            self.fizzbuzzlock.acquire()
            if self.i > self.n:
                break
            printFizzBuzz()
            self.call_cnt += 1
            self.nlock.release()

    # printNumber(x) outputs "x", where x is an integer.
    def number(self, printNumber: 'Callable[[int], None]') -> None:
        while True:
            self.nlock.acquire()
            self.call_cnt += 1
            self.i += 1
            if self.i > self.n:
                self.fizzlock.release()
                self.buzzlock.release()
                self.fizzbuzzlock.release()
                self.nlock.release()
                break
            if self.i % 3 == 0 and self.i % 5 == 0:
                self.fizzbuzzlock.release()
            elif self.i % 3 == 0:
                self.fizzlock.release()
            elif self.i % 5 == 0:
                self.buzzlock.release()
            else:
                printNumber(self.i)
                self.nlock.release()
        

def main():
    fb = FizzBuzz(15)

    threads = [
        threading.Thread(target=fb.fizz, args=(lambda: print("fizz"),)),
        threading.Thread(target=fb.buzz, args=(lambda: print("buzz"),)),
        threading.Thread(target=fb.fizzbuzz, args=(lambda: print("fizzbuzz"),)),
        threading.Thread(target=fb.number, args=(lambda x: print(x),)),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(f'call count: {fb.call_cnt}')

if __name__ == "__main__":
    main()
