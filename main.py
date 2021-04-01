from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication,QMainWindow,QMessageBox
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import os, sys
import classes 
import json
import file_operations 
import controls


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("./bank2/ui/main_window.ui",self)
        self.setFixedSize(600,500)
        self.pushButton_Create_Account.clicked.connect(self.goto_Register_Window)
        self.pushButton_Login.clicked.connect(self.credential_check)
        self.msgbox= QMessageBox()
        self.msgbox.setIcon(QMessageBox.Critical)
        self.msgbox.setWindowTitle("Fail to Login")
    def credential_check(self):
        if os.path.isfile('accounts.json'):
            self.bank_account_id=self.lineEdit_identity_no.text()
            self.bank_account_password=self.lineEdit_password.text()
            if controls.Login_Fields_Control(self.bank_account_id,self.bank_account_password,self.msgbox):
                if   controls.Login_Control(self.bank_account_id,self.bank_account_password,'accounts.json'):
                    self.goto_User_Window(self.bank_account_id,self.bank_account_password)
        
        else:
           
            self.msgbox.setWindowTitle("Attention Please")
            self.msgbox.setText("No user registered yet \nPlease create an account first")
            self.msgbox.exec()
            
    def goto_Register_Window(self):
        registration_window=Registration_Window()
        widget.addWidget(registration_window)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goto_User_Window(self,id,password):
        user_window=User_Window(id,password)
        widget.addWidget(user_window)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    
class User_Window(QMainWindow):
    def __init__(self,id,password):
        super(User_Window,self).__init__()
        loadUi("./bank2/ui/user_window.ui",self)
        self.user_window_id=id
        self.user_windows_password=password
        self.customer=classes.Customer()
        self.bank_account=classes.Bank(self.customer) #cretes a new user
        
        self.pushButton_user_transactions.clicked.connect(self.goto_user_transactions_window)
        self.pushButton_user_settings.clicked.connect(self.goto_user_settings_window)
        self.pushButton_logout.clicked.connect(self.goto_MainWindow)
        self.show_user_info()
        file_operations.log_update(id,'logs.json','logged_in',None,0,None)

        self.pushButton_user_logs.clicked.connect(self.goto_user_logs_window)
    def goto_MainWindow(self):
        main_window=MainWindow()
        widget.addWidget(main_window)
        widget.setCurrentIndex(widget.currentIndex()+1)  

    def goto_user_transactions_window(self):

        user_transactions_window=User_Transactions_Window(self.user_window_id,self.user_windows_password)
        widget.addWidget(user_transactions_window)
        widget.setCurrentIndex(widget.currentIndex()+1)  
    
    def goto_user_logs_window(self):

        user_logs_window=User_Logs_Window(self.user_window_id,self.user_windows_password)
        widget.addWidget(user_logs_window)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def goto_user_settings_window(self):

        user_settings_window=User_Settings_Window(self.user_window_id,self.user_windows_password)
        widget.addWidget(user_settings_window)
        widget.setCurrentIndex(widget.currentIndex()+1) 

    def show_user_info(self): 
              
        self.bank_account.identity=self.user_window_id
        with open("accounts.json",'r') as jfile:
            data=json.load(jfile)
            user=data[self.bank_account.identity]['Fullname']
            self.textBrowser_welcome.setText("Welcome"+" " + user)
            acount_no=data[self.bank_account.identity]['account_no']
            self.label_account_no.setText("Account :"+acount_no)

class Registration_Window(QMainWindow):
    def __init__(self):
        super(Registration_Window,self).__init__()
        loadUi("./bank2/ui/registration_window.ui",self)
       # self.resize(300,300)
        
        self.pushButton_register.clicked.connect(self.user_create)
        self.pushButton_return.clicked.connect(self.goto_MainWindow)
        self.msgbox= QMessageBox()
        self.msgbox.setIcon(QMessageBox.Critical)
        self.msgbox.setWindowTitle("Fail to Register")
        
            
    def goto_MainWindow(self):
        #self.user_create()
        main_Window=MainWindow()
        widget.addWidget(main_Window)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def user_create(self):
        #creates a customer
        new_user=classes.Customer()
        new_user.fullname=self.lineEdit_fullname.text()
        new_user.tel_no=self.lineEdit_3_tel_no.text()
        new_user.identity=self.lineEdit_4_identity.text()
        new_user.email=self.lineEdit_5_email.text()
       
        #create a new_bank_account
        new_bank_account=classes.Bank(new_user)
        new_bank_account.password=self.lineEdit_6_password.text()
        new_bank_account.username=self.lineEdit_2_username.text()

        if controls.Customer_Fields_Control(new_user,new_bank_account,self.msgbox): 
            if os.path.isfile('accounts.json'):
                if  (file_operations.check_accounts(new_bank_account,'accounts.json',self.msgbox)):
                    file_operations.write_to_accounts(new_bank_account,'accounts.json') 
                    file_operations.write_to_logs(new_bank_account,'logs.json')
                    self.msgbox.setIcon(QMessageBox.Information)
                    self.msgbox.setText('Your account is registered succesfully')
                    self.msgbox.exec()
                    
                
            else:
                file_operations.create_accounts(new_bank_account,'accounts.json')
                file_operations.create_logs(new_bank_account,'logs.json')                             
                print ("New user created")
              
           
class User_Transactions_Window(QMainWindow):
    def __init__(self,id,password):
        super(User_Transactions_Window,self).__init__()
        loadUi("./bank2/ui/user_transactions_window.ui",self)
        self.insert_window_id=id
        self.insert_window_password=password
        self.pushButton_back.clicked.connect(self.goto_user_window)
        self.pushButton_insert_money.clicked.connect(self.insert_money)
        self.pushButton_cash_withdraw.clicked.connect(self.withdraw_money)
        self.pushButton_transfer_money.clicked.connect(self.transfer_money)
        self.textBrowser_current_balance.setText(str(file_operations.get_balance(self.insert_window_id,"accounts.json")))
        self.msgbox= QMessageBox()
        self.msgbox.setIcon(QMessageBox.Critical)
        
    def goto_user_window(self):
        user_window=User_Window(self.insert_window_id,self.insert_window_password)
        widget.addWidget(user_window)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def insert_money(self):
        try :
            amount=self.lineEdit_amount.text()
            if int(amount)<=0:
                self.msgbox.setWindowTitle("Info")
                self.msgbox.setIcon(QMessageBox.Warning)
                self.msgbox.setText('Amount is not valid')
                self.msgbox.exec()

            else:
                print (type(amount))
                file_operations.insert_money(self.insert_window_id,'accounts.json','logs.json',amount)
                
                self.textBrowser_current_balance.setText(str(file_operations.get_balance(self.insert_window_id,"accounts.json")))   
                print ("it is ok")
                self.msgbox.setIcon(QMessageBox.Information)
                self.msgbox.setText('Account Updated succesfully')
                self.msgbox.exec()
        except :
            self.msgbox.setIcon(QMessageBox.Warning)
            self.msgbox.setText('Amount is not valid')
            self.msgbox.exec()
    
    def withdraw_money(self):
        try :
            amount=self.lineEdit_amount.text()
            if int(amount)<=0:
                self.msgbox.setWindowTitle("Info")
                self.msgbox.setIcon(QMessageBox.Warning)
                self.msgbox.setText('Amount is not valid')
                self.msgbox.exec()
            else:
               
                file_operations.withdraw_money(self.insert_window_id,'accounts.json','logs.json',amount)
                #self.label_updated_balance.setText("Your balance is updated to " + str(file_operations.get_balance(self.insert_window_id,"accounts.json")))
                self.textBrowser_current_balance.setText(str(file_operations.get_balance(self.insert_window_id,"accounts.json")))   
                self.msgbox.setIcon(QMessageBox.Information)
                self.msgbox.setText('witdraw Succesful')
                self.msgbox.exec()
        except :
            self.msgbox.setWindowTitle("Info")
            self.msgbox.setIcon(QMessageBox.Warning)
            self.msgbox.setText('Amount is not valid')
            self.msgbox.exec()
   
    def transfer_money(self):
        try :
            amount=self.lineEdit_amount.text()
            if int(amount)<=0:
                self.msgbox.setWindowTitle("Info")
                self.msgbox.setIcon(QMessageBox.Warning)
                self.msgbox.setText('Please Check amount')
                self.msgbox.exec()

            else:
                
                to=self.lineEdit_transfer_account.text()
                if len(to)==0:
                    self.msgbox.setWindowTitle("Info")
                    self.msgbox.setIcon(QMessageBox.Warning)
                    self.msgbox.setText('Receiver is not valid')
                    self.msgbox.exec()
                else:

                    file_operations.transfer_money(self.insert_window_id,'accounts.json','logs.json',amount,to)
                    #self.label_updated_balance.setText("Your balance is updated to " + str(file_operations.get_balance(self.insert_window_id,"accounts.json")))
                    self.textBrowser_current_balance.setText(str(file_operations.get_balance(self.insert_window_id,"accounts.json")))   
                    self.msgbox.setWindowTitle("Info")
                    self.msgbox.setIcon(QMessageBox.Information)
                    self.msgbox.setText('Transfer Succesful')
                    self.msgbox.exec()
        except :
            self.msgbox.setWindowTitle("Info")
            self.msgbox.setIcon(QMessageBox.Warning)
            self.msgbox.setText('Amount is ot valid')
            self.msgbox.exec()

class User_Settings_Window(QMainWindow):
    def __init__(self,id,password):
        super(User_Settings_Window,self).__init__()
        loadUi("./bank2/ui/user_settings_window.ui",self)
        self.user_settings_id=id
        self.user_settings_password=password
        self.pushButton_back.clicked.connect(self.goto_user_window)
        self.pushButton_change_password.clicked.connect(self.change_password)
        
        self.textBrowser_current_password.setText(file_operations.get_user_password(id,'accounts.json')) 
        self.msgbox= QMessageBox()
        self.msgbox.setIcon(QMessageBox.Critical)
        self.msgbox.setWindowTitle("Fail to Change")

    def change_password(self):
        new_password=self.lineEdit_new_password.text()
        if (len(new_password)==0):
            self.msgbox.setWindowTitle("Fail to Change")
            self.msgbox.setIcon(QMessageBox.Warning)
            self.msgbox.setText('Please fill in new password field')
            self.msgbox.exec()
        
        elif (len(new_password)==6):
            file_operations.change_password(self.user_settings_id,'accounts.json',new_password)
            self.textBrowser_current_password.setText(file_operations.get_user_password(self.user_settings_id,'accounts.json'))
            self.msgbox.setWindowTitle("Info")
            self.msgbox.setIcon(QMessageBox.Information)
            self.msgbox.setText('Password is updated')
            self.msgbox.exec()
        else:
            self.msgbox.setWindowTitle("Fail to Change")
            self.msgbox.setIcon(QMessageBox.Warning)
            self.msgbox.setText('Lenght of new password should be 6 digits')
            self.msgbox.exec()
  
    def goto_user_window(self):
        user_window=User_Window(self.user_settings_id, self.user_settings_password)
        widget.addWidget(user_window)
        widget.setCurrentIndex(widget.currentIndex()+1)     

class User_Logs_Window(QMainWindow):
    def __init__(self,id,password):
        super(User_Logs_Window,self).__init__()
        loadUi("./bank2/ui/logs_window.ui",self)                    
        self.insert_window_id=id
        self.insert_window_password=password
        self.pushButton_back.clicked.connect(self.goto_user_window)  
        self.pushButton_print_logs.clicked.connect(self.print_logs)  
        self.msgbox= QMessageBox()
        self.msgbox.setIcon(QMessageBox.Critical)
        self.msgbox.setWindowTitle("Fail to Print Logs")
    def goto_user_window(self):
        user_window=User_Window(self.insert_window_id,self.insert_window_password)
        widget.addWidget(user_window)
        widget.setCurrentIndex(widget.currentIndex()+1) 
    
    def print_logs(self):
        
        if self.radio_Button_insert.isChecked():
            file_operations.read_logs(self.insert_window_id,'insert',self.textBrowser)

        elif self.radio_Button_cash_witdraw.isChecked():
            file_operations.read_logs(self.insert_window_id,'cash_withdraw',self.textBrowser) 

        elif self.radio_Button_transfer.isChecked():
            file_operations.read_logs(self.insert_window_id,'transfer',self.textBrowser) 

        else :
           
            self.msgbox.setText('Please Check kind of log you wish to see')
            self.msgbox.exec()
 
app=QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
mainwindow=MainWindow()
widget.addWidget(mainwindow)
widget.show()
sys.exit(app.exec_())



