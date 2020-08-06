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

import pprint
from optparse import OptionParser

class Dictionary:
  # e.g.
  # children = {
  #   'a':{'is_word':True, children:{}}
  # }
  children = {}

  add_count = 0
  look_count = 0

  def add_word(self, word):
    children = self.children

    while len(word) > 0:
      is_last_letter = len(word) == 1
      current_letter = word[0]

      # see if contained in children
      self.look_count += 1
      if current_letter in children:
        if is_last_letter:
          children[current_letter]['is_word'] = True
      else:
        # if not contained in children, insert
        child_info = {
          'is_word': is_last_letter,
          'children': {}
        }
        children[current_letter] = child_info

        self.add_count += 1

      # move 1 level deeper in dictionary
      children = children[current_letter]['children']

      # trim first letter, and repeat
      word = word[1:]

  def contains_word(self, word):
    print 'contains_word(%s)' % word

    children = self.children

    while len(word) > 0:
      print '> ' + word[0]
      if word[0] in children:
        # move 1 level deeper in dictionary
        children = children[word[0]]['children']
        word = word[1:]
      else:
        return False

    return True

  def print_stats(self):
    print '=== Dictionary ==='
    print 'add count: %d' % self.add_count
    print 'look count: %d' % self.look_count

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

  # init base dictionary
  dictionary = Dictionary()

  # read input word into dict
  _process_words_dict(dictionary, options.words_filename)

  print 'done processing words'
  if dictionary.contains_word('car'):
    print 'is word'
  else:
    print 'is not word'

  dictionary.print_stats()

  # # jumble letters
  # jumble_results = _jumble_word(options.word, known_words_dict)

  # # create output
  # for key in jumble_results:
  #   print key


def _process_words_dict(dict_root, filename):

  word_count = 0
  f = open(filename)
  for line in f:
    dict_root.add_word(line.strip())

    # chars = list(line)

    # current_node = dict_root
    # letter_count = 0
    # for char in chars:
    #   if letter_count == len(chars) - 1:
    #     # last letter so is_word is true
    #     current_node = current_node.add_letter(char, True)
    #   else:
    #     current_node = current_node.add_letter(char, False)
    #   letter_count += 1

    word_count += 1

  print '_process_words_dict() complete - # words: %d' % word_count


def _jumble_word(word, known_words_dict):

  word_list = []

  _jumble_helper(word_list, '', list(word))

  # char_list = list(word)
  # max_int = 2 ** len(word)
  # print 'max_int: ' + str(max_int)

  # for bits in range(1, max_int):
  #   substr = _get_substr(bits, char_list)



  return {}


def _jumble_helper(word_list, word_so_far, remaining_letters_list):
  # check if word_so_far is a word

  print 'blah'



if __name__ == '__main__':
  main()