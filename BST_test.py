import unittest
from BST import KVBinarySearchTree
from hypothesis import given, strategies as st
from typing import List, Tuple


def build_tree_from_list(
  pairs: List[Tuple[int, str]]
) -> KVBinarySearchTree[int, str]:
    tree = KVBinarySearchTree.empty()
    for k, v in pairs:
        tree.insert(k, v)
    return tree


class TestKVBinarySearchTree(unittest.TestCase):
    def test_insert_and_search(self):
        tree = KVBinarySearchTree.empty()
        tree.insert(10, "a")
        tree.insert(5, "b")
        tree.insert(15, "c")
        self.assertEqual(tree.search(10), "a")
        self.assertEqual(tree.search(5), "b")
        self.assertEqual(tree.search(15), "c")
        self.assertIsNone(tree.search(100))

    def test_delete_leaf_and_root(self):
        tree = build_tree_from_list([(10, "a"), (5, "b"), (15, "c")])
        tree.delete(5)
        self.assertIsNone(tree.search(5))
        tree.delete(10)
        self.assertIsNone(tree.search(10))

    def test_map_and_filter(self):
        tree = build_tree_from_list([(1, "a"), (2, "b"), (3, "c")])
        tree.map(lambda kv: (kv[0] * 10, kv[1].upper()))
        inorder = tree.inorder()
        self.assertEqual(sorted(inorder), [(10, "A"), (20, "B"), (30, "C")])
        tree.filter(lambda kv: kv[0] != 20)
        inorder = tree.inorder()
        self.assertEqual(inorder, [(10, "A"), (30, "C")])

    def test_reduce(self):
        tree = build_tree_from_list([(1, "a"), (2, "b"), (3, "c")])
        result = tree.reduce(lambda acc, kv: acc + kv[1], "")
        self.assertEqual(set(result), {"a", "b", "c"})

    def test_empty_behavior(self):
        empty = KVBinarySearchTree.empty()
        self.assertTrue(empty.is_empty())
        self.assertEqual(empty.inorder(), [])
        self.assertIsNone(empty.search(1))
        self.assertEqual(empty.reduce(lambda acc, kv: acc + [kv], []), [])
        empty.map(lambda kv: (kv[0] * 2, kv[1]))
        self.assertEqual(empty.inorder(), [])

    def test_duplicate_key_overwrites_value(self):
        tree = KVBinarySearchTree.empty()
        tree.insert(10, "a")
        tree.insert(10, "b")
        self.assertEqual(tree.search(10), "b")

    def test_tree_depth(self):
        tree = build_tree_from_list(
            [(10, "a"), (5, "b"), (15, "c"), (12, "d")]
        )

        def max_depth(node):
            if node is None:
                return 0
            return 1 + max(max_depth(node.left), max_depth(node.right))
        self.assertLessEqual(max_depth(tree.root), 3)


@given(st.lists(st.tuples(st.integers(), st.text())))
def test_monoid_left_identity(items):
    tree = build_tree_from_list(items)
    identity = KVBinarySearchTree.empty()
    result = identity.concat(tree)
    assert result.inorder() == tree.inorder()


@given(st.lists(st.tuples(st.integers(), st.text())))
def test_monoid_right_identity(items):
    tree = build_tree_from_list(items)
    identity = KVBinarySearchTree.empty()
    result = tree.concat(identity)
    assert result.inorder() == tree.inorder()


@given(
    st.lists(st.tuples(st.integers(), st.text())),
    st.lists(st.tuples(st.integers(), st.text())),
    st.lists(st.tuples(st.integers(), st.text()))
)
def test_monoid_associativity(xs, ys, zs):
    t1 = build_tree_from_list(xs)
    t2 = build_tree_from_list(ys)
    t3 = build_tree_from_list(zs)
    left = t1.concat(t2).concat(t3)
    right = t1.concat(t2.concat(t3))
    assert sorted(left.inorder()) == sorted(right.inorder())


@given(st.lists(st.tuples(st.integers(), st.text())))
def test_insert_then_search(items):
    tree = build_tree_from_list(items)

    expected = {}
    for k, v in items:
        expected[k] = v

    for k, v in expected.items():
        assert tree.search(k) == v


@given(st.lists(st.tuples(st.integers(), st.text())))
def test_filter_keeps_only_matching(items):
    tree = build_tree_from_list(items)
    tree.filter(lambda kv: kv[0] % 2 == 0)
    for k, _ in tree.inorder():
        assert k % 2 == 0


@given(st.lists(st.tuples(st.integers(), st.text())))
def test_map_preserves_size(items):
    tree = build_tree_from_list(items)
    original_size = len(tree.inorder())
    tree.map(lambda kv: (kv[0] * 10, kv[1].upper()))
    assert len(tree.inorder()) == original_size
