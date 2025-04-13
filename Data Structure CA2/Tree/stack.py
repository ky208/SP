#-----------------------------------------------------
#
# Filename  : stack.py
#
#-----------------------------------------------------
# This file contains the basic implementation of the 
# Stack class structure.

class Stack:
    def __init__(self):
        # Initialize an empty list to store stack elements
        self.__list= []
        
    # Check if the stack is empty
    def isEmpty(self):
        return self.__list == []
    
    # Return the number of elements in the stack
    def size(self):
        return len(self.__list)
    
    # Clear all elements from the stack
    def clear(self):
        self.__list.clear()
        
    # Add an item to the top of the stack
    def push(self, item):
        self.__list.append(item)
        
    # Remove and return the item from the top of the stack
    def pop(self):
        # Return None if the stack is empty
        if self.isEmpty():
            return None
        else:
            return self.__list.pop()
        
    # Return the item at the top of the stack without removing it
    def get(self):
        # Return None if the stack is empty
        if self.isEmpty():
            return None
        else:
            return self.__list[-1]
        
    # Return a string representation of the stack
    def __str__(self):
        output = '<'
        for i in range( len(self.__list) ):
            item = self.__list[i]
            if i < len(self.__list)-1 :
                output += f'{str(item)}, '
            else:
                output += f'{str(item)}'
        output += '>'
        return output