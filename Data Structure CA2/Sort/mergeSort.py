#-----------------------------------------------------
#
# Filename  : mergeSort.py
#
#-----------------------------------------------------
# This file implements the merge sort algorithm to sort
# a list of assignments either in ascending or descending order.

class MergeSorter:
    def __init__(self):
        pass
    
    # implementing merge sort algorithm with sort order
    def mergeSort(self, assignments, sort_order):
        # Check if length of assignment is greater than 1,
        # this will tell us if sorting is needed
        if len(assignments) > 1:
            # Split the list into two halves
            mid = len(assignments) // 2
            left_half = assignments[:mid]
            right_half = assignments[mid:]

            # Recursively apply merge sort to each half
            self.mergeSort(left_half, sort_order)
            self.mergeSort(right_half, sort_order)

            i = j = k = 0

            # Merge the two halves back into a sorted list
            while i < len(left_half) and j < len(right_half):
                # Compare and merge based on sort order, either ascending or descending
                if (sort_order == 'asc' and left_half[i][0] < right_half[j][0]) or (sort_order == 'desc' and left_half[i][0] > right_half[j][0]):
                    assignments[k] = left_half[i]
                    i += 1
                else:
                    assignments[k] = right_half[j]
                    j += 1
                k += 1
            # Handle any remaining elements in the left half
            while i < len(left_half):
                assignments[k] = left_half[i]
                i += 1
                k += 1
                
            # Handle any remaining elements in the right half
            while j < len(right_half):
                assignments[k] = right_half[j]
                j += 1
                k += 1

        return assignments
    
    