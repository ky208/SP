#-----------------------------------------------------
# Main Program
#-----------------------------------------------------
#
# Filename  : main.py
#
#-----------------------------------------------------
# To run: python main.py
#-----------------------------------------------------
# This is the main program for 
# ST1507 DSAA: Evaluating & Sorting Assignment Statements.


from Menu.menu import Menu
from Storage.storage import Storage
from Tree.parseTree import ParseTree
from Tree.tokenizer import Tokenizer
from utils import Utils
from File.file import File
from Search.search import Search
from Visualize.visualize import VariableBarPlot
import os

def main():
    # Initialize the classes
    menu = Menu(10)
    storage = Storage()
    utils = Utils()
    fileOperation = File()
    menu.showMenu()
    menu.insert(['Add/Modify assignment statement','Display current assignment statements','Evaluate a single variable','Read assignment statements from file','Sort assignment statements','Undo/Redo Assignments (Kien Yu)','Show Variable Dependencies (Kien Yu)','Search assignment statements (Kallen Ng)','Visualize Variables (Kallen Ng)','Exit',])
    exit = False
    
    # Main program
    while not exit:
        # Display main menu
        menu.showOptions()
        # User input
        userInput = input("Enter choice: ")

        # Validate user input
        if not userInput.isdigit() or int(userInput) < 1 or int(userInput) > menu.getLength():
            print(f"Invalid Input. Please enter a number between 1 and {menu.getLength()}\n")
        
        # Option 1: Add/Modify assignment statements
        elif userInput == "1":
            returnMenu = False
            while not returnMenu:
                # Prompts user to enter an assignment statement
                assignment = input("Enter the assignment statement you want to add/modify (Enter \"X\" to return):\nFor example, a=(1+2):\n")
                
                # If user inputs X, return back to main menu
                if assignment=="X" or assignment == "x":
                    returnMenu = True
                    continue
                try:
                    # Split assignment into a variable and value
                    variable,value = assignment.split("=")
                
                    # Check for spaces in variable name
                    if " " in variable or " " in value or not utils.checkParanthesis(value):
                        print("Invalid variable name. Spaces are not allowed. Please re-enter your assignment without spaces.\n")
                        continue
                    # Check if the assignment is correctly parenthesized
                    if not ((value.startswith("(") and value.endswith(")"))):
                        print("Invalid format. Ensure that the value is correctly enclosed in paranthesis.\n")
                        continue
                    
                    # Add/update the assignment in the storage
                    success = storage.addAssignment(variable,value)
                    # If successfully add/update the assignment in the storage then return to main menu
                    if success:
                        returnMenu = True
                        utils.press_enter_to_continue()
                except:
                    print("Invalid Assignment. Please enter in the correct format.\n")
                
        # Option 2: Display current assignment statements
        elif userInput =="2":
            try:
                # Display all the assignments from the storage
                storage.displayAssignments()
            except Exception as e:
                print(f"Error {e}\n")
            utils.press_enter_to_continue()
        
        # Option 3: Evaluate a single variable
        elif userInput=="3":
            returnMenu = False
            while not returnMenu:
                # Prompts user to input a variable to be evaluated
                inputVariable = input("Please enter the variable you want to evaluate (Enter \"X\" to return):\n" )
                
                # If user inputs X, return back to main menu
                if inputVariable=="X" or inputVariable=="x":
                    returnMenu=True
                    continue
                try:
                    # Check if the input variable exist in the storage
                    if inputVariable in storage.getStorage():
                        # Evaluate the variable and prints out the value
                        storage.evaluateVariable(inputVariable)
                        returnMenu = True
                        utils.press_enter_to_continue()  
                    else:
                        print(f"Variable \"{inputVariable}\" not found\n")
                except Exception as e:
                    print(f"Error {e}")
              
        # Option 4: Read assignment statements from file
        elif userInput == "4":
            
            returnMenu = False
            while not returnMenu:
                # Prompts the user to enter the input file
                inputFile = input("Please enter input file (Enter \"X\" to return): ")
                # If user inputs X, return back to main menu
                if inputFile =="X" or inputFile=="x":
                    returnMenu=True
                    continue
                try:
                    # Create a File object
                    fileProcessor = File()
                    # Read assignment statement and add the assignment statements into the storage
                    fileProcessor.readFile(inputFile,storage)
                    utils.press_enter_to_continue()
                    returnMenu=True
                except FileNotFoundError:
                    # If file does not exist then print file not found
                    print("File not found.\n")
                except Exception as e:
                    print(f"Error: {e}")
                    
            
                           
        # Option 5: Sort assignment statements
        elif userInput == "5":
            returnMenu = False
            while not returnMenu:
                # Prompt user to enter an output file
                outputFile = input("\nPlease enter an output file (Enter \"X\" to return): ")
                
                # If user inputs X, return back to main menu
                if outputFile =="X" or outputFile=="x":
                    returnMenu=True
                # Check if user enters a .txt file
                elif not outputFile.endswith(".txt"):
                    print("File type not valid. Please enter a .txt file.")
                else:
                    # Checks if the name of the output file exists
                    if os.path.exists(outputFile):
                        # If file exists then prompt whether the user wants to overwrite or create a new file name
                        choice = input("File already exists. Do you want to overwrite it?: (Y/N): ").upper()
                        if choice == "Y":
                            try:
                                # Sort the assignments in storage
                                sortedAssignments = storage.sortAssignments()
                                # Write the sorted assignments into the output file
                                fileOperation.writeFile(sortedAssignments,outputFile)
                                print("File written successfully")
                                utils.press_enter_to_continue()
                                returnMenu = True
                            except Exception as e:
                                print(f"Error writing to file {e}")
                        elif choice=="N":
                            continue
                        
                        else:
                            print("Invalid input. Returning to menu.\n")
                            returnMenu = True
                    else:
                        try:
                            # Sort the assignments in storage
                            sortedAssignments = storage.sortAssignments()
                            # Write the sorted assignments into the output file
                            fileOperation.writeFile(sortedAssignments,outputFile)
                            print("File written successfully")
                            utils.press_enter_to_continue()
                            returnMenu = True
                        except Exception as e:
                            print(f"Error writing to file {e}")
                            
                            
                
                                
        # Kien Yu's additional feature: Undo/Redo Assignments
        elif userInput == "6":
            returnMenu = False
            while not returnMenu:
                # Prompt user to enter an action ('D' for undo, 'R' for redo, 'X' to return to main menu)
                action = input("\nEnter 'D' to remove the latest entry or 'R' to restore the most recently deleted entry (Enter \"X\" to return): ").upper()
                
                # If user inputs D, perform an undo operation on the storage
                if action == "D":
                    # Perform undo
                    storage.undo()
                    returnMenu = True
                    utils.press_enter_to_continue()   
                # If user inputs R, perform a redo operation on the storage
                elif action == "R":
                    # Perform redo
                    storage.redo()
                    returnMenu = True
                    utils.press_enter_to_continue()  
                    
                # If user inputs X, return to main menu 
                elif action == "X":
                    returnMenu = True
                else:
                    print("Invalid input. Please enter 'D' or 'R'")
        
        # Kien Yu's additional feature: Show Variable Dependencies
        elif userInput == "7":
            # Display the variable dependency
            storage.display_dependencies()
            
            while True:
                choice = input("\nDo you want to write these dependencies into a text file? (Y/N): ").upper()
                # If user enters 'Y', prompt user to enter output file name
                if choice=="Y":
                    while True:
                        fileName = input("\nEnter filename to write variable dependencies (Enter \"X\" to return): ")
                        # If user inputs X, return to main menu
                        if fileName.upper()=="X":
                            break
                        
                        # Check if user enters a .txt file
                        if not fileName.endswith(".txt"):
                            print("File type not valid. Please enter a .txt file.")
                        else:
                            # Check if the file exists
                            if os.path.exists(fileName):
                                # If file exists, prompt user whether to overwrite the existing file
                                overwrite = input("File already exists. Do you want to overwite it? (Y/N): ").upper()
                                if overwrite == "Y":

                                    try:
                                        # Write variable dependency to file
                                        storage.writeDependencyToFile(fileName)
                                        print(f"Variable dependencies written to {fileName}")
                                        break
                                    except Exception as e:
                                        print(f"Error: {e}")
                                # If user chooses not to overwrite, user will enter a new file name
                                elif overwrite =="N":
                                    continue
                                else:
                                    print("Invalid input. Please enter 'Y' for yes, 'N' for no.")
                            else:
                                try:
                                    # Write variable dependency to file
                                    storage.writeDependencyToFile(fileName)
                                    print(f"Variable dependencies written to {fileName}")
                                    break
                                
                                except Exception as e:
                                    print(f"Error: {e}")
                    break
                elif choice=="N":
                    break
                else:
                    print("Invalid input. Please enter 'Y' for yes, 'N' for no.")

            utils.press_enter_to_continue()
            
        # Kallen's additional feature: (range searching)
        elif userInput == "8":  
            search = Search(storage)
            try:
                search.getRange()
                utils.press_enter_to_continue()  
            except Exception as e:
                print(f"Error: {e}")
                utils.press_enter_to_continue()
                pass
                
        # Kallen's additional feature: (visualize variables using barplot)                 
        elif userInput == '9':
            try:
                assignments = storage.retrieveAllAssignments() # retrieve all assignments stored in storage
                if not assignments:
                    print("No assignments found. To proceed, please assign values to at least one variable. Returning to the main menu...")
                    utils.press_enter_to_continue()
                    returnMenu = True # returns user back to main menu
                    continue
                # Filtering assignments to exclude those with None values."
                filtered_assignments = [(variable, values) for variable, values in assignments if None not in values] 
                variable_values = {variable: values for variable, values in filtered_assignments}
                visualize = VariableBarPlot(variable_values) # plot the barplot
                visualize.plot()
            except Exception as e:
                print(f"Error: {e}")
                utils.press_enter_to_continue()
                
                
        # Exit the program
        elif userInput == "10":
            print("\nBye, thanks for using ST1507 DSAA: Assignment Statement Evaluator & Sorter")
            exit = True

            
            

if __name__ == "__main__":
    main()
