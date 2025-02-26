# Kirov reporting！- lab 1 - variant 3 - Set based on binary tree

A binary search tree (BST), also called an ordered or sorted binary tree,
is a rooted binary tree data structure with the key of each internal node
being greater than all the keys in the respective node's left subtree and
less than the ones in its right subtree. The time complexity of operations
on the binary search tree is linear with respect to the height of the tree.

Definition and property
Structure: Each node has a maximum of two children (left child and right child).

Order:

The value of all nodes in the left subtree < the value of the current node.

The value of all nodes in the right subtree > the value of the current node.

All subtrees satisfy the above rule (recursively defined)

### Advantages and disadvantages
| Advantages| disadvantages|
|----|----|
|Fast lookup (similar to binary lookup)|Worst case degenerates to linked list (efficiency plummets)|
|Support dynamic data insertion and deletion |need to maintain balance (otherwise the efficiency is unstable)|
|Natural support for ordered traversal (mid-order traversal) |is not suitable for frequently inserted and deleted scenarios|

## Project structure

- `foo.py` -- implementation of `Foo` class and `add` features.
- `foo_test.py` -- unit and PBT tests for `Foo`.

## Implementation restrictions

- Unbalanced Tree --

Tree could be unbalanced, specially when the input is
sorted, which can significantly increase the time complexity. An AVL tree
or Red-Black tree, which automatically balances the tree after each insertion
or deletion.These balanced trees ensure that the operations remain O(log n)
even in the worst case. Also, a easy way to rebalance the tree is insert
nodes in a more randomized fashion, like using a Treap (a BST combined
with a heap).

- Iterative methods --

The current traversal methods use recursion, which
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

- Deletion Performance --

The current deletion approach for nodes with two
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

## Analysis of Unit Testing and Property-Based Testing (PBT)

## 1. Unit Testing

Unit testing ensures that individual parts of a program work as expected. It
typically tests specific functions or methods in isolation.

### Advantages(Unit Test)

- **Simple and Easy to Understand:**

  Unit tests such as `test_insert()`, `test_search()`, etc., are straightforward.
Each test focuses on a specific behavior of the BST (Binary Search Tree), making
the logic easy to follow and maintain.

- **Easy Debugging:**

  If a unit test fails, it’s usually easy to track down the specific problem
in the corresponding test function. The isolated nature of the tests makes
pinpointing issues simpler.

- **Explicit Boundary Conditions:**

  Unit tests can explicitly test boundary conditions like an empty tree, deleting
non-existing nodes, etc. These are intentional edge cases written by the developer
to ensure the program handles them correctly.

- **Quick to Implement:**

  Unit tests can be written quickly for known or anticipated behaviors of the
system.If a developer knows the expected outputs for certain inputs, the tests
are relatively easy to create.

### Disadvantages(Unit test)

- **Limited Coverage:**

  Unit tests often only cover common use cases. They may not uncover edge cases
or unexpected combinations of input and state. These are areas that might need
additional attention.

- **Manual Test Case Writing:**

  Writing unit tests requires manually specifying each possible input and its
expected outcome. This can become cumbersome, especially as the system grows
in complexity.

- **Doesn't Discover All Bugs:**

  Unit tests generally verify specific behaviors. As a result, they might miss
bugs that arise under certain conditions or with unusual combinations of data.

## 2. Property-Based Testing (PBT)

Property-based testing involves automatically generating a large number of test
cases to check the properties of the program. In this case, the `Hypothesis`
library in Python is used to generate random test inputs.

### Advantages(PBT Test)

- **Wide Coverage:**

  The key strength of PBT is its ability to automatically generate a wide range
of inputs, including boundary cases. This ensures that the code is tested across
a broader input space without requiring manually written test cases for each scenario.

- **Uncovers Edge Cases and Unexpected Bugs:**

  By generating random inputs, PBT is more likely to identify corner cases or
bugs that would otherwise be missed. It can reveal issues that arise only in
extreme or edge conditions, such as very large inputs.

- **Simplified Test Case Writing:**

  In PBT, instead of writing individual test cases for each possible input, you
define properties (e.g., "inorder traversal should be sorted") that the program
must satisfy. This greatly reduces the overhead of manually writing tests for
every case.

- **Automation:**

  PBT automatically generates test data, running tests on a large number of randomly
generated inputs. This makes it particularly useful when there are many potential
edge cases or when the input space is too large to cover manually.

### Disadvantages(PBT Test)

- **Difficult to Debug:**

  When a PBT test fails, it can be difficult to track down the exact cause. The input
data is randomly generated, so reproducing the failure might require multiple attempts.
This can make debugging more challenging.

- **Less Specific:**

  PBT focuses on testing the properties of the program rather than verifying exact
outputs. While this approach ensures that certain properties hold, it may not verify
specific behavior or correctness under all conditions.

- **Potential for Non-Representative Data:**

  Since the data is generated randomly, there is a chance that the generated data
may not be representative of real-world use cases. If the generation strategy is
not properly tuned, it might create impractical or irrelevant inputs.

## Summary

### **When to Use Unit Testing:**

- To test specific behaviors of the system.
- For cases where exact outputs need to be verified.
- When you want to test a system in a controlled, predictable manner.
- Ideal for debugging and pinpointing issues.

### **When to Use Property-Based Testing (PBT):**

- To test the general properties of the program.
- For automatically generating a large number of test cases.
- To uncover edge cases and bugs that are hard to identify manually.
- Suitable for large and complex input spaces.

## **Recommended Approach:**

- **Combining Both Approaches:**

The ideal approach is to use both unit testing and
property-based testing together. Unit tests ensure that the system works as expected
for known use cases, while PBT can help discover edge cases and validate broader
properties of the system. This combination maximizes the reliability and robustness
of your code.
