from abc import ABC, abstractmethod


class Tree(ABC):
    """Abstract base clase representing a tree"""

    class Position(ABC):
        """Abstraction that represents the location of a single element"""

        @abstractmethod
        def element(self):
            """Returns the element stored at this position"""
            raise NotImplementedError("Must be implemented by subclass")

        @abstractmethod
        def __eq__(self, other):
            """Return true if other position represent the same location"""
            raise NotImplementedError("Must be implemented by subclass")

        @abstractmethod
        def __ne__(self, other):
            """Returns true if other position doesn't represent the same location"""
            raise NotImplementedError("Must be implemented by subclass")

    @abstractmethod
    def root(self):
        """Returns the position representing the tree's root or None"""
        raise NotImplementedError("Must be implemented by subclass")

    @abstractmethod
    def parent(self, p):
        """Returns the position representing the p's parent or None"""
        raise NotImplementedError("Must be implemented by subclass")

    @abstractmethod
    def num_children(self, p):
        """Returns the number of children that position p has"""
        raise NotImplementedError("Must be implemented by subclass")

    @abstractmethod
    def children(self, p):
        """Returns an iteration of positions of p's children"""
        raise NotImplementedError("Must be implemented by subclass")

    @abstractmethod
    def __len__(self):
        """Returns the total number of elements in a tree"""
        raise NotImplementedError("Must be implemented by subclass")

    @abstractmethod
    def position(self):
        """Returns an iteration of all tree positions"""
        raise NotImplementedError("Must be implemented by subclass")

    def is_root(self, p):
        """Returns true if the position p is the root position"""
        return self.root() == p

    def is_leaf(self, p):
        """Return true if position p does not have children"""
        return self.num_children(p) == 0

    def is_empty(self, p):
        """Return true if tree is empty"""
        return len(self) == 0

    def depth(self, p):
        """The number of levels separating position p from the root"""
        if self.is_root(p):
            return 0
        else:
            return self.depth(self.parent(p))+1

    def _height1(self):
        """Returns the height of the tree"""
        return max(self.depth(p) for p in self.position() if self.is_leaf(p))

    def _height2(self, p):
        """Return the height of the subtree rooted at position p"""
        if self.is_leaf(p):
            return 0
        else:
            return max( self._height2(q) for q in self.children(p) ) + 1
        
    def height(self, p):
        if p == None:
            return self._height2(self.root())
        else:
            return self._height2(p)
