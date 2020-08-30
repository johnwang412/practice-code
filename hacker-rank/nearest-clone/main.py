#!/usr/bin/env python3

import math
import os
import random
import re
import sys

# Complete the findShortest function below.

#
# For the weighted graph, <name>:
#
# 1. The number of nodes is <name>_nodes.
# 2. The number of edges is <name>_edges.
# 3. An edge exists between <name>_from[i] to <name>_to[i].
#
#


class GraphWalker:
    def __init__(self, root_node_ids: set(), graph_from: list, graph_to: list):
        self.node_map = {}
        list(map(self._add_root, root_node_ids))
        self.nmap = _gen_neighbors_map(graph_from, graph_to)

    def add_seen(self, root_id: int, seen_node_id: int):
        if root_id not in self.node_map:
            self.node_map[root_id] = set()
        self.node_map[root_id].add(seen_node_id)

    def set_next_children(self, root_nid: int) -> set:
        """
        find next set of children from current children (or root node id if no current children)
          - exclude any nodes already seen
          - set children found on child_node_ids property
        """
        next_children = set()
        
        current_children_nids = self.node_map[root_nid]['child_node_ids']
        if current_children_nids is None:
            current_children_nids = {root_nid}

        # find all children
        # if children not in seen ids, then add to seen ids and add to next_children
        for nid in current_children_nids:
            next_children = next_children.union(self.nmap[nid])
                    
        seen_nids = self.node_map[root_nid]['node_ids_seen']
        next_children = next_children.difference(seen_nids)
        seen_nids = seen_nids.union(next_children)

        self.node_map[root_nid]['node_ids_seen'] = seen_nids
        self.node_map[root_nid]['child_node_ids'] = next_children

        return next_children

    def _add_root(self, root_id: int):
        self.node_map[root_id] = {
            'node_ids_seen': {root_id},
            'child_node_ids': None,
        }

    def _get_child_nids(self, nid: int) -> set:
        return self.nmap[nid]


def _gen_neighbors_map(graph_from: list, graph_to: list):
    nmap = {}
    for idx in range(0, len(graph_from)):
        if graph_from[idx] not in nmap:
            nmap[graph_from[idx]] = set()
        if graph_to[idx] not in nmap:
            nmap[graph_to[idx]] = set()

        nmap[graph_from[idx]].add(graph_to[idx])
        nmap[graph_to[idx]].add(graph_from[idx])
    return nmap


def findShortest(
        num_graph_nodes: int, 
        graph_from: list, 
        graph_to: list, 
        ordered_node_colors: list, 
        color_id: int,
    ):
    """
    :param ordered_node_ids: colors for each node, ordered by node_id (first 
        color in list corresponds to 1st node)
    """
    # solve here


    """
    For each node with color X, do breadth first search until same color is 
    found. Return distance when first color is encountered.

    todo: 
    - how to detect cycles: for each starting node, keep set of nodes seen
    """

    # add root nodes
    root_node_ids = set()
    for idx in range(0, len(ordered_node_colors)):
        if ordered_node_colors[idx] == color_id:
            node_id = idx + 1
            root_node_ids.add(node_id)

    gw = GraphWalker(root_node_ids, graph_from, graph_to)

    potential_len = 1
    complete = False

    while not complete:
        # for each root node, get next set of children (excluding those 
        #   already seen)
        # for each child, if it has the same color, then we're done, exit
       
        found_more_children = False

        for root_id in root_node_ids:

            child_node_ids = gw.set_next_children(root_id)
            if len(child_node_ids) > 0:
                found_more_children = True

            # check if any children match the color
            for c_nid in child_node_ids:
                if c_nid in root_node_ids:
                    return potential_len

        if not found_more_children:
            complete = True
            
        potential_len += 1

    return -1


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    graph_nodes, graph_edges = map(int, input().split())

    graph_from = [0] * graph_edges
    graph_to = [0] * graph_edges

    for i in range(graph_edges):
        graph_from[i], graph_to[i] = map(int, input().split())

    ids = list(map(int, input().rstrip().split()))

    val = int(input())

    ans = findShortest(graph_nodes, graph_from, graph_to, ids, val)

    fptr.write(str(ans) + '\n')

    fptr.close()

