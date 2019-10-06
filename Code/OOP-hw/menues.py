import account
import os

#store all the existent banks created when an user specifies the bank where he wants to sign in
global banks_list
banks_list = []

def User_Menu():
    pass


#function for displaying and interactive menu for SIGN IN and LOG IN operations
#------------------------------------------------------------------------------
def First_Menu():


    print("Welcome to our application for banking!")
    print("What is the action you want to perform?\n")
    print("1.Sign in\n2.Log in\n")
    answer = input("Type in 1 or 2:")

    if answer == "1":
        bank = input("Enter the bank where you want to be a user: ")
        #if the bank introduced is new, add it to list 'banks_list'
        if bank not in banks_list:
            bank_user = account.Bank(bank)
            banks_list.append(bank_user)
        else:
            for i in banks_list:
                if isinstance(i, account.Bank):
                    if i.name == bank: #find if the specified bank is in the list to associate the new user account to it
                        bank_user = i 
        id = input("Enter the ID: ")
        password = input("Enter the password: ")
        my_user = bank_user.create_user(id, password) #the new user account is associated to the specified bank
       
        #the case when the ID is already used by another user
        while my_user == 0:
            id = input("Enter a different ID: ")
            my_user = bank_user.create_user(id, password) #the new user account is associated to the specified bank
         
        
        #the menu offers the posibility to return to the Log in/Sign in menu or to succeed to the User Menu
        print("Do you want to suceed to the USER MENU(1) or go back to the FIRST MENU(2)?")
        ans = input("Enter your option (1 or 2): ")
        if ans == "1":
            os.system('cls')
            User_Menu(my_user)
        else: 
             os.system('cls')
             First_Menu()
            
    else:
        if answer == "2":
            ok = 0
            while ok == 0:
                bank = input("Enter the bank where you want to log in:")
                for i in banks_list:
                    if isinstance(i, account.Bank):
                        if i.name == bank: #check if the introduced bank exists
                            bank_user = i
                            ok = 1
                            break
                #the case when the user wants to LOG IN for a nonexisting bank
                if ok == 0:
                    print("The introduced bank does not exist!")
            id = input("Enter the ID: ")
            password = input("Enter the password:")
            my_user = bank_user.login_user(id, password) 

            #the case when the ID or password doesn't match with any account created at a specified bank
            while my_user == 0:
                id = input("Enter the ID: ")
                password = input("Enter the password:")
                my_user = bank_user.login_user(id, password)
            os.system('cls')
            User_Menu(my_user) #after Log in, succeed directlyy to User Menu

#function for a logged in user, that displays an interactive menu for proceeding the desired transactions
#-------------------------------------------------------------------------------------------------------- 
def User_Menu(user_to_query):
    global count

    print("HELLO! WELCOME TO YOUR USER MENU!\n\n What kind of transaction would you like to perform?\n")
    print("1.Open a new account\n2.Close an existing account\n3.Insert money in an existing account\n4.Withdraw money from an existing account\n5.Transfer money between 2 existing accounts\n6.Display a report of an existing account")
    ans = input("Enter your option:")
    
    #choose to create a new bank account
    if ans == "1":
        if isinstance(user_to_query, account.User):
            user_to_query.open_account() #call function 'open_account' from class User
            
    else:
        #choose to close an existing account
        if ans == "2":
            iban = input("Enter the iban of the account to be closed:")
            if isinstance(user_to_query, account.User):
                user_to_query.close_account(iban)  #call function 'close_account' from class User
                
        else:
            #choose to insert money in an existing bank account
            if ans == "3":
                iban = input("Enter the iban of the account you want to feed:")
                sum = input("Enter the sum of money to insert:")
                if isinstance(user_to_query, account.User):
                    user_to_query.insert_sum(sum, iban) #call function 'insert_sum' from class User
            else:
                #choose to withdraw money from an existing bank account
                if ans == "4":
                    iban = input("Enter the iban of the account you want to withdraw from:")
                    sum = input("Enter the sum of money to withdraw:")
                    if isinstance(user_to_query, account.User):
                        user_to_query.extract_sum(sum, iban) #call function 'extract_sum' from class User
                else:
                    #choose to transfer money between 2 existing bank accounts
                    if ans == "5":
                        iban1 = input("Enter the iban of the account you want to transfer money from:")
                        iban2 = input("Enter the iban of the acount you want to tranfer money in:")
                        sum = input("Enter the sum of money you want to transfer:")
                        if isinstance(user_to_query, account.User):
                            user_to_query.transfer_money(iban1, iban2, sum) #call function 'transfer_money' from class User
                    else:
                        #choose to display detailed rapport of an existing bank account
                        if ans == "6":
                            iban = input("Enter the iban of the account:")
                            if isinstance(user_to_query, account.User):
                                user_to_query.account_report(iban) #call function 'account_report' from class User

    #the possibility to perform another transaction
    print("Do you want to perform another transaction?")
    ans = input("Enter Y/N:")
    if ans == "Y":
        os.system('cls')
        User_Menu(user_to_query)
    else:
        os.system('cls')
        #the possibility to return to the First Menu
        print("Do you want to get back to the first menu?")
        ans = input("Enter Y/N:")
        if ans == "Y":
            os.system('cls')
            First_Menu()
        else:
            #the end of the session
            os.system('cls')
            print("Thank you for choosing us for your transactions!\n \n             Have a good day!")
