#-----------------------------------------------------
# ShiftCipher Class
#-----------------------------------------------------
#
# Name      : Toh Kien Yu
# StudentID : 2222291
# Class     : DAAA/FT/2B/05
# Filename  : shiftCipher.py
#
#-----------------------------------------------------

class ShiftCipher:
    
    # Constructor
    def __init__(self):
        pass
    # Shift letter based on operation type, either decrypt or encrypt
    def shiftLetter(self, char, base, shift, operationType):
        if operationType == "E":
            return chr(((ord(char) - base + shift ) % 26) + base)
        elif operationType == "D":
            return chr(((ord(char) - base - shift ) % 26) + base)
    
    # Encrypt/Decrypt the whole text
    def changeText(self, text, shift, operationType):
        translated = ''
        # Loop through every character in the text
        for i in text:
            # If character is alphabetic, shift the letter
            if i.isalpha():
                if i.islower():
                    base = ord('a')
                    translated += self.shiftLetter(i,base,shift,operationType)
                else:
                    base = ord('A')
                    translated += self.shiftLetter(i,base,shift,operationType)

            else:
                # Non-alphabetic characters will stay the same
                translated += i
        return translated