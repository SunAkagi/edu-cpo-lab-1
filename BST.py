from typing import Optional, Callable, TypeVar, Generic, Tuple, List
from functools import reduce as functools_reduce

KT = TypeVar("KT")
VT = TypeVar("VT")
S = TypeVar("S")


class KVTreeNode(Generic[KT, VT]):
    def __init__(self, key: KT, value: VT,
                 left: Optional['KVTreeNode[KT, VT]'] = None,
                 right: Optional['KVTreeNode[KT, VT]'] = None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right


class KVBinarySearchTree(Generic[KT, VT]):
    def __init__(self, root: Optional[KVTreeNode[KT, VT]] = None):
        self.root = root

    @staticmethod
    def empty() -> 'KVBinarySearchTree[KT, VT]':
        return KVBinarySearchTree()

    def is_empty(self) -> bool:
        return self.root is None

    def insert(self, key: KT, value: VT) -> None:
        self.root = self._insert(self.root, key, value)

    def _insert(self,
                node: Optional[KVTreeNode[KT, VT]],
                key: KT,
                value: VT
    ) -> KVTreeNode[KT, VT]:
        if node is None:
            return KVTreeNode(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value
        return node

    def search(self, key: KT) -> Optional[VT]:
        return self._search(self.root, key)

    def _search(self, node: Optional[KVTreeNode[KT, VT]], key: KT
    ) -> Optional[VT]:
        if node is None:
            return None
        if key < node.key:
            return self._search(node.left, key)
        elif key > node.key:
            return self._search(node.right, key)
        else:
            return node.value

    def inorder(self) -> List[Tuple[KT, VT]]:
        def traverse(node: Optional[KVTreeNode[KT, VT]]
        ) -> List[Tuple[KT, VT]]:
            if node is None:
                return []
            return (
                traverse(node.left)
                + [(node.key, node.value)]
                + traverse(node.right)
            )
        return traverse(self.root)

    def reduce(self, func: Callable[[S, Tuple[KT, VT]], S],
               initializer: Optional[S] = None) -> Optional[S]:
        items = self.inorder()
        if not items:
            return initializer
        return (
            functools_reduce(func, items, initializer)
            if initializer is not None
            else functools_reduce(func, items)
        )

    def map(self, func: Callable[[Tuple[KT, VT]], Tuple[KT, VT]]) -> None:
        items = self.inorder()
        self.root = None
        for k, v in map(func, items):
            self.insert(k, v)

    def filter(self, predicate: Callable[[Tuple[KT, VT]], bool]) -> None:
        items = [pair for pair in self.inorder() if predicate(pair)]
        self.root = None
        for k, v in items:
            self.insert(k, v)

    def concat(self, other: 'KVBinarySearchTree[KT, VT]'
    ) -> 'KVBinarySearchTree[KT, VT]':
        result = KVBinarySearchTree(self.root)
        for k, v in other.inorder():
            result.insert(k, v)
        return result

    def delete(self, key: KT) -> None:
        self.root = self._delete(self.root, key)

    def _delete(self, node: Optional[KVTreeNode[KT, VT]], key: KT
    ) -> Optional[KVTreeNode[KT, VT]]:
        if node is None:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None and node.right is None:
                return None
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            min_node = self._min_value_node(node.right)
            node.key, node.value = min_node.key, min_node.value
            node.right = self._delete(node.right, min_node.key)
        return node

    def _min_value_node(self, node: KVTreeNode[KT, VT]) -> KVTreeNode[KT, VT]:
        current = node
        while current.left is not None:
            current = current.left
        return current
