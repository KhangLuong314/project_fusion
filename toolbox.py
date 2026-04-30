def merge_sorted_seq(array, left, right, end, temp_array):
    l = left
    r = right
    N = 0
    
    while l < right and r < end:
        if array[l] < array[r]:
            temp_array[N] = array[r]
            l += 1

        else:
            temp_array[N] = array[r]
            r += 1
        N += 1

        while l < right:
            temp_array[N] = array[l]
            l += 1
            N += 1

        while r < end:
            temp_array[N] = array[r]
            r += 1
            N += 1

        for i in range(end - left):
            array[i + left] = temp_array[i]

def merge_sort(array, first, last, temp_array):
    if first == last:
        return
    
    else:
        middle = (first + last) // 2

        merge_sort(array, first, middle, temp_array)
        merge_sort(array, middle + 1, last, temp_array)

        merge_sorted_seq(array, first, middle + 1, last + 1, temp_array)
    
def bin_search(array, target):
    left = 0
    right = len(array) - 1

    while left <= right:
        middle = (left + right) // 2

        if array[middle] == target:
            return middle
        elif array[middle] < target:
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