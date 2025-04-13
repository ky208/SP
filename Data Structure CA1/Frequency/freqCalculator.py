#-----------------------------------------------------
# FrequencyCalculator Class
#-----------------------------------------------------
#
# Name      : Toh Kien Yu
# StudentID : 2222291
# Class     : DAAA/FT/2B/05
# Filename  : freqCalculator.py
#
#-----------------------------------------------------

class FrequencyCalculator:
    # Constructor
    def __init__(self):
        pass
    
    # Calculate frequency of each letter in the text
    def letterFrequency(self, text):
        frequency = { chr(i):0 for i in range(ord('A'), ord('Z') + 1)}
        totalLetters = 0
        # Loop through every character in the text
        for letter in text:
            if 'A' <= letter <= 'Z':
                frequency[letter] += 1
                totalLetters +=1
        return frequency,totalLetters
    
    # Calculate frequency of each letter in percentage
    def letterPctFrequency(self,frequency,totalLetters):
        frequency_percentage = {}
        
        # Calculate percentage frequency for each letter and store it in a dictionary 
        for letter,count in frequency.items():
            percentage = format(((count/totalLetters) * 100),".2f")
            frequency_percentage[letter] = percentage
        return frequency_percentage