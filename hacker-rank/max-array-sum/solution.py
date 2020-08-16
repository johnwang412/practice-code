import pdb
import typing


class SumMem:
    def __init__(self):
        self.sum_map = {}

    def _get_key(start_idx: int, end_idx: int) -> str:
        return f'{start_idx} - {end_idx}'

    def get(start_idx: int, end_idx: int) -> typing.Optional[int]:
        key = _get_key(start_idx, end_idx)
        self.sum_map.get(key, None)

    def set(start_idx: int, end_idx: int, max_sum: int):
        key = _get_key(start_idx, end_idx)
        self.sum_map[key] = max_sum


def max_subset_sum(input_arr: typing.List, mem: SumMem):
    
    # choose items
    # items cannot be adjacent

    # for each choice, iterate over sublist of choices
    # - sublist cannot include adjacent number
    # - either choose or not choose the next number

    # memoize --> how to represent a unique subset choice
    # - Option 1: 'binary string' as hash key with value as max subset sum
    #   - Limiting factor --> length of string 100K
    # - Option 2: start + end index of sub list as hash key
    #   - No scalability issues --> same effect

    # Requirements
    # - len(subset) >= 2

    """
    [3,7,4,6,5]
    
    [3, 4]

    """

    input_arr = [3,7,4,6,5,8,9]

    print(f'calc max subset sum for: {input_arr}')
    
    idx_start = 0

    while idx_start < len(input_arr): 

        set_size = 3
        subset = []
        idx = idx_start
        while set_size > 0 and idx < len(input_arr):
            subset.append(input_arr[idx])
            set_size -= 1
            idx += 2

        if len(subset) >= 2:
            print(f'subset: {subset}')

        idx_start += 1






def main():
    print(f'hello world')

    input_arr = [3,7,4,6,5]

    mem = SumMem()

    print(f'max subset sum: {max_subset_sum(input_arr, mem)}')


if __name__ == '__main__':
    main()

