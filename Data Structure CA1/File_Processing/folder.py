#-----------------------------------------------------
# Folder Class
#-----------------------------------------------------
#
# Name      : Toh Kien Yu
# StudentID : 2222291
# Class     : DAAA/FT/2B/05
# Filename  : folder.py
#
#-----------------------------------------------------


import os
from Encrypt_Operation.operation import EncryptDecrypt
from Frequency.frequency import Frequency

class Folder():
    # Constructor
    def __init__(self):
        pass
    
    # Batch processing of multiple encrypted files that are stored in a folder
    def bulkRead(self,folder):
        statusMsg = ''
        # Get full folder path
        folderPath = os.path.join(os.getcwd(),folder)
        referencedFile = 'englishtext.txt'
        message = EncryptDecrypt()
        frequency = Frequency()
        i = 0
        # Dictionary to store file name and corresponding inferred cipher key
        logKeys = {}
        
        # Loop through each file in the specified folder path
        for filename in os.listdir(folderPath):
                filePath = os.path.join(folderPath,filename)
                if os.path.getsize(filePath) > 0:
                    with open(filePath,'r') as file:
                        # Infer cipher key of the current file and store it in a dictionary
                        inferredCipherKey = frequency.inferCipherKey(filePath,referencedFile)
                        logKeys[filename] = inferredCipherKey
                        
        # Sort the logKeys dictionary based on cipher key in ascending order
        sortedLogKeys = dict(sorted(logKeys.items(), key=lambda x:x[1]))
        
        # Loop through sortedKeys dictionary, decrypt each files and create a decrypted output file
        for i,(filename,key) in enumerate(sortedLogKeys.items(),start=1):
            filePath = os.path.join(folderPath,filename)
            outputPath = os.path.join(folderPath,f'file{i}.txt')
            message.encryptDecryptFile(filePath,'D',key, outputPath)
            statusMsg += f"Decrypting: {filename} with key: {key} as: file{i}.txt\n\n"

        # Write the history the files decrypted inside log.txt file
        logOutputPath = os.path.join(folderPath,f'log.txt')
        f2 = open(logOutputPath,"w")
        f2.write(statusMsg)

        return statusMsg