# The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases by 3330, is unusual in two ways: (i) each of the three terms are prime, and, (ii) each of the 4-digit numbers are permutations of one another.

# There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting this property, but there is one other 4-digit increasing sequence.

# What 12-digit number do you form by concatenating the three terms in this sequence?




def main():

  primes_list = _get_primes_list2(10000)
  four_dig_primes = filter(lambda x: x >= 1000 and not x == 0, primes_list)

  primes_strs = map(lambda x: str(x), four_dig_primes)

  processed = map(_sort, primes_strs)

  processed = sorted(processed, lambda x,y: cmp(x[0], y[0]))

  pairs_dict = {}
  for pair in processed:
    value = []
    if pair[0] in pairs_dict:
      value = pairs_dict[pair[0]]
      value.append(pair)
    else:
      value = [pair]
    pairs_dict[pair[0]] = value

  new_dict = {}
  for key, value in pairs_dict.iteritems():
    if len(value) >= 3:
      new_dict[key] = value

  for key, value in new_dict.iteritems():
    numbers = []
    for tup in value:
      numbers.append(int(tup[1]))
    numbers.sort()
#    print numbers

    diff = numbers[1] - numbers[0]
    test = 2
    while test < len(numbers):
      if diff == numbers[test] - numbers[test-1]:
        print '----> YAY %d%d%d' % (numbers[test-2], numbers[test-1], numbers[test])
      else:
        diff = numbers[test] - numbers[test-1]
      test += 1


def _sort(num_str):
  char_list = list(num_str)
  char_list.sort()

  sorted_str = ''.join(char_list)
  return (sorted_str, num_str)



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