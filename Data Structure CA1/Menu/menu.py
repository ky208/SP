#-----------------------------------------------------
# Menu Class
#-----------------------------------------------------
#
# Name      : Toh Kien Yu
# StudentID : 2222291
# Class     : DAAA/FT/2B/05
# Filename  : menu.py
#
#-----------------------------------------------------

class Menu:
    # Constructor
    def __init__(self,options):
        self.__length = 0
        self.__list = []
        self.options = options
        return
    # Get menu length
    def getLength(self):
        return self.__length
    
    # Set menu length
    def setLength(self,length):
        self.__length = length
        
    # Get menu list
    def getList(self):
        return self.__list
    
    # Set menu list
    def setList(self,list):
        self.__list = list
    
    # Display menu
    def showMenu(self):
        print("\n"+"*"*56)
        print("*" + " ST1507 DSAA: Welcome to: " + " "*28 + "*")
        print("*" + " "*54 + "*")
        print("*" + " "*5 + "~ Caesar Cipher Encrypted Message Analyzer ~" + " "*5 + "*")
        print("*" + "-"*54 + "*")
        print("*" + " "*54 + "*")
        print("*  " + "- Done by: Toh Kien Yu (2222291) " + " "*19 + "*")
        print("*  " + "- Class: DAAA/FT/2B/05 " + " "*29 + "*")
        print("*"*56)
        return

    # Insert items into menu
    def insert(self,list):
        for i in list:
            self.__list.append(i)
            self.__length +=1
        return
    
    # Show menu options
    def showOptions(self):
        choices = ','.join(str(i) for i in range(1,self.options+1))
        print(f"Please select your choice: ({choices})")
        # Loop through the list and display the options
        for i in range(len(self.__list)):
            print(f"\t{i+1}. {self.__list[i]}")
        return