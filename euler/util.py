def get_primes_list(max_int):
  """Returns list of prime numbers up to max_int

  Uses simple sieve, uses max_int space
  """
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

  return filter(lambda x: not x == 0 and not x == 1, int_arr)
