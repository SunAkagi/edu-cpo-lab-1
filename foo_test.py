import unittest
from hypothesis import given,  strategies as st
from foo import BinarySearchTree


class TestBinarySearchTree(unittest.TestCase):
    def setUp(self):
        self.bst = BinarySearchTree()
        self.test_values = [50, 30, 70, 20, 40, 60, 80]
        for value in self.test_values:
            self.bst.insert(value)

    def test_insert(self):
        # Insert a new value and check if it's present
        self.bst.insert(25)
        self.assertTrue(self.bst.search(25))

    def test_search(self):
        # Search for existing and non-existing values
        self.assertTrue(self.bst.search(30))
        self.assertFalse(self.bst.search(100))

    def test_delete(self):
        # Delete existing values and verify they are gone
        self.bst.delete(30)
        self.assertFalse(self.bst.search(30))

        # Ensure other nodes remain intact
        self.assertTrue(self.bst.search(20))
        self.assertTrue(self.bst.search(40))

    def test_min_max_value(self):
        # Check minimum and maximum values
        self.assertEqual(self.bst.minValue(), 20)
        self.assertEqual(self.bst.maxValue(), 80)

    def test_traversals(self):
        # Check traversal methods
        self.assertEqual(self.bst.inorder_traversal(),
                         [20, 30, 40, 50, 60, 70, 80])
        self.assertEqual(self.bst.preorder_traversal(),
                         [50, 30, 20, 40, 70, 60, 80])
        self.assertEqual(self.bst.postorder_traversal(),
                         [20, 40, 30, 60, 80, 70, 50])


class TestBSTProperties(unittest.TestCase):
    @given(st.lists(st.integers(), unique=True))
    def test_inorder_traversal_is_sorted(self, values):
        bst = BinarySearchTree()
        for value in values:
            bst.insert(value)
        self.assertEqual(sorted(values), bst.inorder_traversal())

    @given(st.lists(st.integers(), unique=True), st.integers())
    def test_search_after_insertion(self, values, key):
        bst = BinarySearchTree()
        for value in values:
            bst.insert(value)
        bst.insert(key)
        self.assertTrue(bst.search(key))

    @given(st.lists(st.integers(), unique=True), st.integers())
    def test_delete_and_search(self, values, key):
        bst = BinarySearchTree()
        for value in values:
            bst.insert(value)
        if key in values:
            bst.delete(key)
            self.assertFalse(bst.search(key))
        else:
            with self.assertRaises(ValueError):
                bst.delete(key)

    @given(st.lists(st.integers(), unique=True))
    def test_monoid_addition(self, values):
        bst = BinarySearchTree()
        for v in values:
            bst.insert(v)

        tree_sum = bst.reduce(lambda x, y: x + y, 0)

        self.assertEqual(tree_sum, sum(values))  
        self.assertEqual(bst.reduce(lambda x, y: x + y, 0), bst.reduce(lambda x, y: y + x, 0))

    @given(st.lists(st.integers(min_value=1, max_value=100), unique=True))
    def test_monoid_multiplication(self, values):
        bst = BinarySearchTree()
        for v in values:
            bst.insert(v)

        tree_product = bst.reduce(lambda x, y: x * y, 1)

        product = 1
        for v in values:
            product *= v

        self.assertEqual(tree_product, product)
