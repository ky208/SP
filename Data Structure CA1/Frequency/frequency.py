#-----------------------------------------------------
# Frequency Class
#-----------------------------------------------------
#
# Name      : Toh Kien Yu
# StudentID : 2222291
# Class     : DAAA/FT/2B/05
# Filename  : frequency.py
#
#-----------------------------------------------------

from Encrypt_Operation.operation import EncryptDecrypt
from Frequency.freqCalculator import FrequencyCalculator
from File_Processing.fileOperation import FileOperation

class Frequency:
    # Constructor
    def __init__(self):
        self.frequencyCalculator = FrequencyCalculator()
        self.fileOperation = FileOperation()

    # Show frequency Text
    def showFrequencyText(self,text):
        # Calculate letter frequency and total number of letters
        frequency,totalLetters = self.frequencyCalculator.letterFrequency(text)

        # Converting the frequency of each alphabet in percentage
        return self.frequencyCalculator.letterPctFrequency(frequency,totalLetters)
    
    # Show frequency file
    def showFrequencyFile(self,file):
        try:
            # Read file
            text = self.fileOperation.readFile(file)
            text = text.upper()
            # Calculate letter frequency and total number of letters
            frequency,totalLetters = self.frequencyCalculator.letterFrequency(text)
            # Converting the frequency of each alphabet in percentage
            return self.frequencyCalculator.letterPctFrequency(frequency,totalLetters)
        
        except FileNotFoundError:
            print(f"File {file} does not exists.")
    
    # Show frequency graph
    def showFrequencyGraph(self,letterFrequencyPct):
        rowLetterPct = []
        # Formatting the display of letter frequencies
        for letter,count in letterFrequencyPct.items():
            if float(count) > 10:
                rowLetterPct.append(f" {letter}-{count}%")
            else:
                rowLetterPct.append(f" {letter}- {count}%")
                
        # Sorting letter frequency by percentage in descending order
        sortedFrequency = sorted(letterFrequencyPct.items(),key=lambda item:float(item[1]),reverse=True)
        top5Pct = sortedFrequency[:5]
        top5Pct = dict(top5Pct)
        top5PctRow = []

        # Formatting the display of the top 5 letter frequency
        for letter,count in top5Pct.items():
            if float(count) > 10:
                top5PctRow.append(f"{letter}-{count}%")  
            else:
                top5PctRow.append(f"{letter}- {count}%")
        rowStr = ''
        # Generating frequency graph
        for i in range(26,0,-1):
            for letter,count in letterFrequencyPct.items():
                count = float(count)
                count = count * 26/100

                if count % 1 != 0:
                    noOfAesterisk = int(count) + 1

                else:
                    noOfAesterisk =  int(count)

            
                if i <= noOfAesterisk:
                    rowStr += '*  '
                else:
                    rowStr += '   '           

            rowStr += f"| {rowLetterPct.pop(0)}"

            if i == 16:
                rowStr += "\tTOP 5 FREQ"
                
            if i == 15:
                rowStr += "\t----------"

            if i <= 14:

                if len(top5PctRow) >= 1:
                    rowStr += f"\t| {top5PctRow.pop(0)}"
            
            rowStr += '\n'

        return rowStr
    
    # Find smallest difference between 2 dictionary
    def findSmallestDifference(self,message,sortedReference):
        smallestDiff = 10000
        smallestShift = None
        count = 0
        encryptDecrypt = EncryptDecrypt()
        # Iterate through every possible shifts and find the smallest difference
        for i in range(0,26):
            # Decrypting using current shift
            decrypted = encryptDecrypt.decrypt(message,count)
            # Calculate letter frequency in the decrypted text
            decryptedFrequency = self.showFrequencyText(decrypted)

            # Convert letter frequency to float
            for char,pct in decryptedFrequency.items():
                decryptedFrequency[char] = float(pct)
            diff=0
            
            # Calculate absolute difference between decrypted and referenced frequencies
            for letter in sortedReference:
                diff += abs(decryptedFrequency[letter]- sortedReference[letter])

            # Update the smallest difference and best shift
            if diff < smallestDiff:
                    smallestDiff = diff
                    smallestShift = count
                    
            # Increment the shift
            count +=1
        return smallestShift
    
    # Infer cipher key
    def inferCipherKey(self,inputFile,referenceFile):
        # Read reference file
        referenceText = self.fileOperation.readFile(referenceFile)
        referenceText = referenceText.upper()
        referencedFrequency = self.fileOperation.parseReferenceFile(referenceText)
        
        # Sort reference file's letter frequency in descending order
        sortedRef = dict(sorted(referencedFrequency.items(),key=lambda item:item[1],reverse=True))
        
        # Read input file
        message = self.fileOperation.readFile(inputFile)
        message = message.upper()
        
        # Find the smallest difference between input and reference file and return the cipher key
        smallestShift = self.findSmallestDifference(message,sortedRef)
        
        return smallestShift




