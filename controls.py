from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import classes
import file_operations
import json

#registretion form fields control
def Customer_Fields_Control(new_user,new_bank_account,msgbox):
    if len(new_user.fullname)==0:
       
        msgbox.setText('Name field can`t be empty')
        msgbox.exec()
        return False
      
    if len(new_bank_account.password) <5:
       
        msgbox.setText("Password cant be less than 5 digits")
        msgbox.exec()
        return False

    if len(new_user.identity)!=3:
        msgbox.setText("Identity field shoul have 3 digits")
        msgbox.exec()
        return False

    return True
#************************************************************************
#Login page fields control, it is for verifying not for validation 

def Login_Fields_Control(bank_account_identity,bank_account_password,msgbox):
    if len(bank_account_identity)!=3:
       
       
        msgbox.setText('Identity digit can`t be less than 3 ')
        msgbox.exec()
        return False
    
    if len(bank_account_password)==0:
   
        msgbox.setText('Check your Password ')
        msgbox.exec()
        return False
        

    return True
#********************************************************
#This method validates the ented values are matches with database
def Login_Control(bank_account_identity,bank_account_password,file):
    with open(file,"r") as jfile:
        data = json.load(jfile)
        if bank_account_identity in data:
            if bank_account_password==data[bank_account_identity]['password']:
                print ("Login Succesfull")
                return True
            else:
                print ("Password does not match")
                return False
        else:
            print ("Identity no Found")
            return False
    