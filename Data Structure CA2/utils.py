#-----------------------------------------------------
#
# Filename  : utils.py
#
#-----------------------------------------------------
# This file contains the utilities needed for our program.

class Utils:
    def __init__(self):
        pass
    
    # Prompt user to enter to continue
    def press_enter_to_continue(self):
        input("\nPress enter key, to continue....\n")
    
    # Checks if given paranthesis is correctly parenthesized
    def checkParanthesis(self,expression):
        # Checks if expression starts with '(' and ends with ')'
        if not ((expression.startswith("(") and expression.endswith(")"))):
            return False
        
        balance = 0
        # Iterate the whole expression to ensure the 
        # number of '(' is the same as the number of ')'
        for char in expression:
            if char=="(":
                balance+=1
            elif char==")":
                balance -=1
            if balance < 0:
                return False
            
        return balance ==0
