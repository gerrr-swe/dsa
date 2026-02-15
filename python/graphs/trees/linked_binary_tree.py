from binary_tree import BinaryTree

class LinkedBinaryTree(BinaryTree):
    """Linked representation of a binary tree"""

    class _Node:
        """Lightweight nonpublic class for storign a node"""
        __slots__ = ["_parent", "_element", "_left", "_right"]

        def __init__(self, element, parent, left, right):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class Position(BinaryTree.Position):

        def __init__(self, container, node):
            """Should not be inkoked by user"""
            self._container = container # tree it belongs to
            self._node = node

        def element(self):
            return self._node._element

        def __eq__(self, other):
            return type(other) is type(self) and self._node is other._node

    def _validate(self,p):
        if not isinstance(p, self.position):
            raise TypeError("p must be proper position type")
        if p._container is not self:
            raise ValueError("p does not belong to this container")
        if p._node._parent is p._node:
            raise ValueError("p is no longer valid")
        return p._node

    def _make_position(self,node):
        return self.Position(self,node) if node is not None else None

    # constructor

    def __init__(self):
        self._root = None
        self._size = 0

    # public methods

    def __len__(self):
        return self._size

    def root(self):
        return self._make_position(self._root)

    def left(self, p):
        node = self._validate(p)
        return self._make_position(p._left)

    def right(self, p):
        node = self._validate(p)
        return self._make_position(p._right)
    
    def num_children(self, p):
        count = 0
        if p._left is not None:
            count += 1
        if p._right is not None:
            count += 1
        return count
    
    # no public update methods

    
