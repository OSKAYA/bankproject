import datetime


class Bank():
    
    account_number= "XBNK-"+str(datetime.datetime.today().date())
    customer_count=0
    def __init__(self, customer):
        
        self.customer =customer
        Bank.customer_count+=1
        self.password=str()
        self.username=str()
        self.account_number=self.account_number+'-'+str(Bank.customer_count)
  
    
 

class Customer():
    def __init__(self):
        self.fullname=str()
        
        self.tel_no=str()
        self.identity=str()
        self.email=str()

  

