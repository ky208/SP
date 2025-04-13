#-----------------------------------------------------
#
# Filename  : file.py
#
#-----------------------------------------------------
# This file provides functinality for file processing
# such as reading a file and writing to a file

class File:
    def __init__(self):
        pass
     # Reads assignments from a file and adds them to the storage.
    def readFile(self,fileName,storage):
        # Open the file in read mode
        with open(fileName,'r') as file:
            for line in file:
                # Split each line into a variable and value
                var,expression = line.strip().split("=")
                # Add assignment into the storage
                storage.addAssignment(var,expression)
            # Display assignment
            storage.displayAssignments()
                
    # Writes sorted assignments to a file.  
    def writeFile(self, sortedAssignments, outputFile):
        try:
            # Sort the keys (evaluation results) in descending order
            sortedResults = sorted(sortedAssignments.keys(), key=lambda x:(x is not None,x), reverse=True)
            # Open file in write mode
            with open(outputFile, 'w') as file:
                for result in sortedResults:
                    evalGroup = sortedAssignments[result]
                    # Format and write the result and evaluated group to the output file
                    file.write(self.formatGroup(result,evalGroup))
        except Exception as e:
            print(f"Error writting file {e}")
    
    # Format how the information is displayed
    def formatGroup(self,result,evaluatedGroup):
        formatString = ""
        # If result is not None, format it to either a float or integer
        if result is not None:
            resultStr = f"*** Statements with value=> {int(result)}\n" if result.is_integer() else f"***Statement with value=> {float(result)}\n"
        else:
            # If result is None just write None
            resultStr = f"*** Statements with value=> {result}\n"
        formatString += resultStr
        # Add each variable and its corresponding expression to formatString
        for var,exp in evaluatedGroup:
            formatString += f"{var}={exp}\n"
        formatString += "\n"
        return formatString