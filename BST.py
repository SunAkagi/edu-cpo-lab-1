from typing import Optional, Callable, TypeVar, Generic, Tuple, List
from typing import Protocol, Any, cast
from functools import reduce as functools_reduce


class SupportsLessThan(Protocol):
    def __lt__(self, other: Any) -> bool: ...


KT = TypeVar("KT", bound=SupportsLessThan)
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

    def _insert(
        self,
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

    def _search(
        self,
        node: Optional[KVTreeNode[KT, VT]],
        key: KT
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
        def traverse(
            node: Optional[KVTreeNode[KT, VT]]
        ) -> List[Tuple[KT, VT]]:
            if node is None:
                return []
            return (
                traverse(node.left)
                + [(node.key, node.value)]
                + traverse(node.right)
            )
        return traverse(self.root)

    def reduce(
        self,
        func: Callable[[S, Tuple[KT, VT]], S],
        initializer: Optional[S] = None
    ) -> Optional[S]:
        items = self.inorder()
        if not items:
            return initializer
        if initializer is not None:
            return functools_reduce(func, items, initializer)
        else:
            acc = cast(S, items[0])
            return functools_reduce(func, items[1:], acc)

    def map(
        self,
        func: Callable[[Tuple[KT, VT]], Tuple[KT, VT]]
    ) -> None:
        items = self.inorder()
        self.root = None
        for k, v in map(func, items):
            self.insert(k, v)

    def filter(self, predicate: Callable[[Tuple[KT, VT]], bool]) -> None:
        items = [pair for pair in self.inorder() if predicate(pair)]
        self.root = None
        for k, v in items:
            self.insert(k, v)

    def concat(
        self,
        other: Optional['KVBinarySearchTree[KT, VT]'],
    ) -> Optional['KVBinarySearchTree[KT, VT]']:
        if self.is_empty():
            return other
        if other.is_empty():
            return self

        if self.root.key < other.root.key:
            self.root.right = self.concat_trees(self.root.right, other.root)
            return self
        elif self.root.key > other.root.key:
            other.root.right = self.concat_trees(self.root, other.root.right)
            return other
        else:
            self.root.left = self.concat_trees(self.root.left, other.root.left)
            self.root.right = self.concat_trees(
                self.root.right,
                other.root.right
            )
            return self

    def concat_trees(
        self,
        tree1: Optional[KVTreeNode[KT, VT]],
        tree2: Optional[KVTreeNode[KT, VT]]
    ) -> Optional[KVTreeNode[KT, VT]]:
        if tree1 is None:
            return tree2
        if tree2 is None:
            return tree1

        if tree1.key < tree2.key:
            tree1.right = self.concat_trees(tree1.right, tree2)
            return tree1
        elif tree1.key > tree2.key:
            tree2.right = self.concat_trees(tree1, tree2.right)
            return tree2
        else:
            tree2.left = self.concat_trees(tree1.left, tree2.left)
            tree2.right = self.concat_trees(tree1.right, tree2.right)
            return tree2

    def delete(self, key: KT) -> None:
        self.root = self._delete(self.root, key)

    def _delete(
        self,
        node: Optional[KVTreeNode[KT, VT]],
        key: KT
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

    def equals(self, other: 'KVBinarySearchTree[KT, VT]') -> bool:
        def are_nodes_equal(
            node1: Optional[KVTreeNode[KT, VT]],
            node2: Optional[KVTreeNode[KT, VT]]
        ) -> bool:
            if node1 is None and node2 is None:
                return True
            if node1 is None or node2 is None:
                return False
            return (
                node1.key == node2.key and
                node1.value == node2.value and
                are_nodes_equal(node1.left, node2.left) and
                are_nodes_equal(node1.right, node2.right)
            )
        return are_nodes_equal(self.root, other.root)
