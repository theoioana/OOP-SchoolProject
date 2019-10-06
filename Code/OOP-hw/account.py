import datetime

#forward declaration of class User for using it in the folllowing classes: Bank and Account
class User:
    pass

#global list with numbers sequence for generating unique ibans
global x 
x = [range(1000000000,9999999999)]

#global index for list x for choosing the next available number sequence
index_x = 0

#store the creation time of a bank account to check in test function
start_times = {} 

#store the moment when account rapport is demanded to check in test test function
end_times = {}

#store the moment when a transaction is performed to check in test function
transaction_times = []

#class Bank that takes care of the operations of logging in and signing in
#-------------------------------------------------------------------------
class Bank:
    
    #list of User instances, the bank is maintaing the evidence of its users 
    #stores the new created user accounts' ID and password and checks the ID and password for logging in 
    list_users = [] 

    def __init__(self, name):
        self.name = name
        #we need a short name for the bank in order to include it in the IBAN code of an account
        self.short = name[0] + name[(int)(len(name) / 2)] + name[(int)(len(name) - 1)]
        
    #function for signing in
    def create_user(self, ID, password):
        #iterate through 'list_users' to check if the introduced ID is taken by another existing user
        for i in self.list_users:
            if isinstance(i,User):
                if ID == i.id:
                    print("ID already taken")
                    return 0
        
        new_user = User(ID, password, self.name) #create the new user account
        self.list_users.append(new_user) #add the newly created user to 'list_users'
        print("Account succesfully created!")
        return new_user
    
    #function for logging in
    def login_user(self,ID, password):
       ok = 0
       #check if the ID and password match with an existing account
       #iterate through 'list_users' to check if the introduced ID and password are matching with any existing user account
       for i in self.list_users:
           if isinstance(i, User):
               if i.id == ID and i.password == password:
                   print("You've logged in succesfully!\n")
                   ok = 1
                   return i
       if ok == 0:
            print("The ID or the password doesn't match.\n")
            return 0  #the function returns 0 if the ID and password doesn't match with any existing user accounts


#class that takes care of the responsabilities of a bank account
#---------------------------------------------------------------    
class Account:
    
    currency = "RON"
    balance = 0 #the total sum of money of the bank account
    transactions = [] #the list we store all the transactions performed 
    max_sum_allowed = 10000000 #the maximum sum allowed to have in the bank account

    #initialise the memebers of a bank account
    def __init__(self, ID, password, bank_name):
        global index_x 
        self.holder = User(ID, password, bank_name) #create a copy of the user's data
        self.iban = "RO" + "20" + self.holder.bank.short +str(x[0][index_x]) + "XX" #generate a unique iban
        index_x += 1
        self.balance = 0 #the total sum of money of the bank account
        now = datetime.datetime.now() #generate the creation time of the account
        self.start_datetime = str(now.strftime("%Y-%m-%d %H:%M:%S"))
        start_times[self.iban] = self.start_datetime #add it in the 'start_times' list for the test function 
    
    #function that takes care of inserting and extracting money from an account
    def modifiy_balance(self, sum):
        
        #check if the bank account reaches the maximum sum allowed
        if self.balance + (int)(sum) > self.max_sum_allowed:
            #offer the user the option to add less money so the 'max_sum_allowed' is not reached  
            print("The maximum sum of this account was reached! You cannot insert this sum of money! \n You can only add " + str(self.max_sum_allowed - self.balance)+"\n")
            print("Agree to only add this much?")
            ans = input("Enter Y/N: ")

            #the user accepts to add less money
            if ans == 'Y':

                sum2 = self.max_sum_allowed - self.balance

                self.balance += sum2 #add the sum to the 'balance' self member
                now = datetime.datetime.now()
                time = str(now.strftime("%Y-%m-%d %H:%M:%S")) #generate the time of the transaction
                transaction_times.append(time) #store the time for the test function
                #add the transaction to the list in order to be displayed in the account report
                self.transactions.append("The user inserted the sum of "+ str(sum2) + " RON from the account on " + time) 
                
            else:
                print("Transaction aborted")
                return 0 #the function returns 0 when the transaction can't be finished
        
        else:
            #check if there are sufficient funds in the bank account for extracting the sum inserted
            if self.balance + (int)(sum) < 0:
                print("Insufficient funds! TRANSACTION ABORTED! \n")
                return 0 #the function returns 0 when the transaction can't be finished
        
            else:
                self.balance += (int)(sum)
                if (int)(sum) < 0:
                    now = datetime.datetime.now()
                    time = str(now.strftime("%Y-%m-%d %H:%M:%S"))
                    transaction_times.append(time)
                    #adds in the self member 'transactions' list all the actions that a user performs with a bank account
                    self.transactions.append("The user extracted the sum of " + str(-sum) + " RON from the account on " + time )
                else:
                    now = datetime.datetime.now()
                    time = str(now.strftime("%Y-%m-%d %H:%M:%S"))
                    transaction_times.append(time)
                    self.transactions.append("The user inserted the sum of "+ str(sum) + " RON in the account on " + time)
    
    #function that prints details about a given account and also all the transactions' history
    #-----------------------------------------------------------------------------------------
    def account_report(self):
        print("======================= ACCOUNT REPORT =============================\n")
        now = datetime.datetime.now()
        time = str(now.strftime("%Y-%m-%d %H:%M:%S"))
        end_times[self.iban] = time
        print("----------------------- created on " + self.start_datetime + " untill " + time + "---------------------------\n")
        print("Bank:" + str(self.holder.bank.name))
        print("IBAN code: " + self.iban + '\n')
        print("Account Holder ID:" + self.holder.id +'\n')
        print("Account currency:" + self.currency + '\n')
        print("Final balance: " + str(self.balance))
        print("Record of all transaction:\n")
        for i in self.transactions:
            print(i + "\n")

#class that takes care of all the actions a logged in user can perform
#---------------------------------------------------------------------
class User:
    
    def __init__(self, ID, password, bank_name):
        self.id = ID
        self.password = password
        self.bank = Bank(bank_name) #an user is associated to a specific bank
        self.accounts = [] #list of user's all accounts 
    
    #function that creates an Account object and stores data about the new account  
    def open_account(self):
        new_account = Account(self.id, self.password, self.bank.name) #create an Account instance associated to the current user
        self.accounts.append(new_account) #add the user's new account in self memnber 'accounts' list
        print("Account succesfully created!\nYour unique IBAN is: " + str(new_account.iban) )
    
    #closes an existing account by elimnating it from the lists that keeps the user's bank account's evidence
    def close_account(self, iban):
        ok = 0
        for i in self.accounts:
            if isinstance(i, Account) :
                if i.iban == iban:      #find the introduced iban in the list of existing accounts
                    self.accounts.remove(i) #if found, erase it
                    ok = 1
                    print("Account succesfully closed!")

        #the case when the user introduces a non existing IBAN code
        if ok == 0:
            print("Transaction associated with a nonexisting account\n")
    
    #function that calls function 'modify_balance' form the class Account in order to change the state of an existing account
    def insert_sum(self,sum, dest_account_iban):
        ok = 0
        for i in self.accounts:
            if isinstance(i, Account) :
                if i.iban == dest_account_iban:  #find the introduced iban in the list of existing accounts
                    var = i.modifiy_balance((int)(sum)) #call of 'modifiy_balance' with positive value, meaning that money are inserted
                    ok = 1
                    if var != 0:   #'modify_balance' returns 0  when the transaction can't be finished
                        print("Transaction finished succesfully!")
        
        #the case when the user introduces a non existing IBAN code
        if ok == 0:
            print("Transaction associated with a nonexisting account\n")
    
    #function that calls function 'modify_balance' form the class Account in order to change the state of an existing account
    def extract_sum(self,sum, source_acount_iban):
        ok = 0
        for i in self.accounts:
            if isinstance(i, Account) : 
                if i.iban == source_acount_iban: #find the introduced iban in the list of existing accounts
                    var = i.modifiy_balance(-(int)(sum)) #call of 'modifiy_balance' with neagtive value, meaning that money are extracted
                    ok = 1
                    if var != 0: #'modify_balance' returns 0  when the transaction can't be finished
                        print("Transaction finished succesfully!")

        #the case when the user introduces a non existing IBAN code            
        if ok == 0:
            print("Transaction associated with a nonexisting account\n")
    
    #function that calls function 'modify_balance' form the class Account in order to change the states of 2 existing accounts,
    # by extracting and inserting money from the 2 accounts
    def transfer_money(self,source_account_iban, dest_account_iban, sum):
        #first, extract money from the source account
        ok = 0
        for i in self.accounts:
            if isinstance(i, Account) :
                if i.iban == source_account_iban:
                    var = i.modifiy_balance(-(int)(sum))
                    ok = 1
                    if var == 0:
                        return
        
        #the case when the user introduces a non existing IBAN code
        if ok == 0:
            print("Transaction associated with a nonexisting account\n")
            return

        #second, insert money in the source account
        ok = 0
        for i in self.accounts:
            if isinstance(i, Account) :
                if i.iban == dest_account_iban:
                    var = i.modifiy_balance((int)(sum))
                    ok = 1
                    if var != 0:
                        print("Transaction finished succesfully!")
        
        #the case when the user introduces a non existing IBAN code                
        if ok == 0:
            print("Transaction associated with a nonexisting account\n")
    
    #function that calls the 'account_report' function from Account class for an existing account
    def account_report(self, iban_account_to_report):
        ok = 0
        for i in self.accounts:
            if isinstance(i, Account):
                if i.iban == iban_account_to_report:
                    i.account_report()
                    ok = 1
        
        #the case when the user introduces a non existing IBAN code
        if ok == 0:
            print("Transaction associated with a nonexisting account\n")

