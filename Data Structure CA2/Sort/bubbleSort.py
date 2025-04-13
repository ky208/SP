#-----------------------------------------------------
#
# Filename  : bubbleSort.py
#
#-----------------------------------------------------
# This file implements the bubble sort algorithm to sort
# a list of assignments either in ascending or descending order.

class BubbleSorter:
    def __init__(self):
        pass
    
    # Implementing bubble sort algorithm with sort order
    def bubbleSort(self, assignments, sort_order):
        n = len(assignments)
        for i in range(n):
            # Last i elements are already in place
            for j in range(0, n-i-1):
                if (sort_order == 'asc' and assignments[j][1] > assignments[j+1][1]) or (sort_order == 'desc' and assignments[j][1] < assignments[j+1][1]):
                    assignments[j], assignments[j+1] = assignments[j+1], assignments[j]
        return assignments