import unittest
from BST import KVBinarySearchTree, KVTreeNode
from hypothesis import given, strategies as st
from typing import List, Tuple
from typing import Optional


def build_tree_from_list(
  pairs: List[Tuple[int, str]]
) -> KVBinarySearchTree[int, str]:
    tree: KVBinarySearchTree[int, str] = KVBinarySearchTree.empty()
    for k, v in pairs:
        tree.insert(k, v)
    return tree


class TestKVBinarySearchTree(unittest.TestCase):
    def test_insert_and_search(self) -> None:
        tree: KVBinarySearchTree[int, str] = KVBinarySearchTree.empty()
        tree.insert(10, "a")
        tree.insert(5, "b")
        tree.insert(15, "c")
        self.assertEqual(tree.search(10), "a")
        self.assertEqual(tree.search(5), "b")
        self.assertEqual(tree.search(15), "c")
        self.assertIsNone(tree.search(100))

    def test_delete_leaf_and_root(self) -> None:
        tree: KVBinarySearchTree[int, str] = (
          build_tree_from_list([(10, "a"), (5, "b"), (15, "c")])
        )
        tree.delete(5)
        self.assertIsNone(tree.search(5))
        tree.delete(10)
        self.assertIsNone(tree.search(10))

    def test_map_and_filter(self) -> None:
        tree: KVBinarySearchTree[int, str] = (
          build_tree_from_list([(1, "a"), (2, "b"), (3, "c")])
        )
        tree.map(lambda kv: (kv[0] * 10, kv[1].upper()))
        inorder = tree.inorder()
        self.assertEqual(sorted(inorder), [(10, "A"), (20, "B"), (30, "C")])
        tree.filter(lambda kv: kv[0] != 20)
        inorder = tree.inorder()
        self.assertEqual(inorder, [(10, "A"), (30, "C")])

    def test_reduce(self) -> None:
        tree: KVBinarySearchTree[int, str] = (
          build_tree_from_list([(1, "a"), (2, "b"), (3, "c")])
        )
        result = tree.reduce(lambda acc, kv: acc + kv[1], "")
        self.assertEqual(set(filter(None, result or "")), {"a", "b", "c"})

    def test_empty_behavior(self) -> None:
        empty: KVBinarySearchTree[int, str] = KVBinarySearchTree.empty()
        self.assertTrue(empty.is_empty())
        self.assertEqual(empty.inorder(), [])
        self.assertIsNone(empty.search(1))
        self.assertEqual(empty.reduce(lambda acc, kv: acc + [kv], []), [])
        empty.map(lambda kv: (kv[0] * 2, kv[1]))
        self.assertEqual(empty.inorder(), [])

    def test_duplicate_key_overwrites_value(self) -> None:
        tree: KVBinarySearchTree[int, str] = KVBinarySearchTree.empty()
        tree.insert(10, "a")
        tree.insert(10, "b")
        self.assertEqual(tree.search(10), "b")

    def test_tree_depth(self) -> None:
        tree: KVBinarySearchTree[int, str] = build_tree_from_list(
            [(10, "a"), (5, "b"), (15, "c"), (12, "d")]
        )

        def max_depth(node: Optional[KVTreeNode[int, str]]) -> int:
            if node is None:
                return 0
            return 1 + max(max_depth(node.left), max_depth(node.right))
        self.assertLessEqual(max_depth(tree.root), 3)


@given(st.lists(st.tuples(st.integers(), st.text())))
def test_monoid_left_identity(items: List[Tuple[int, str]]) -> None:
    tree: KVBinarySearchTree[int, str] = build_tree_from_list(items)
    identity: KVBinarySearchTree[int, str] = KVBinarySearchTree.empty()
    result = identity.concat(tree)
    assert result.inorder() == tree.inorder()


@given(st.lists(st.tuples(st.integers(), st.text())))
def test_monoid_right_identity(items: List[Tuple[int, str]]) -> None:
    tree: KVBinarySearchTree[int, str] = build_tree_from_list(items)
    identity: KVBinarySearchTree[int, str] = KVBinarySearchTree.empty()
    result = tree.concat(identity)
    assert result.inorder() == tree.inorder()


@given(
    st.lists(st.tuples(st.integers(), st.text())),
    st.lists(st.tuples(st.integers(), st.text())),
    st.lists(st.tuples(st.integers(), st.text()))
)
def test_monoid_associativity(
    xs: List[Tuple[int, str]],
    ys: List[Tuple[int, str]],
    zs: List[Tuple[int, str]]
) -> None:
    t1 = build_tree_from_list(xs)
    t2 = build_tree_from_list(ys)
    t3 = build_tree_from_list(zs)

    t1_copy = build_tree_from_list(xs)
    t2_copy = build_tree_from_list(ys)
    t3_copy = build_tree_from_list(zs)

    left = t1.concat(t2).concat(t3)
    right = t1_copy.concat(t2_copy.concat(t3_copy))

    assert left = right


@given(st.lists(st.tuples(st.integers(), st.text())))
def test_insert_then_search(items: List[Tuple[int, str]]) -> None:
    tree: KVBinarySearchTree[int, str] = build_tree_from_list(items)

    expected = {}
    for k, v in items:
        expected[k] = v

    for k, v in expected.items():
        assert tree.search(k) == v


@given(st.lists(st.tuples(st.integers(), st.text())))
def test_filter_keeps_only_matching(items: List[Tuple[int, str]]) -> None:
    tree: KVBinarySearchTree[int, str] = build_tree_from_list(items)
    tree.filter(lambda kv: kv[0] % 2 == 0)
    for k, _ in tree.inorder():
        assert k % 2 == 0


@given(st.lists(st.tuples(st.integers(), st.text())))
def test_map_preserves_size(items: List[Tuple[int, str]]) -> None:
    tree: KVBinarySearchTree[int, str] = build_tree_from_list(items)
    original_size = len(tree.inorder())
    tree.map(lambda kv: (kv[0] * 10, kv[1].upper()))
    assert len(tree.inorder()) == original_size
