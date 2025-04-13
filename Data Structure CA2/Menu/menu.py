#-----------------------------------------------------
#
# Filename  : menu.py
#
#-----------------------------------------------------
# This file handles the displaying of main menu such 
# as inserting items into the menu and displaying of options.

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
        print("\n"+"*"*59)
        print("*" + " ST1507 DSAA: Evaluating & Sorting Assignment Statements " + "*")
        print("*" + "-"*57 + "*")
        print("*" + " "*57 + "*")
        print("*  " + "- Done by: Toh Kien Yu (2222291) &" + " Kallen Ng (2222556)" + " *")
        print("*  " + "- Class: DAAA/FT/2B/05 " + " "*32 + "*")
        print("*" + " "*57 + "*")
        print("*"*59)
        print("\n")
        return

    # Insert items into menu
    def insert(self,list):
        for i in list:
            self.__list.append(i)
            self.__length +=1
        return
    
    # Show menu options
    def showOptions(self):
        choices = ','.join(f"'{i}'" for i in range(1,self.options+1))
        print(f"Please select your choice: ({choices})")
        # Loop through the list and display the options
        for i in range(len(self.__list)):
            print(f"\t{i+1}. {self.__list[i]}")
        return