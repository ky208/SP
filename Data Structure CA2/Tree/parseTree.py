#-----------------------------------------------------
#
# Filename  : parseTree.py
#
#-----------------------------------------------------
# This file contains the building of Parse Tree

from Tree.stack import Stack
from Tree.binaryTree import BinaryTree
from Tree.tokenizer import Tokenizer

# The ParseTree class represents a parse tree for mathematical expressions.
class ParseTree():
    # Constructor
    def __init__(self):
        pass
    
    # Build a parse tree from a mathematical expression.
    def buildParseTree(exp):
        # Tokenize the expression
        tokenizer = Tokenizer(exp)
        tokens = tokenizer.tokenize()
        
        # Check if the expression is in the form (number)
        if len(tokens) == 3 and tokens[1].replace('.', '').isdigit() and tokens[0] == "(" and tokens[2] == ")":
            return BinaryTree(float(tokens[1]))

        # Create a stack
        stack = Stack()
        tree = BinaryTree('?')
        stack.push(tree)
        currentTree = tree
        
        # Iterate through the tokens in the expression
        for t in tokens:
            # If token is '(' add a new node as left child
            # and descend into that node
            if t == '(':
                currentTree.insertLeft('?')
                stack.push(currentTree)
                currentTree = currentTree.getLeftTree() 
            
            # If is alphabetic
            elif t.isalpha():
                # Set the key of the current node as the variable name
                currentTree.setKey(t)
                parent = stack.pop()
                currentTree = parent
            
            # If token is operator set key of current node
            # to that operator and add a new node as right child
            # and descend into that node
            elif t in ['+', '-', '*', '/', '**']:
                currentTree.setKey(t)
                currentTree.insertRight('?')
                stack.push(currentTree)
                currentTree = currentTree.getRightTree()
            
            # Handle cases where the token is enclosed within parenthesis but represents a float e.g (1,23)
            elif t[0] == '(' and t[-1] == ')' and t[1:-1].replace('.', '').isdigit():
                try:
                    # Attempt the convert token into a float
                    t = float(t[1:-1])
                except ValueError:
                    raise ValueError(f"Invalid num {t}")
                # Set key of current node
                currentTree.setKey(t)
                
                # Move back to parent node in the tree
                parent = stack.pop()
                currentTree = parent
            # Handle cases where the token is a numeric value
            elif t.replace('.', '').isdigit():
                try:
                    # Attempt to convert token into a float
                    t = float(t)
                except ValueError:
                    raise ValueError(f"Invalid num {t}")
                # Set the key of current node
                currentTree.setKey(t)
                # Move back to the parent node
                parent = stack.pop()
                currentTree = parent
                
            # If token is ')' go to parent of current node
            elif t == ')':
                currentTree = stack.pop()  
        
            else:
                raise ValueError(f"Unexpected token {t}")
            
        return tree