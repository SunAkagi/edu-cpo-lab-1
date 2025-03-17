from typing import Callable, TypeVar, Generic, Optional, Union
from functools import reduce

T = TypeVar('T')
R = TypeVar('R')
S = TypeVar("S")


class TreeNode(Generic[T]):
    def __init__(self, key: T):
        self.left: Optional['TreeNode[T]'] = None
        self.right: Optional['TreeNode[T]'] = None
        self.val: T = key


class BinarySearchTree(Generic[T]):
    def __init__(self):
        self.root: Optional[TreeNode[T]] = None

    def insert(self, key):
        if self.search(key):
            return
        if self.root is None:
            self.root = TreeNode(key)
        else:
            self._insert(self.root, key)

    def _insert(self, root, key):
        if key < root.val:
            if root.left is None:
                root.left = TreeNode(key)
            else:
                self._insert(root.left, key)
        elif key > root.val:
            if root.right is None:
                root.right = TreeNode(key)
            else:
                self._insert(root.right, key)

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, root, key):
        if root is None or root.val == key:
            return root
        if key < root.val:
            return self._search(root.left, key)
        return self._search(root.right, key)

    def delete(self, key):
        if self.root is None:
            raise ValueError(f"Tree is empty, cannot delete key {key}")
        if not self.search(key):
            raise ValueError(f"Key {key} not found in the tree.")
        self.root = self._delete(self.root, key)

    def _delete(self, root, key):
        if root is None:
            return root

        if key < root.val:
            root.left = self._delete(root.left, key)
        elif key > root.val:
            root.right = self._delete(root.right, key)
        else:
            # Node with only one child or no child
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            root.val = self._minValueNode(root.right).val
            # Delete the inorder successor
            root.right = self._delete(root.right, root.val)

        return root

    def _minValueNode(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def minValue(self):
        if self.root is None:
            return None
        current = self.root
        while current.left is not None:
            current = current.left
        return current.val

    def maxValue(self):
        if self.root is None:
            return None
        current = self.root
        while current.right is not None:
            current = current.right
        return current.val

    def inorder_traversal(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, root, result):
        if root:
            self._inorder(root.left, result)
            result.append(root.val)
            self._inorder(root.right, result)

    def preorder_traversal(self):
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, root, result):
        if root:
            result.append(root.val)
            self._preorder(root.left, result)
            self._preorder(root.right, result)

    def postorder_traversal(self):
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, root, result):
        if root:
            self._postorder(root.left, result)
            self._postorder(root.right, result)
            result.append(root.val)

    def map(self, func: Callable[[T], R]) -> 'BinarySearchTree[R]':
        new_tree: BinarySearchTree[R] = BinarySearchTree()
        for value in self.inorder_traversal():
            new_tree.insert(func(value))
        return new_tree

    def filter(self, predicate: Callable[[T], bool]) -> 'BinarySearchTree[T]':
        new_tree = BinarySearchTree[T]()
        for value in self.inorder_traversal():
            if predicate(value):
                new_tree.insert(value)
        return new_tree

    def reduce(self, func: Callable[[Union[S, None], T], S],
               initializer: Optional[S] = None) -> Optional[S]:
        values = self.inorder_traversal()
        if not values:
            return initializer
        return reduce(func, values, initializer)
