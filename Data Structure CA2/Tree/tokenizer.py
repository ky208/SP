#-----------------------------------------------------
#
# Filename  : tokenizer.py
#
#-----------------------------------------------------
# This file tokenizes the expression and returns a list 
# of tokens

class Tokenizer:
    def __init__(self,expression):
        # Initialize the Tokenizer with the given expression
        self.expression = expression
        
    def tokenize(self):
        # Tokenize the expression and return a list of tokens
        tokens = []
        currentToken = ''
        
        # Iterate through each character in the expression
        for char in self.expression:
            # Check if the character is alphanumeric or a dot
            if char.isalnum() or char=='.':
                currentToken += char
            else:
                if currentToken:
                    # Append the current token if it's not empty
                    tokens.append(currentToken)
                    currentToken = ''
                if char in ['+','-','*','/','=','(',')']:
                    # Append operators and parentheses as separate tokens
                    tokens.append(char)
                    
        if currentToken:
            # Append the last token if it's not empty
            tokens.append(currentToken)
            
            
        # Handle "**" as a single token
        new_tokens = []
        i = 0
        while i < len(tokens):
            if tokens[i] == '*' and i + 1 < len(tokens) and tokens[i + 1] == '*':
                # Merge consecutive '*' characters into a '**' token
                new_tokens.append('**')
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1

        return new_tokens
