# Complete the function below.

def longestChain(words):
    # Build hash map of words to speed up search
    #   If out of mem, can quicksort words and then binary search / etc..
    words_map = {}
    for w in words:
        words_map[w] = 1

    longest = 0
    for w, _ in words_map.iteritems():
        if len(w) <= longest:
            # can't possibly get a longer chain with a word of same length
            continue

        chain_len = find_chain_len(w, words_map)
        if chain_len > longest:
            longest = chain_len

    return longest


def find_chain_len(root_word, words):
    # len(w) <= 60 so probably don't need to worry about stack overflow for
    #   recursion
    if len(root_word) == 0:
        return 0
    if not root_word in words:
        return 0

    len_so_far = 1
    max_child_len = 0
    for i, _ in enumerate(root_word):
        child_word = root_word[:i] + root_word[i+1:]
        child_len = find_chain_len(child_word, words)
        if child_len > max_child_len:
            max_child_len = child_len
            if max_child_len == len(child_word):
                # we already found longest so stop search since we just
                # looking for longest count
                break

    return max_child_len + len_so_far


if __name__ == "__main__":

    words = [
        'a',
        'b',
        'ba',
        'bca',
        'bda',
        'bdca',
    ]

    print longestChain(words)
