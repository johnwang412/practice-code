#!/bin/python

import math
import sys

"""
    1b
   / \
  2r  5r
 /|   |\
3 4   6b 7r
      |
      8b

red (good, bad)
blue (good, bad)


1_n = (2n * 5n) * 2

1_n = (2ng + 2nb) * (5ng + 5nb) * 2

1_n = (2ng*5ng + 2ng*5nb + 2nb*5ng + 2nb*5nb) * 2

    -> only one product has all good configs
    -> of that product, 1/2^n


(c1ng * c2ng * ... * cnng) = n_good = number of combos of children subtrees that are good
- 2 * n_good = number of good combos including root
- case where root is r and roots of all child trees is b (and vice versa)
  - 2/n_c^2 * n_good = proportion of good child tree combos that have same color roots
  - (2/n_c^2 * n_good) * 2 = number good child configs that can become bad by having inverted root

TOTAL = 2 * (n_good) - 2 * (2/(n_c^2) * n_good)
  where n_good = (c1ng * c2ng ... * cnng)
"""
class Node:

    RED = 1
    BLUE = -1

    def __init__(self, node_num):
        self.key = str(node_num)
        self.children = []
    def add_child(self, child):
        found = False
        for c in self.children:
            if c.key == child.key:
                found = True
        if not found:
            self.children.append(child)
    def traverse(self, parent, fn):
        fn(self)
        for c in self.children:
            if parent and parent.key == c.key:
                continue
            c.traverse(self, fn)

    def is_leaf(self, parent):
        # all connected nodes also connect back to parent
        if parent and len(self.children) <= 1:
            return True
        if not parent and len(self.children) == 0:
            return True
        return False

    def count(self, parent):
        parent_node_cnt = 0
        if parent:
            parent_node_cnt = 1

        child_count = len(self.children) - parent_node_cnt
        # is single node leaf
        # - this case actually should not happen
        if child_count == 0:
            # If child is leaf, return 1 (for algo purposes - todo - list cases)
            # Basically, all leaf children have to be same color as root node
            # otherwise, they create an isolated attack case, so they might as
            # well be "absorbed" into the root node and not affect count
            return 1

        c_good_count_list = []
        num_leaves = 0
        for child in self.children:
            if parent and child.key == parent.key:
                continue
            if child.is_leaf(self):
                num_leaves += 1
                continue
            c_good_count_list.append(child.count(self))

        # print str(self.key) + ': ' + str(c_good_count_list)
        n_good = reduce(lambda carry, x: x*carry, c_good_count_list, 1)
        # if len(c_good_count_list) == 1:
        #     # in this case root only has single child, so has to be same color
        #     # as single child and we just return n_good
        #     return n_good

        if child_count == 1:
            # single connection []->[].. color has to match child root so just pass up
            # todo: this does not work
            return n_good
        else:
            total = 2 * n_good
            if not parent and num_leaves == 0:
                # take out condition where all countable child roots are same color
                total = int(total - (reduce(lambda carry, x: x/2 * carry, c_good_count_list, 1) * 2))

        return total

def build_map(roads, node_map):
    root = None

    # build map
    for road in roads:
        anode = node_map.get(str(road[0]))
        bnode = node_map.get(str(road[1]))
        if not anode:
            anode = Node(road[0])
        if not bnode:
            bnode = Node(road[1])
        if not root:
            root = anode
        anode.add_child(bnode)
        bnode.add_child(anode)
        node_map[str(road[0])] = anode
        node_map[str(road[1])] = bnode
    return root


def kingdomDivision(n, roads):
    node_map = {}
    root = build_map(roads, node_map)
    if root.is_leaf(None):
        return 2
    return int(root.count(None) % (math.pow(10,9) + 7))


if __name__ == "__main__":
    n = int(raw_input().strip())
    roads = []
    for roads_i in xrange(n-1):
        roads_temp = map(int,raw_input().strip().split(' '))
        roads.append(roads_temp)
    result = kingdomDivision(n, roads)
    print result

