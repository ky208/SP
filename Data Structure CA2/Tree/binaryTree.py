#-----------------------------------------------------
#
# Filename  : binaryTree.py
#
#-----------------------------------------------------
# This file contains binary class which represents the
# binary expression tree.


# The BinaryTree class represents a binary tree node and provides methods for tree manipulation and evaluation.
class BinaryTree:
    def __init__(self,key, leftTree = None, rightTree = None):
        self.key = key
        self.leftTree = leftTree
        self.rightTree = rightTree
        
    # Set the key value of the node.    
    def setKey(self, key):
        self.key = key
        
    # Get the key value of the node.
    def getKey(self):
        return self.key
    
    # Get the left subtree of the node.
    def getLeftTree(self):
        return self.leftTree
    
    # Get the right subtree of the node.
    def getRightTree(self):
        return self.rightTree
    
    # Insert a new left subtree to the node.
    def insertLeft(self, key):
        # If there is no existing left subtree, create a new one with the key
        if self.leftTree == None:
            self.leftTree = BinaryTree(key)
        else:
            t =BinaryTree(key)
            self.leftTree , t.leftTree = t, self.leftTree
    
    # Insert a new right subtree to the node.
    def insertRight(self, key):
        # If there is no existing right subtree, create a new one with the key
        if self.rightTree == None:
            self.rightTree = BinaryTree(key)
        else:
            t =BinaryTree(key)
            self.rightTree , t.rightTree = t, self.rightTree
            
    # Print the tree in preorder traversal.
    def printPreorder(self, level):
        # Print the key of the current node based on tree levels
        print( str(level*'-') + str(self.key))
        # Recursively print the left subtree if it exists
        if self.leftTree != None:
            self.leftTree.printPreorder(level+1)
            
        # Recursively print the right subtree if it exists
        if self.rightTree != None:
            self.rightTree.printPreorder(level+1)
            
    # Evaluate the expression represented by the tree.
    def evaluate(self):
        if self.leftTree is None and self.rightTree is None:
            
            try:
                # If the current node has no children, try to convert its key to float
                return float(self.key)
            except ValueError:
                return None
            
        # Recursively evaluate the left and right subtrees and perform operation specified by the current node's key
        leftVal = self.leftTree.evaluate() if self.leftTree is not None else None
        rightVal = self.rightTree.evaluate() if self.rightTree is not None else None
        
        # Operations
        if self.key == '+':
            return leftVal + rightVal
        elif self.key == '-':
            return leftVal - rightVal
        elif self.key == '*':
            return leftVal * rightVal
        elif self.key == '/':
            if rightVal==0:
                raise ZeroDivisionError("Division by zero. Please enter a valid assignment")
            return leftVal / rightVal
        elif self.key =="**":
            return leftVal**rightVal
    
    # Print the tree in inorder traversal.
    def printInOrder(self,level=0):
        # Recursively print the right subtree if it exists.
        if self.rightTree:
            self.rightTree.printInOrder(level+1)
        
        # Print current node key with formatting.
        if isinstance(self.key,float):
            if self.key.is_integer():
                print(level*"." + str(int(self.key)))
            else:
                print(level*"." + str(float(self.key)))
  
        else:
            # Print current node's key if it is not a float
            print(level*"." + str(self.key))
            
        # Recursively print the left subtree if it exists
        if self.leftTree:
            self.leftTree.printInOrder(level+1)
