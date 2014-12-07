# Can you create a program to solve a word jumble? ( More info here. )
# The program should accept a string as input, and then return a list
# of words that can be created using the submitted letters. For
# example, on the input "dog", the program should return a set of
# words including "god", "do", and "go".

# Please implement the program in a language of your choice, but
# refrain from using any combinatorics helper modules or imports
# (e.g. itertools in Python). In order to verify your words, just
# download an English word list ( here are a few ). Then upload your
# program to GitHub or Gist, and send it back!
#

from optparse import OptionParser

class Dictionary:
  words = {}

  add_count = 0
  look_count = 0

  def add_word(self, word):
    self.look_count += 1
    if word in self.words:
      return
    self.words[word] = ''
    self.add_count += 1

  def contains_word(self, word):
    return word in self.words

def main():
  parser = OptionParser()
  parser.add_option('-f', '--file', dest='words_filename',
                    help='dictionary file to use',
                    default=None)
  parser.add_option('-w', '--word', dest='word',
                    help='word to jumble',
                    default=None)
  (options, args) = parser.parse_args()

  if not options.words_filename or not options.word:
    print 'No input specified - need words file and word to jumble'

  # init dictionary
  dictionary = Dictionary()

  # read input word into dict
  _process_words_dict(dictionary, options.words_filename)

  # jumble letters
  jumble_results = _jumble_word(options.word, dictionary)

  # create output
  for key in jumble_results:
    print key


def _process_words_dict(dictionary, filename):
  word_count = 0
  f = open(filename)
  for line in f:
    dictionary.add_word(line.strip())
    word_count += 1

  print '_process_words_dict() complete - # words: %d' % word_count


def _jumble_word(word, dictionary):
  words_found_dict = {}
  _jumble_helper(words_found_dict, [], list(word), dictionary)

  print 'words found: %d' % len(words_found_dict)

  return words_found_dict


def _jumble_helper(words_found_dict, letters_picked_list, letters_left_list,
    dictionary):

  if len(letters_left_list) == 0:
    return
  else:
    for index, letter in enumerate(letters_left_list):
      # add letter; if it's a word, add to words found
      new_letter_list = list(letters_picked_list)
      new_letter_list.append(letter)
      word = ''.join(new_letter_list)
      if dictionary.contains_word(word):
        words_found_dict[word] = ''

      letters_left_copy = list(letters_left_list)
      letters_left_copy.pop(index)

      # recursive call
      _jumble_helper(words_found_dict, new_letter_list, letters_left_copy,
        dictionary)


if __name__ == '__main__':
  main()