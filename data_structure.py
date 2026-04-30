"""
Data structure definitions for the project.
by Khang Luong and Anthony Storm
CSCE 311, University of Nebraska-Lincoln
"""

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.parent = None

class Binary_Search_Tree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        new_data = (key, value)
        if self.root is None:
            self.root = TreeNode(new_data)
            return
        cur = self.root
        while cur is not None:
            cur_key = cur.data[0]
            if key < cur_key:
                if cur.left is None:
                    cur.left = TreeNode(new_data)
                    cur.left.parent = cur
                    return
                cur = cur.left
            elif key > cur_key:
                if cur.right is None:
                    cur.right = TreeNode(new_data)
                    cur.right.parent = cur
                    return
                cur = cur.right
            else:
                cur.data = new_data

    def find_min(self):
        if self.root is None:
            return None
        cur = self.root
        while cur.left is not None:
            cur = cur.left
        return cur.data

    def find_max(self):
        if self.root is None:
            return None
        cur = self.root
        while cur.right is not None:
            cur = cur.right
        return cur.data

    def contains(self, key):
        cur = self.root
        while cur is not None:
            if key == cur.data[0]:
                return True
            elif key < cur.data[0]:
                cur = cur.left
            else:
                cur = cur.right
        return False

    def find_range(self, min_val, max_val):
        """Returns a list of values (indices) for keys within [min_val, max_val]."""
        results = []
        self._find_range_recursive(self.root, min_val, max_val, results)
        return results

    def _find_range_recursive(self, node, min_val, max_val, results):
        if node is None:
            return

        key = node.data[0]
        
        # If node's key is greater than min_val, there might be more in the left subtree
        if key > min_val:
            self._find_range_recursive(node.left, min_val, max_val, results)
            
        # If node's key is in range, add its value (index)
        if min_val <= key <= max_val:
            results.append(node.data[1])
            
        # If node's key is less than max_val, there might be more in the right subtree
        if key < max_val:
            self._find_range_recursive(node.right, min_val, max_val, results)