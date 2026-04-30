"""
Project Fusion toolbox module
by Khang Luong and Anthony Storm
CSCE 311, University of Nebraska-Lincoln
"""

import numpy as np
import statistics

def cal_stats(data, category, stat_type, config):
    """
    Data --> from fusion_experiment.csv
    stat_type --> Either SDM or mean
    config --> tokamak, reverse field pinch, or stellarator
    """
    
    cat = data[data[category] == config]

    if stat_type == 'mean':
        total = sum(cat)
        num_exp = len(cat)
        mean = total / num_exp

        return mean
    
    if stat_type == 'SDM':
        SDM = statistics.stdev(cat)

        return SDM

def merge_sorted_seq(array, left, middle, right):
    """Merges two sorted sub-arrays."""
    # Create copies of the sub-arrays to safely merge back into the original array
    left_part = array[left:middle].copy()
    right_part = array[middle:right].copy()
    
    i = j = 0
    k = left
    
    # Merge in descending order to support "Top X" ranking naturally
    while i < len(left_part) and j < len(right_part):
        if left_part[i] > right_part[j]:
            array[k] = left_part[i]
            i += 1
        else:
            array[k] = right_part[j]
            j += 1
        k += 1
        
    while i < len(left_part):
        array[k] = left_part[i]
        i += 1
        k += 1
        
    while j < len(right_part):
        array[k] = right_part[j]
        j += 1
        k += 1

def merge_sort(array, first, last):
    """Standard Merge Sort implementation (Recursive)."""
    if last - first <= 1:
        return
    
    middle = (first + last) // 2
    merge_sort(array, first, middle)
    merge_sort(array, middle, last)
    merge_sorted_seq(array, first, middle, last)
    
def bin_search(array, target):
    """Binary Search implementation for sorted arrays.
    Works with both integer IDs and float values."""
    left = 0
    right = len(array) - 1

    while left <= right:
        middle = (left + right) // 2
        mid_val = array[middle]
        
        # Check for exact match (integers) or near-equality (floats)
        if isinstance(target, int) or (isinstance(target, float) and target == int(target)):
            # Integer comparison
            if mid_val == target:
                return middle
        else:
            # Float comparison for efficiency values
            if abs(mid_val - target) < 1e-9:
                return middle
                
        if array[middle] < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1 

def find_min(self):

       cur = self.root                             # current node is the root node
       while cur.left is not None:                 # while the there is a node,
           cur = cur.left                          # go left (finds minimum value)
       return cur.data                             # return the current node, which is the leftmost node and thus the minimum

def find_max(self):

      cur = self.root                 # current node
      while cur.right is not None:    # while there are still larger nodes
          cur = cur.right             # keeps pointing to larger nodes
      return cur.data                 # returns value farthest right node

def contains(self, key):
       
      cur = self.root                         # sets current node
      found = False                           # has not found the key in the tree (just starting search)
      count = 0                               # keeps track of while loop searches
      while cur is not None and count < 16:   # keeps searching while a node exists (16 set for a stopping point, problem specific)
          if key == cur.data[0]:              # if the node has the key it is looking for,
              found = True                    # sets found to true
              count += 1                      # counts up the counter
          elif key < cur.data[0]:             # if the target key is less than current value in node,
              cur = cur.left                  # goes left to search lower nodes
              count += 1                      # counts up the counter
          else:                               # then the key is greater than the key in the node
              cur = cur.right                 # goes right to search higher keys
              count += 1                      # ups the counter

      return found

def correlation_matrix(design_matrix, compare_matrix):
    """
    Design matrix = data matrix containing row data and column categories
    Compare matrix = data that the design matrix is correlated to
    Output: matrix containing values from -1 to 1 correlating the design matrix to the compare matrix
    """

    y = compare_matrix
    X = design_matrix
    X_T = np.transpose(X)
    pre_pre_p = X_T @ X
    pre_p = np.linalg.inv(pre_pre_p)
    p = pre_p @ X_T
    b = p @ y

    return b
