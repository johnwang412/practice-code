import dataclasses
from typing import Optional, Tuple


class QuadTree:

    @dataclasses.dataclass
    class qtCoord:
        x: int
        y: int
    
    @dataclasses.dataclass
    class qtItem:
        coord: 'QuadTree.qtCoord'
        item: object

    class qtNode:
        def __init__(self, item_limit: int, start: 'QuadTree.qtCoord', end: 'QuadTree.qtCoord'):
            self.item_limit = item_limit
            self.items: list[QuadTree.qtItem] = []
            """
            Option 2

            6,6 to 10,10
            """
            # Children order: [top_left, top_right, bottom_left, bottom_right]?
            self.children: list[QuadTree.qtNode] = []


        def insert(self, coord: 'QuadTree.qtCoord', item: object) -> bool:
            """
            :return: True if inserted, False if not inserted (should always return True for now 5/8/2025)
            """
            if not self._in_range(coord):
                print(f'Node - insert: coord {coord} not in range')
                return False

            if not self.children:
                if len(self.items) < self.item_limit:
                    self.items.append(QuadTree.qtItem(coord=coord, item=item))
                else:
                    # TODO: split and add items to resulting children
                    pass
            else:
                # TODO: calculate child item should go to
                pass

        def search(
                self, 
                start: 'QuadTree.qtCoord', 
                end: 'QuadTree.qtCoord', 
                center: 'QuadTree.qtCoord', 
                radius: int
                ) -> list['QuadTree.qtItem']:
            """
            start and end help traverse the quadtree whereas center and radius do the final
                distance filtering
            """
            items = []
            if not self.children():
                # go through items and see which ones are in the start / end coordinates
                pass
            else:
                # get child nodes we should search - for each child node, append the items
                pass

            return items
                

    def __init__(self, node_item_limit: int=4, limit_coord: Optional['QuadTree.qtCoord']=None):
        self._node_item_limit = node_item_limit
        self._limit_coord = limit_coord if limit_coord is not None else QuadTree.qtCoord(20, 20)
        # Root node covers the entire QuadTree area
        self.root_node = QuadTree.qtNode(self._node_item_limit, start_coord=QuadTree.qtCoord(0,0), end_coord=self._limit_coord)

    def _get_search_bounds(self, coord: 'QuadTree.qtCoord', radius: int):
        # TODO: implement
        pass

    def insert(self, coord: 'QuadTree.qtCoord', item: object) -> bool:
        """
        :return: True if inserted, False if not inserted (should always return True for now 5/8/2025)
        """
        return self.root_node.insert(coord, item)
    
    def search(self, center: 'QuadTree.qtCoord', radius: int) -> list[qtItem]:
        start, end = self._get_search_bounds(center, radius)
        return self.root_node.search(start, end, center, radius)


if __name__ == '__main__':

    qt = QuadTree()