#-----------------------------------------------------
#
# Filename  : search.py
#
#-----------------------------------------------------
# This file retrieves variables within a specified range, utilizing the BubbleSort algorithm for sorting.
from Sort.bubbleSort import BubbleSorter

# kallen's additional feature (range searching)
class Search:
    def __init__(self, storage):
        # storage instance used for retrieving variables and their expressions.
        self.storage = storage
        self.sorter = BubbleSorter() # Instantiate BubbleSorter in the constructor

    def is_valid_range(self, input_str):
        '''
        Check if the input string for the range is valid.

        Returns:
        - True if the input string contains only valid characters, False otherwise.
        '''
        allowed_chars = set("0123456789-()")
        return all(char in allowed_chars for char in input_str)

    def getVariablesInRange(self, min_value, max_value):
        # Retrieve variables within the specified range.
        variables_in_range = []

        # Iterate over variables in storage
        for variable, expression in self.storage.getStorage().items():
            result = self.storage.evaluateExpression(expression)
            # Check if the result is within the specified range
            if result is not None and min_value <= result <= max_value:
                variables_in_range.append(variable)

        return variables_in_range
                
    def getRange(self):
        '''
        Get user input for the range, validate it, and retrieve variables within the range.
        Additionally, prompt the user for sorting options and display the sorted variables.
        '''
        while True:
            try:
                # Prompt user for the range in the format (min-max)
                range_input = input("\nEnter the range you wish to search (min-max), or enter 'X' to return to the main menu:\nFor example, (1-10)\n")

                # Check if the user wants to return to the main menu
                if range_input.lower() == 'x':
                    print("Returning to the main menu.")
                    return  # Exit the function

                # Validate the format of the range
                if not range_input.startswith('(') or not range_input.endswith(')') or ' ' in range_input:
                    raise ValueError("Invalid range format. Please use brackets and avoid spacing.")

                # Check if only allowed characters are entered
                if not self.is_valid_range(range_input):
                    raise ValueError("Invalid characters in the range. Please enter only numbers, brackets, and hyphens.")
                
                # Extract min and max values from the range string
                range_values = range_input[1:-1].split("-")

                # Check if it's a valid range (not a single value)
                if len(range_values) != 2:
                    raise ValueError("Invalid range. Please provide a valid range with two distinct values.")

                # Extract min and max values from the range string
                min_range, max_range = map(int, range_input[1:-1].split("-"))

                # Validate the range values
                if min_range >= max_range:
                    raise ValueError("Invalid range. The minimum value must be less than the maximum value.")

                variables_in_range = self.getVariablesInRange(min_range, max_range)

                if variables_in_range:
                    break  # Exit the loop if input is valid and processed
                else:
                    print(f"No variables found in the specified range.")

            except ValueError as ve:
                print(f"Error: {ve}")

        # Loop for sorting order input
        while True:
            try:
                # Prompt user for sorting
                sort_order = input("\nHow do you want to arrange the variables? Type 'asc' for ascending order or 'desc' for descending order:").lower()

                # Validate the sorting order
                if sort_order not in ['asc', 'desc']:
                    raise ValueError("Invalid sorting order. Please enter 'asc' for ascending or 'desc' for descending.")

                sorted_assignments = self.sortVariables(variables_in_range, sort_order)

                order_text = "ascending" if sort_order == "asc" else "descending"

                # Display both variable names and evaluated values
                formatted_assignments = ', '.join([f"{var}: {self.storage.evaluateExpression(value)}" for var, value in sorted_assignments])
                print(f"\nVariables in the range ({min_range}-{max_range}) sorted in {order_text} order: {formatted_assignments}")

                break  # Exit the loop if input is valid and processed

            except ValueError as ve:
                print(f"Error: {ve}")
    
    def sortVariables(self, variables, sort_order):
        assignments = [(variable, self.storage.getStorage()[variable]) for variable in variables]
        sorted_assignments = self.sorter.bubbleSort(assignments, sort_order) # sort using BubbleSort
        return sorted_assignments
