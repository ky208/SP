#-----------------------------------------------------
#
# Filename  : storage.py
#
#-----------------------------------------------------
# This file contains the storage class which stores and
# manipulates the assignment statements.

from Tree.tokenizer import Tokenizer
from Tree.parseTree import ParseTree
from Sort.mergeSort import MergeSorter

class Storage:
    # Initialize the storage, undo stack, and redo stack.
    def __init__(self):
        self.__storage = {}
        self.__undoStack=[]
        self.__redoStack=[]
        
    # Add a new assignment to the storage.
    def addAssignment(self,variable,value):
        # Save the current state of the storage for undo functionality
        self.saveCurrentUndoState()
        original_val = self.__storage.get(variable)
        success=True
        
        # Check for circular dependency before adding assignment
        if self.detectCircularDependency(variable,value):
            print(f"Assignment cannot be added. '{variable}' = '{value}' due to Maximum Recursion Error.\n")
            return False
        try:
            # Attempt to evaluate the expression
            self.evaluateExpression(value)
            self.__storage[variable] = value
        except ZeroDivisionError:
            print(f"Assignment cannot be added. '{variable}' = '{value}' due to Zero Division Error.")
            success = False
            
        except Exception as e:
            print(f"Error: {e}")
            success=False
        # If assignment was unsuccessful, revert to the original state
        if not success:
            if original_val is not None:
                self.__storage[variable] = original_val
                
            else:
                del self.__storage[variable]
            self.__undoStack.pop()
        return success     

    def detectCircularDependency(self,variable,value):
        # If variable is found in value, it means a circular dependency occurs.
        if variable in value:
            return True
        return False
    
    # Get the current storage.
    def getStorage(self):
        return self.__storage.copy()
    
    # Evaluate the given expression.
    def evaluateExpression(self,expression):
        # Check if expression only consists of digits.
        if expression.isdigit():
            return float(expression)
        
        # Tokenize the expression
        tokens = Tokenizer(expression).tokenize()
        
        # Iterate through the tokens in the expression
        for i,token in enumerate(tokens):
            # If token is an alphabet, check if it exists in the storage
            if token.isalpha():
                # Check if token exists in the storage. 
                # If token does not exist in storage, return None.
                if token not in self.__storage:
                    return None
                # Recursively evaluate the token in the expression
                value = self.evaluateExpression(self.__storage[token])
                
                # If evaluated results is None return None
                if value is None:
                    return None
                # Replace the token in the expression with its evaluated value
                tokens[i] = str(value)
        # Reconstruct the expression
        newExpression = ''.join(tokens)
        # Build a parse tree from the new expression
        tree = ParseTree.buildParseTree(newExpression)
        # Evaluate the parse tree and return the final result
        result = tree.evaluate()
        return result
    
    # Print the result of an assignment in a formatted manner
    def printFormattedResults(self,variable,expression,result):
        if result is not None:
            # Check if result is a float or integer
            if result.is_integer():
                print(f"{variable}={expression}=> {str(int(result))}")
            else:
                print(f"{variable}={expression}=> {str(float(result))}")
        else:
            print(f"{variable}={expression}=> {result}")

    # Display all current assignments and their results. 
    def displayAssignments(self):
        assignments = self.getStorage()
        print("\nCURRENT ASSIGNMENTS:\n********************")
        for variable,originalExpression in sorted(assignments.items()):
            try:
                # Evaluate and print each assignment's result
                result = self.evaluateExpression(originalExpression)
                self.printFormattedResults(variable,originalExpression,result)
            except Exception as e:
                print(f"Error: {e}")
    
    # Evaluate a specific variable and display its expression tree.    
    def evaluateVariable(self,variable):
        # Check if variable exists in the storage
        if variable in self.getStorage():
            # Retrieve the variable in the storage
            expression = self.getStorage()[variable]
            print("\nExpression Tree")
            # Build parse tree from the expression
            parseTree = ParseTree.buildParseTree(expression)
            # Print the parse tree in-order travesal
            parseTree.printInOrder()
            # Evaluate the expression
            result = self.evaluateExpression(expression)
            if result is not None:
                # Check if result is a float or integer
                if result.is_integer():
                    print(f"Value for variable \"{variable}\" is {str(int(result))}")
                else:
                    print(f"Value for variable \"{variable}\" is {str(float(result))}")
            else:
                print(f"Value for variable \"{variable}\" is {result}")
            
        else:
            print(f"Variable \"{variable}\" not found")
    
    # Sort assignments based on their evaluated results.
    def sortAssignments(self):
        # Get assignments in the storage
        assignments = self.getStorage()
        evaluatedDict = {}
        
        # Create a MergeSorter instance for sorting
        sorter = MergeSorter()
        
        # Iterate through each variable and its corresponding expression
        for var, exp in assignments.items():
            
            # Evaluate the expression and get the results
            result = self.evaluateExpression(exp)

            # Check if result is in the evaluated dictionary
            if result not in evaluatedDict:
                evaluatedDict[result] = []
                
            # Append the variable and expression tuple to the result list in the dictionary
            evaluatedDict[result].append((var, exp))
            
        # Create a dictionary to store the sorted assignments
        sorted_assignments = {result: sorter.mergeSort(eval_group.copy(),'asc') for result, eval_group in evaluatedDict.items()}
        return sorted_assignments
    
    
    # Kien Yu Redo/Undo 
    # Save the current state of the storage for undo functionality.
    
    # Return the undo stack with previous states of the storage
    def getUndoStack(self):
        return self.__undoStack
    
    # Returns the redo stack with previously undone states of the storage
    def getRedoStack(self):
        return self.__redoStack
    
    # Save the current state of the storage in the undo state
    def saveCurrentUndoState(self):
        self.__undoStack.append(self.__storage.copy())
        
    # Perform an undo operation by reverting to the previous  state in the undo stack.
    def undo(self):
        # If there are no more undo state, print no more assignments to undo
        if not self.__undoStack:
            print("No more assignments to undo.")
            return
        
        # Append a copy of the current storage to the redo stack
        self.__redoStack.append(self.__storage.copy())
        
        # Replace the current storage with the previous state from the undo stack
        self.__storage = self.__undoStack.pop()
        print("Latest entry deleted")
    
    # Perform a redo operation by reverting to the previously undone state in the redo stack.
    def redo(self):
        # If no assignments to redo, print no more assignments to redo.
        if not self.__redoStack:
            print("No more assignments to redo.")
            return
        
        # Append a copy of the current storage to the undo stack
        self.__undoStack.append(self.__storage.copy())
        
        # Replace the current storage with the previously undone state from the redo stack
        self.__storage = self.__redoStack.pop()
        print("Latest entry reverted")
        
    # Analyse and return the dependencies of each variable in the storage
    def analyze_dependencies(self):
        # Create a dictionary to store variable dependencies
        dependencies={}
        
        # Iterate through the variable and expressions in the storage
        for variable,expression in self.getStorage().items():
            # Find dependencies of current variable and store them in the dependencies dictionary
            dependencies[variable] = self.find_dependencies(expression,variable)
        return dependencies
    
    # Find dependences for a given variable within the expression
    def find_dependencies(self,expression,current_var):
        # Empty list to store dependencies
        dependencies = []
        
        # Tokenize the expression
        tokens = Tokenizer(expression).tokenize()
        # Iterate through tokens in the expression
        for token in tokens:
            # Check if token is an alphabetical character, excluding the current variable
            # and check if the token exists in the storage
            if token.isalpha() and token != current_var and token in self.getStorage():
                dependencies.append(token)
        
        # Remove duplicates bu converting the list to a set then back to a list again
        return list(set(dependencies))
    
    # Display variable dependencies for each variable in the storage.
    def display_dependencies(self):
        # Analyze variable dependencies and store result in a dictionary
        dependencies = self.analyze_dependencies()
        
        # Get the assignments from storage
        assignments = self.getStorage()
        
        # Print header
        print("\nVARIABLE DEPENDENCIES\n*********************")
        
        # Iterate through variables and their expression in a sorted order
        for variable,originalExpression in sorted(assignments.items()):
            try:
                # Evaluate the expression to obtain result
                result=self.evaluateExpression(originalExpression)
                
                # Print formatted results for the variable
                self.printFormattedResults(variable,originalExpression,result)
                
                # Get variable dependencies for the current variable
                variable_dependencies = dependencies.get(variable,[])
                
                # Print variable dependences or if there are no dependencies
                if variable_dependencies:
                    print(f"Variable '{variable}' depends on: {', '.join(variable_dependencies)}\n")
                          
                else:
                    print(f"Variable '{variable}' depends on: No Dependencies.\n")
            
            except Exception as e:
                print(f"Error {e}")
                
    def writeDependencyToFile(self,outputFile):
        # Analyze variable dependencies and store result in a dictionary
        dependencies = self.analyze_dependencies()
        # Get the assignments from storage
        assignments = self.getStorage()
        
        with open(outputFile,'w') as file:
            file.write("VARIABLE DEPENDENCIES\n*********************\n")
            
            for variable,originalExpression in sorted(assignments.items()):
                try:
                    # Evaluate the expression to obtain result
                    result=self.evaluateExpression(originalExpression)
                    # Format as integer if its a whole number, else keep it as a float
                    formattedResult = int(result) if result is not None and result.is_integer() else result
                    outputStr = f"{variable}={originalExpression}=> {formattedResult if result is not None else 'None'}\n"
                    file.write(outputStr)
                    
                    # Get variable dependencies for the current variable
                    variable_dependencies = dependencies.get(variable,[])
                    
                    if variable_dependencies:
                        file.write(f"Variable '{variable}' depends on: {', '.join(variable_dependencies)}\n\n")
                    else:
                        file.write(f"Variable '{variable}' depends on: No Dependencies.\n\n")
                    
                except Exception as e:
                    print(f"Error {e}")
                
                
    # Retrieve all current assignments and their results. (Kallen's additional feature)
    def retrieveAllAssignments(self):
        assignments = self.getStorage()
        formatted_assignments = []

        for variable, originalExpression in sorted(assignments.items()):
            try:
                result = self.evaluateExpression(originalExpression)
                formatted_assignments.append((variable, [result]))  # Ensure result is in a list
            except Exception as e:
                print(f"Error: {e}")

        return formatted_assignments
    