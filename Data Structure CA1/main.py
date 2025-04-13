#-----------------------------------------------------
# Main Program
#-----------------------------------------------------
#
# Name      : Toh Kien Yu
# StudentID : 2222291
# Class     : DAAA/FT/2B/05
# Filename  : main.py
#
#-----------------------------------------------------
# To run: python main.py
#-----------------------------------------------------
import os
from Menu.menu import Menu
from Frequency.frequency import Frequency
from File_Processing.folder import Folder
from Encrypt_Operation.operation import EncryptDecrypt
from File_Processing.fileOperation import FileOperation

## Main Programme
def main():
    menu = Menu(8)
    frequency = Frequency()
    operationType = EncryptDecrypt()
    folder = Folder()
    fileOperation = FileOperation()
    menu.showMenu()
    input("\n\nPress enter key, to continue....\n")
    menu.insert(['Encrypt/Decrypt Message','Encrypt/Decrypt File','Analyze letter frequency distribution','Infer caesar cipher key from file','Analyze, and sort encrypted files','Analyse File Statistics','Create Text File','Exit'])
    exit = False

    while not exit:
        # Display menu options
        menu.showOptions()
        # User input
        userInput = input("Enter choice: ")
        
        # Input validation
        if not userInput.isdigit() or int(userInput) < 1 or int(userInput) > menu.getLength():
            print(f"Invalid Input. Please enter a number between 1 and {menu.getLength()}\n")
            
        # Encrypt/Decrypting messages
        elif userInput == "1":
            returnMenu = False
            while not returnMenu:
                # User chooses whether to encrypt or decrypt and inputs the text
                choice = input("Enter \"E\" for Encrypt or \"D\" for Decript (Enter \"B\" to return): ")
                choice = choice.upper()
                if choice == "B":
                    returnMenu = True
                    continue
                elif choice == "E":
                    text = input("\nPlease type text you want to encrypt: \n")
                elif choice == "D":
                    text = input("\nPlease type text you want to decrypt: \n")
                else:
                    print("Invalid input. Please enter \"E\" for Encrypt or \"D\" for Decript (Enter \"B\" to return): ")
                    continue
                
                # Input validation for cipher key    
                while True:
                    try:
                        cipherKey = int(input("\nEnter the cipher key: "))
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid integer.")
                
                # Perform encryption/decryption based on user input  
                if choice == "E":
                    result = operationType.encrypt(text,cipherKey)
                    print(f"\nPlaintext:\t{text}\nCiphertext:\t{result}")
                elif choice == "D":
                    result = operationType.decrypt(text,cipherKey)  
                    print(f"\nCiphertext:\t{text}\nPlaintext:\t{result}")
                    
                input("\n\nPress enter key, to continue....\n")
                returnMenu = True

        # Encrypting/Decrypting Files
        elif userInput == "2":
            returnMenu = False
            while not returnMenu:
                # User chooses whether to encrypt or decrypt and inputs the file
                choice = input("\nEnter \"E\" for Encrypt or \"D\" for Decript (Enter \"B\" to return): ")
                choice = choice.upper()
                if choice == "B":
                    returnMenu = True
                    continue
                elif choice == "E":
                    while True:
                        inputFile = input("\nPlease enter the file you want to encrypt: ")
                        if os.path.exists(inputFile):
                            break
                        else:
                            print(f"Error: {inputFile} does not exist.")
                        
                elif choice == "D":
                    while True:
                        inputFile = input("\nPlease enter the file you want to decrypt: ")
                        if os.path.exists(inputFile):
                            break
                        else:
                            print(f"Error: {inputFile} does not exist.")
                else:
                    print("Invalid input. Please enter \"E\" for Encrypt or \"D\" for Decript (Enter \"B\" to return): ")
                    continue
                
                # Input validation for cipher key
                while True:
                    try:
                        cipherKey = int(input("\nEnter the cipher key: "))
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid integer.")
                # Input validation output file (must be in .txt)
                while True:
                    outputFile = input("\nPlease enter an output file (.txt): ")
                    if outputFile.endswith(".txt"):
                        break
                    else:
                        print("File type not valid. Please enter a .txt file.")
                        
                # Encrypt/Decrypt the file      
                result = operationType.encryptDecryptFile(inputFile,choice,cipherKey,outputFile)
                print(f"{outputFile} created!")
                input("\n\nPress enter key, to continue....\n")
                returnMenu = True

        # Analyze letter frequency distribution
        elif userInput == "3":
            returnMenu = False
            while not returnMenu:
                try:
                    while True:
                        # User inputs the file to be analyzed
                        fileName = input("\nPlease enter the file you want to analyse (Enter \"B\" to return): ")
                        if fileName.upper() == "B":
                            returnMenu = True
                            break
                        elif os.path.exists(fileName):
                            break
                        else:
                            print(f"File {fileName} does not exist. Please enter a valid file name.")
                            
                    if returnMenu:
                        continue
                    
                    # Get the input file's letter frequency in percecntage 
                    letterFrequencyPct = frequency.showFrequencyFile(fileName)

                    
                    if letterFrequencyPct is not None:
                        # Display frequency graph
                        frequencyGraph = frequency.showFrequencyGraph(letterFrequencyPct)
                        frequencyGraph += "_"*78 + "|"
                        print(frequencyGraph)
                        letters = list(letterFrequencyPct.keys())
                        print('  '.join(letters))
                            
                    else:
                        print(f"Error: Unable to analyze {fileName}")     
                except Exception as e:
                    print(f"Error: {e}")
                    
                returnMenu = True
                input("\n\nPress enter key, to continue....\n")  

        # Infer caesar cipher key from file
        elif userInput == "4":
            returnMenu = False
            while not returnMenu:
                try:
                    while True:
                        # User inputs the file to be analyzed
                        inputFile = input("\nPlease enter the file you want to analyse (Enter \"B\" to return): ")
                        if inputFile.upper() == "B":
                            returnMenu = True
                            break
                        # If input file does not exist
                        elif not os.path.exists(inputFile):
                            print(f"Error: Input File {inputFile} does not exist.")
                            continue
                        break
                    if returnMenu:
                        break
                    
                    while True:
                        # User inputs the reference frequencies file to be analyzed
                        referenceFile = input("\nPlease enter the reference frequencies file (Enter \"B\" to return): ")
                        if referenceFile.upper() == "B":
                            returnMenu = True
                            break
                        # If reference file does not exist
                        elif not os.path.exists(referenceFile):
                            print(f"Error: Reference File {referenceFile} does not exist.")
                            continue
                        
                        break
                    if returnMenu:
                        break
                    # Infer Caesar cipher key
                    inferredCipherKey = frequency.inferCipherKey(inputFile,referenceFile)
                    print(f"The inferred caesar cipher key is: {inferredCipherKey}")
                    while True:
                        # User chooses whether to decrypt the input file and save it into an output file
                        choice = input(f"Would you want to decrypt this key? y/n: ")
                        if choice.lower() == 'y':
                            # Input validation output file (must be in .txt)
                            while True:
                                outputFile = input("\nPlease enter an output file: ")
                                if outputFile.endswith(".txt"):
                                    break
                                else:
                                    print("File type not valid. Please enter a .txt file.")
                            # Decrypt the file
                            operationType.encryptDecryptFile(inputFile,'D',inferredCipherKey,outputFile)
                            returnMenu = True
                            break
                        elif choice.lower() == 'n':
                            break
                        else:
                            print("Invalid input. Please enter 'y' or 'n'")
                                
                        
                except Exception as e:
                    print(f"Error: {e}")
                    
                input("\nPress enter key, to continue....\n")
                returnMenu = True
                
        # Analyze, and sort encrypted files
        elif userInput == "5":
            returnMenu = False
            while not returnMenu:
                try:
                    while True:
                        # User inputs folder to be batch processed
                        folderInput = input("\nPlease enter the folder name (Enter \"B\" to return): ")
                        if folderInput.upper() == "B":
                            returnMenu = True
                            break
                        # If the folder does not exist
                        elif not os.path.exists(folderInput):
                            print(f"\nError: Folder: {folderInput} does not exist.")
                            continue
                        break
                    if returnMenu:
                        break
                    # Batch processing of the files in the folder
                    status = folder.bulkRead(folderInput)
                    print(status)
                    returnMenu = True
                
                except FileNotFoundError as e:
                    print("Error: Please enter a valid folder name")

                except Exception as e:
                    print(f"Error: {e}\nenglishtext.txt does not exist.")

                input("Press enter key, to continue....\n")
                returnMenu  = True
                
        # Analyse File Statistics
        elif userInput == "6":
            returnMenu = False
            while not returnMenu:
                inputFile = input("Please enter the file name (Enter \"B\" to return): ")
                    
                if inputFile.upper() == "B":
                    returnMenu  = True
                else:
                    try:
                        # Analyse file and obtain statistics results
                        result = fileOperation.analyseFile(inputFile)
                        print("\nStatistics")
                        print("-" * 80)
                        for j,k in result.items():
                            print(f'{j}:\n{k}\n')
                        input("Press enter key, to continue....\n")
                        returnMenu = True
                    except FileNotFoundError:
                        print("Error: File does not exist.")
                    except Exception:
                        print("Error: Please input valid file name")

        # Create a text file
        elif userInput == "7":
            returnMenu = False
            while not returnMenu:
                try:
                    # User chooses a text file name
                    fileName = input("\nCreate a text file name (***.txt): ") + ".txt"
                    content = input("Enter the content in the text file: ")
                    
                    # User writes content into the file
                    fileOperation.writeFile(fileName,content)
                    print(f"\nText file '{fileName}' created successfully!\nContent:\n{content}")
                    returnMenu = True
                except Exception:
                    print("Error")
                    returnMenu = True
                    
                input("Press enter key, to continue....\n")
                
        # Exit the application
        elif userInput == "8":
            print("\nBye, thanks for using ST1507 DSAA: Caesar Cipher Encrypted Message Analyzer")
            exit = True


if __name__ == "__main__":
    main()