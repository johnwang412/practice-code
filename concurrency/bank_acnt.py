"""Simple bank account mutex example.

Run a bunch of concurrent threads moving money around two bank accounts.
Assert a the end that money is same as beginning.
"""


# TODO: Write a process that debits and credits an acnt from two data sources
# - Do we have to use 2PC?
# 

from dataclasses import dataclass
import random
import threading
import time


@dataclass
class BankAccount:
    name: str
    balance: int = None
    lock: threading.Lock = threading.Lock()


def move_money(john_acnt: BankAccount, tiff_acnt: BankAccount):
    acnts = [john_acnt, tiff_acnt]
    from_idx = random.choice([0, 1])
    to_idx = 1 - from_idx
    from_acnt = acnts[from_idx]
    to_acnt = acnts[to_idx]

    # take money
    with from_acnt.lock:
        if from_acnt.balance >= 5:
            time.sleep(0.001)
            from_acnt.balance -= 5
        else:
            return False

    # give money
    with to_acnt.lock:
        to_acnt.balance += 5
    
    return True


def main():
    """
    Start bank acnt at $20
    Create 50 threads, each thread checks if we can deduct $5 and does so
    Check if balance is positive
    """
    john_funds = 20
    tiff_funds = 30
    john_acnt = BankAccount(name='John', balance=john_funds)
    tiff_acnt = BankAccount(name='Tiff', balance=tiff_funds)

    print(f'Orig balance - john: {john_acnt.balance}, tiff: {tiff_acnt.balance}, total: {john_acnt.balance + tiff_acnt.balance}')

    threads = []
    for i in range(5000):
        t = threading.Thread(target=move_money, args=(john_acnt, tiff_acnt))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()

    print(f'Final balance - john: {john_acnt.balance}, tiff: {tiff_acnt.balance}, total: {john_acnt.balance + tiff_acnt.balance}')


if __name__ == "__main__":
    start_time = time.time()
    main()
    elapsed_time = (time.time() - start_time) * 1000
    print(f'Elapsed time: {elapsed_time:.2f} ms')