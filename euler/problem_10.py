# The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

# Find the sum of all the primes below two million.


def main():
  print 'find sum of all primes below 2M'

  primes_list = _get_primes_list2(2000000)

  print reduce(lambda x, y: x+y, primes_list) - 1

def _get_primes_list2(max_int):
  int_arr = []

  for counter in range(0, max_int + 1):
    int_arr.append(counter)

  for counter in range(2, max_int + 1):

    if int_arr[counter] == 0:
      # already a number that wasn't prime so skip
      continue

    # prime number, so use it to kill others
    test_num = counter
    multiple = 2
    test_num *= multiple
    while test_num <= max_int:
      int_arr[test_num] = 0
      multiple += 1
      test_num = counter * multiple

  return int_arr



if __name__ == '__main__':
  main()