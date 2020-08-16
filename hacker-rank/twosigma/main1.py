#!/bin/python

class Node:
    def __init__(self, idx):
        self.name = idx
        self.friends = []
        self.friend_names = []
        self.clic_name = None

    def befriend(self, fnode):
        if fnode.name not in self.friend_names:
            self.friends.append(fnode)
            self.friend_names.append(fnode.name)

    def establish_clic(self, clic_name=None):
        if self.clic_name is not None:
            # I'm already in a clic, I feel good about myself
            if clic_name is not None and self.clic_name != clic_name:
                print '***** did not expect that, trying to clic a friend already in another clic'
            return

        if clic_name is not None:
            # Someone asked me to join a clic, join
            self.clic_name = clic_name
        else:
            # Make myself a clic
            self.clic_name = self.name

        # Traverse friends tree and "color" all nodes with clic name
        for f in self.friends:
            f.establish_clic(self.clic_name)

    def get_friends(self):
        return self.friends


def friendCircles(friends):
    # Build a graph, color clusters of nodes with the same color (clic_name)
    #   and count disjoint clusters
    # Each node represents a kid
    # Each person's name is the row / column index ("0", "1", ...)
    # Clics that end up being created have names of the first kid who started
    #   the clic

    # Build nodes (kids)
    nodes_map = {}
    for idx, _ in enumerate(friends):
        nodes_map[idx] = Node(idx)

    # Build graph connections
    for r_idx, row in enumerate(friends):
        lonely_kid = nodes_map[r_idx]
        for c_idx, col in enumerate(row):
            if col == 'Y' and c_idx != r_idx:
                lonely_kid.befriend(nodes_map[c_idx])

    # Color groups
    for idx, node in nodes_map.iteritems():
        node.establish_clic()

    clics = {}
    # count number of distinct clics that exist
    for idx, node in nodes_map.iteritems():
        if node.clic_name not in clics:
            clics[node.clic_name] = 1

    return len(clics)


if __name__ == "__main__":

    friends_arr = [
        ['Y', 'Y', 'N', 'N'],
        ['Y', 'Y', 'Y', 'N'],
        ['N', 'Y', 'Y', 'N'],
        ['N', 'N', 'N', 'Y'],
    ]

    friendCircles(friends_arr)
