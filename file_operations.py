import json
import classes
import os
import datetime 
from PyQt5.QtWidgets import QMessageBox


#For reading logs from logs.json file
def read_logs(user_id,operation,tb):
    
    f1="operation: {}, date: {}, amount: {}"  #for money insert&witdraw
    f2="operation: {}, date: {}, amount: {}, toWhom: {}" #for money transfer
    f3="operation: {}, date: {}"  #for password change
    with open('logs.json',"r") as jfile:
        data = json.load(jfile)
            
        logs= data[str(user_id)]['log']       
         
        if operation=='insert':
            tb.clear()
            for log in logs:
               if(log['type']=='insert'):
                    tb.append(f1.format(log['type'],log['date'],log['amount']))
            return
       
        elif operation=='transfer':
            tb.clear()
            for log in logs:
                if (log['type']=='transfer'):
                    tb.append(f2.format(log['type'],log['date'],log['amount'],log['to ']))
            return
        
        elif operation=='cash_withdraw':
            tb.clear()
            for log in logs:   
                if (log['type']=='cash_withdraw'):
                    tb.append(f1.format(log['type'],log['date'],log['amount']))
            return
        else :
            return 




def get_user_password(user_id,file):
   with open(file,"r") as jfile:
      data=json.load(jfile)
      return data[user_id]['password']
def change_password(user_id,file,new_password):
   with open(file,'r+') as jfile:
      data=json.load(jfile)
      data[user_id]['password']=new_password
      jfile.seek(0)
      json.dump(data,jfile,indent=2)
               
      log_update(user_id,'logs.json','password updated',None,0,None)
          
            
            
        

def get_balance(user_id,file)  :  
   with open(file,"r") as jfile:
      data=json.load(jfile)
      return data[user_id]['balance']
#this method is implemented to update logs file
def log_update(user_id,logfile,operation,amount,transfer,to):
    
    if transfer ==1:
         new_data={'type':operation,'date':str((datetime.datetime.now().time())),'amount':amount,'to ':to}
    else:
         new_data={'type':operation,'date':str((datetime.datetime.now().time())),'amount':amount}

    with open(logfile,"r+") as jfile:
        data = json.load(jfile)
        temp=data[user_id]['log']
   
        data[user_id]['log'].append(new_data)
        jfile.seek(0)
        json.dump(data, jfile,indent=2)
###################################account database -Settings############################
#This method is implemented to creating account file in first place and
# to register first user/account data in.
def create_accounts(new_bank_account,file):
   data= {}
   data[new_bank_account.customer.identity]=[]
   data[new_bank_account.customer.identity] = ({
           "Fullname":new_bank_account.customer.fullname,
           "Username":new_bank_account.username,
           "tel_no":new_bank_account.customer.tel_no,
           "identity":new_bank_account.customer.identity,
           "email":new_bank_account.customer.email,
           "password":new_bank_account.password,
           "account_no":new_bank_account.account_number,
           "balance":int()
      })
   with open(file,'a') as jfile:
      json.dump(data,jfile, indent=2)
      print("creating a new account file succesfull")



#Check accounts method is implemented to prevent creating new account with same identity
# which should be uniq     
# 
# 
def check_accounts(new_bank_account,file,msgbox):
   new_bank_account_id=new_bank_account.customer.identity
   with open(file,'r+') as jfile:
      data=json.load(jfile)
      if new_bank_account_id in data:
         msgbox.setText('This identity registered before\nCheck your identity!')
         msgbox.exec()
         return False 
      return True         
#####Creates log files
def create_logs(new_bank_account,file):
   log_data={}
   log_data[new_bank_account.customer.identity] = ({
           "log":[{"type":"","date":str((datetime.datetime.now().time())),"amount":""}],
           
   })
   with open('logs.json','a') as jfile:
      json.dump(log_data,jfile, indent=4)
      print("logs file created succesfully")
           
#This portion of codes registers incoming data from register page to accounts.json
def write_to_accounts(new_bank_account,file):

   new_data={}
   new_data[new_bank_account.customer.identity]=[]
   new_data[new_bank_account.customer.identity] = ({
           "Fullname":new_bank_account.customer.fullname,
           "Username":new_bank_account.username,
           "tel_no":new_bank_account.customer.tel_no,
           "identity":new_bank_account.customer.identity,
           "email":new_bank_account.customer.email,
           "password":new_bank_account.password,
            "account_no":new_bank_account.account_number,
            "balance":int()
      })
   with open(file,'r+') as jfile:
      data=json.load(jfile)
      data.update(new_data)
      jfile.seek(0)
      json.dump(data, jfile,indent=2)
      print("Accounts file updated succesfully")

###################################transections database -Settings############################
def write_to_logs(new_bank_account,file):
   id=new_bank_account.customer.identity
   new_log_data={}
   new_log_data[id] = ({
           "log":[{"type":"","date":str((datetime.datetime.now().time())),"amount":""}],
           
   })
   with open(file,'r+') as jfile:
      data=json.load(jfile)
      data.update(new_log_data)
      jfile.seek(0)
      json.dump(data, jfile,indent=2)
      print("Logs file updated succesfully")


def insert_money(user_id,file1,file2,amount)  :
   

   with open(file1,'r+') as jfile:
      data=json.load(jfile)
      
      try :
         
         data[user_id]['balance']=data[user_id]['balance']+int(amount)
         jfile.seek(0)
         json.dump(data,jfile,indent=2)
         print("Money inserted succesfully")
         
         log_update(user_id,file2,'insert',str(amount),0,None)
      except :
         print ("You should enter an int")

def withdraw_money(user_id,file1,file2,amount)  :
   

   with open(file1,'r+') as jfile:
      data=json.load(jfile)
      
      try :
         
         data[user_id]['balance']=data[user_id]['balance']-int(amount)
         jfile.seek(0)
         json.dump(data,jfile,indent=2)
         print("Money taken succesfully")
         log_update(user_id,file2,'cash_withdraw',(amount),0,None)
      except :
         print ("You should enter an int")
     
def transfer_money(user_id,file1,file2,amount,to)  :
   

   with open(file1,'r+') as jfile:
      data=json.load(jfile)
      
      try :
         
         data[user_id]['balance']=data[user_id]['balance']-int(amount)
         jfile.seek(0)
         json.dump(data,jfile,indent=2)
         print("Money sent succesfully")
         log_update(user_id,file2,'transfer',str(amount),1,to)
      except :
         print ("You should enter an int")   
  
      
