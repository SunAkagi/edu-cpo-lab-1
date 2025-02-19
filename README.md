# Kirov reporting！- lab 1 - variant 3 - Set based on binary tree

A binary search tree (BST), also called an ordered or sorted binary tree,
is a rooted binary tree data structure with the key of each internal node
being greater than all the keys in the respective node's left subtree and
less than the ones in its right subtree. The time complexity of operations
on the binary search tree is linear with respect to the height of the tree.

## Project structure

- `foo.py` -- implementation of `Foo` class and `add` features.
- `foo_test.py` -- unit and PBT tests for `Foo`.

## Implementation restrictions

- Unbalanced Tree -- Tree could be unbalanced, specially when the input is
sorted, which can significantly increase the time complexity. An AVL tree
or Red-Black tree, which automatically balances the tree after each insertion
or deletion.These balanced trees ensure that the operations remain O(log n)
even in the worst case. Also, a easy way to rebalance the tree is insert
nodes in a more randomized fashion, like using a Treap (a BST combined
with a heap).
- Iterative methods -- The current traversal methods use recursion, which
can be inefficient for large trees due to the risk of stack overflow. We
could optimize the traversal methods to be iterative using a stack or queue.
```python
def inorder_traversal(self):
    result = []
    stack = []
    current = self.root
    while stack or current:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        result.append(current.val)
        current = current.right
    return result
```
- Deletion Performance -- The current deletion approach for nodes with two
children involves finding the inorder successor and deleting it. One optimization
here could be to replace the current node’s value with the successor’s value, and
then delete the successor (which will never have both children). This simplifies
the logic slightly and can potentially make the tree easier to manage
```python
def delete(self, key):
    if self.root is None:
        raise ValueError(f"Tree is empty, cannot delete key {key}")
    
    parent = None
    current = self.root
    
    # Find the node to be deleted and its parent
    while current and current.val != key:
        parent = current
        if key < current.val:
            current = current.left
        else:
            current = current.right
    
    if current is None:
        raise ValueError(f"Key {key} not found in the tree.")
    
    # Case 1: Node to be deleted has no children (leaf node)
    if current.left is None and current.right is None:
        if parent is None:
            self.root = None  # Tree is now empty
        elif parent.left == current:
            parent.left = None
        else:
            parent.right = None
    # Case 2: Node to be deleted has one child
    elif current.left is None or current.right is None:
        child = current.left if current.left else current.right
        if parent is None:
            self.root = child  # If the root is being deleted
        elif parent.left == current:
            parent.left = child
        else:
            parent.right = child
    # Case 3: Node to be deleted has two children
    else:
        # Find the inorder successor (smallest node in the right subtree)
        successor_parent = current
        successor = current.right
        while successor.left:
            successor_parent = successor
            successor = successor.left
        
        # Copy the successor's value to the current node
        current.val = successor.val
        
        # Delete the successor (which will have at most one child)
        if successor_parent.left == successor:
            successor_parent.left = successor.right
        else:
            successor_parent.right = successor.right
```

## Contribution

- Sun Jiajian (sunakagi@163.com) -- .
- Yang Liang (2663048219@qq.com) -- .

## Advantages and disadvantages of unit test and PBT tests.

- ...
