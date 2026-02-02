from tree import Tree
from typing import Optional

class BinaryTree(Tree):
    """Abstrac class representing the binary tree implementation"""

    def left(self, p) -> Optional[Tree.Position]:
        """Returns a position representing the left child of p or None"""
        raise NotImplementedError("Must be implemented by subclass")


    def right(self, p) -> Optional[Tree.Position]:
        """Returns a position representing the right child of p or None"""
        raise NotImplementedError("Must be implemented by subclass")
    
    def sibling(self, p) -> Optional[Tree.Position]:
        """Returns a position representing p's sibling or None"""
        parent = self.parent(p)

        if parent is None:
            return None
        else:
            if self.left(parent) == p:
                return self.right(parent)
            else:
                return self.left(parent)

    def children(self, p):
        """Generate an iteration of positions representing p children"""
        if self.left(p) is not None:
            yield self.left(p)
        if self.right is not None:
            yield self.right(p)