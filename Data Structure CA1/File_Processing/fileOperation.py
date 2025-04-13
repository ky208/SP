#-----------------------------------------------------
# FileOperation Class
#-----------------------------------------------------
#
# Name      : Toh Kien Yu
# StudentID : 2222291
# Class     : DAAA/FT/2B/05
# Filename  : fileOperation.py
#
#-----------------------------------------------------

from Frequency.freqCalculator import FrequencyCalculator

class FileOperation:
    # Constructor
    def __init__(self):
        pass
    
    # Read content in a file
    def readFile(self,file):
        try:
            # Open the file as read mode
            with open(file,'r') as f:
                content = f.read()
                return content
            
        except FileNotFoundError:
            print(f"File {file} does not exists")
            return
    
    # Write content into a file
    def writeFile(self,file,content):
        try:
            # Open the file as write mode
            with open(file,'w') as f:
                f.write(content)
                
        except Exception as e:
            print(f"Error writing to {file}: {e}")
            return
    
    # Parse referenced file for processing
    def parseReferenceFile(self,referenceFile):
        referencedFrequency = {}
        lines = referenceFile.split()

        # Loop through every line of the referenced file and assign keys to its corresponding value before storing it in a dictionary 
        for line in lines:
            key,value = line.split(',')
            referencedFrequency[key] = float(value)
        return referencedFrequency
            
    # Analyse file and obtain its statistics
    def analyseFile(self,inputFile):
        freqCalculator = FrequencyCalculator()
        content = self.readFile(inputFile)
        wordCount = len(content.split())
        charCount = len(content)
        
        numberOfLines = content.count('\n')
        
        letterFrequency,totalLetters = freqCalculator.letterFrequency(content.upper())
        
        # Split file content into sentences
        sentences = content.split('.')
        totalWords = 0
        sentenceCount = 0

        for sentence in sentences:
            wordsInSentece = sentence.split()
            if len(wordsInSentece) > 1:
                totalWords += len(wordsInSentece)
                sentenceCount += 1
        # Calculate average words per sentence
        if sentenceCount > 0:
            averageWordPerSentence = totalWords/sentenceCount    
        else:
            averageWordPerSentence = 0

        # Results are stored in a dictionary
        analysisResults = {
            'Content': content,
            'Letter Frequency': letterFrequency,
            'Total Letter': totalLetters,
            'Word Count': wordCount,
            'Character Count': charCount,
            'Number Of Lines': numberOfLines + 1,
            'Average Word Per Sentence': averageWordPerSentence
        }
        return analysisResults
            
            