#-----------------------------------------------------
# EncryptDecrypt Class
#-----------------------------------------------------
#
# Name      : Toh Kien Yu
# StudentID : 2222291
# Class     : DAAA/FT/2B/05
# Filename  : operation.py
#
#-----------------------------------------------------
from Encrypt_Operation.shiftCipher import ShiftCipher
from File_Processing.fileOperation import FileOperation

class EncryptDecrypt(ShiftCipher):
    # Constructor
    def __init__(self):
        # Inherit from ShiftCipher class
        super().__init__()
    
    # Encrypt text
    def encrypt(self,text,shift):
        return self.changeText(text,shift,'E')
    
    # Decrypt text
    def decrypt(self,text,shift):
        return self.changeText(text,shift,'D')
    
    # Encrypt/Decrypt content in the file
    def encryptDecryptFile(self,inputFile,choice,cipherKey,outputFile):
        handleFile = FileOperation()
        try:
            # Read file
            message = handleFile.readFile(inputFile)
            
            if message is not None:
                # Encrypt/Decrypt the message based on user's choice
                translated = self.changeText(message,cipherKey,choice)
                # Write encrypted/decrypted content into the output file
                handleFile.writeFile(outputFile,translated)
            else:
                print("Please enter a valid file name.")

        except FileNotFoundError:
            print(f"{inputFile} does not exists.")

        except FileExistsError:
            print("Output file already exists, enter a new file name.")