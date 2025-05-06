import random
from typing import Optional


class MaxHeap:
    def __init__(self):
        self.arr = []
        self.n = 0
    
    def __str__(self):
        return str(self.arr)
    
    def add(self, val: int):
        # Add item to left most leaf available
        if self.n >= len(self.arr):
            self.arr.append(val)
        else:
            self.arr[self.n] = val
        val_idx = self.n
        self.n += 1

        parent_idx = self._get_parent_idx(val_idx)
        while parent_idx != val_idx and self.arr[parent_idx] < self.arr[val_idx]:
            # swap values
            tmp = self.arr[parent_idx]
            self.arr[parent_idx] = self.arr[val_idx]
            self.arr[val_idx] = tmp

            val_idx = parent_idx
            parent_idx = self._get_parent_idx(val_idx)

    def len(self):
        return self.n

    def pop_max(self) -> Optional[int]:
        if self.n == 0:
            return None

        # save max val (root)
        max_val = self.arr[0]

        # move last node (random val) to root
        self.arr[0] = self.arr[self.n-1]
        self.n -= 1

        # move root to right position
        i = 0
        l = i * 2 + 1
        r = i * 2 + 2
        while l < self.n or r < self.n:
            # find max child
            max_idx = l
            if self.arr[r] > self.arr[l]:
                max_idx = r

            if self.arr[i] >= self.arr[max_idx]:
                break
            tmp = self.arr[i]
            self.arr[i] = self.arr[max_idx]
            self.arr[max_idx] = tmp

            i = max_idx
            l = i * 2 + 1
            r = i * 2 + 2
        
        return max_val


    def peak_max(self) -> Optional[int]:
        if self.n > 0:
            return self.arr[0]
        return None

    def _get_parent_idx(self, i: int):
        """
        param i: index we want the parent of
        """
        return i // 2


def main():
    heap = MaxHeap()

    nums = [random.randint(0,1000000) for i in range(10)]
    print(f'max of nums: {max(nums)}')
    t = nums.copy()
    t.sort()
    print(t)

    for n in nums:
        heap.add(n)
    
    print(f'heap max: {heap.peak_max()}')

    while heap.len() > 0:
        m = heap.pop_max()
        print(heap.peak_max())


if __name__ == '__main__':
    main()