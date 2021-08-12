
from pathlib import Path
import sys
import os
import logging
from PyQt5 import QtCore
from numpy import isnan
import pandas as pd
from xhtml2pdf import pisa
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import QObject,QThread, pyqtSignal,QSize
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QComboBox


from pytesseract import image_to_string 
from PIL import Image
import pytesseract

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.errorhandler import ErrorHandler
from selenium.webdriver.remote.file_detector import LocalFileDetector
from selenium.webdriver.remote.mobile import Mobile
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.remote.switch_to import SwitchTo
from selenium.webdriver.remote.webdriver import WebDriver

import math
import time
import json
from attendanceReportGeneratorUI import  Ui_MainWindow

class whatsappBot(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    messagePasser=pyqtSignal(str)
    def __init__(self, parent=None):
        super(whatsappBot, self).__init__(parent)
        self.reportFilePath='./report/'
        self.studentDetialsFilePath=None
        self.phNo=None
        self.greetings='Dear Parent, Greetings from KLH ECE Department'
        self.currentIndex=None 
    # def __init__(self,parent=None):
    #     super().__init__(parent)
    #     # self.filePath=None
    
    def run(self):
       if self.studentDetialsFilePath==None:
          self.messagePasser.emit("You have not selected the student list file")
          return
       self.driver=webdriver.Chrome(executable_path='./chromedriver.exe') 
       self.driver.get("https://web.whatsapp.com/")
       time.sleep(2)       
       try:
           WebDriverWait(self.driver, 200).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[3]/div/header/div[1]/div/div/span')))
       except:
            print('logging failed or timed out')
            return
       with open(self.studentDetialsFilePath) as csv_file:
            df=pd.read_csv(csv_file,header=0)
            for index, row in df.iterrows():
                if index < self.currentIndex:
                    continue                
                self.phNo=row[3]
                if pd.isna(self.phNo):
                    df.loc[index,6]='missing phone number'
                    logging.debug(str(row[1])+': missing parent\'s contact number')
                    continue
                
                if pd.isna(row[4]) or pd.isna(row[5]):
                    logging.warning("missing mentor detials")
                else:
                    greetingsToSend=self.greetings.replace('\n'," ")+"Mentor name: "+str(row[4]) +" contact number: "+str(int(row[5]))
                    
                self.reportFilePath=os.path.abspath('./report/'+str(row[0])+'.pdf')

                if not Path(self.reportFilePath).exists():                    
                    logging.error('error opening '+self.reportFilePath)         
                    continue
                       
                try:
                    self.driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[3]/div/header/div[2]/div/span/div[2]/div/span').click()
                    time.sleep(2)
                    self.driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[1]/div/label/div/div[2]').send_keys(str(int(self.phNo)))
                    time.sleep(2)
                    self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]/div[1]/div/div/div[2]/div').click()                    
                    time.sleep(2)
                    self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[1]/div[2]').click()    
                    time.sleep(2)
                    self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div[1]/div/ul/li[3]/button/input').send_keys(self.reportFilePath)
                    time.sleep(2)
                    self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/span/div/div/span').click()
                    time.sleep(2)
                    self.driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[1]/div').send_keys(greetingsToSend)                            
                    self.driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[2]/button/span').click()
                    time.sleep(2)
                    df.loc[index,6]='Done'                                        
                except Exception as e:
                    df.loc[index,6]='Error'
                    self.messagePasser.emit(str(e))
                    logging.error(str(e))
                progressPercentage=int((index/df.last_valid_index())*100)
                self.progress.emit(progressPercentage)    
            df.to_csv('sendResult.csv')
class reportGenBotWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    messagePasser=pyqtSignal(str)
    session_id= "none"
    url="none"
    stop=False
    def __init__(self, parent=None):
        super(reportGenBotWorker, self).__init__(parent)
        self.username=None
        self.mypassword=None
        self.currentIndex=None
        self.studentDetialsFilePath=None
        self.academicYear=None
        self.semester=None        


    def create_driver_session(self, session_id, executor_url):
            from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

            # Save the original function, so we can revert our patch
            org_command_execute = RemoteWebDriver.execute

            def new_command_execute(self, command, params=None):
                if command == "newSession":
                    # Mock the response
                    return {'success': 0, 'value': None, 'sessionId': session_id}
                else:
                    return org_command_execute(self, command, params)

            # Patch the function before creating the driver object
            RemoteWebDriver.execute = new_command_execute

            new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
            new_driver.session_id = session_id

            # Replace the patched function with original function
            RemoteWebDriver.execute = org_command_execute

            return new_driver

    def get_captcha_text(self,location,size):
            pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
            im = Image.open('screenshot.png') # uses PIL library to open image in memory

            left = location['x']
            top = location['y'] 
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']


            im = im.crop((left, top, right, bottom)) # defines crop points
            im.save('screenshot.png')
            captcha_text = image_to_string(Image.open('screenshot.png')).lower()
            os.remove('screenshot.png')
            return captcha_text.strip()
    def generateReport(self):        
        with open(self.studentDetialsFilePath) as csv_file:
            df=pd.read_csv(csv_file,header=0)
            for index, row  in df.iterrows():                                        
                if self.stop == True:
                    return 
                if index >=self.currentIndex:
                    try:
                        self.driver.find_element_by_xpath('//*[@id="dynamicmodel-profileid-selectized"]').clear()
                        self.driver.find_element_by_xpath('//*[@id="dynamicmodel-profileid-selectized"]').send_keys(str(row[0]).strip())                                
                        time.sleep(3)
                        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div/div/div[2]/div[1]/div[1]/form/div/div[1]/div[1]/div[2]')))
                        self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/div[1]/div[1]/form/div/div[1]/div[1]/div[2]').click()
                        # option=self.driver.find_element_by_xpath('//*[@id="dynamicmodel-profileid-selectized"]/option[contains(text(),'+str(row(0)).strip()+')]')
                        # elem._setSelected(option)                                
                    except Exception as e:
                        self.messagePasser.emit(str(e))
                        logging.error("Searching is a hard job. Could not find the student id") 
                        return
                    self.driver.find_element_by_xpath('//*[@id="dynamicmodel-academicyear"]/option[text()="'+self.academicYear+'"]').click()
                    self.driver.find_element_by_xpath('//*[@id="dynamicmodel-semesterid"]/option[text()="'+self.semester+'"]').click()
                    self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/div[1]/div[1]/form/div/div[4]/button[1]').click()
                    time.sleep(2)
                    tempList=[]
                    try:
                        # self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/div[1]/span/i').click()
                        numberOfCourses_elem=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div/div/div[2]/div[1]/div[1]/div/div/b')))
                        numberOfCourses=int(numberOfCourses_elem.text)
                        # time.sleep(2)                    
                        for i in range(numberOfCourses):
                            if self.stop !=True and i>=0:    
                                table_dict={
                                    'course_code':self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr['+str(i+1)+']/td[2]').text,
                                    'course_desc':self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr['+str(i+1)+']/td[3]').text,
                                    'ltps':self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr['+str(i+1)+']/td[4]').text,
                                    'section':self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr['+str(i+1)+']/td[5]').text,
                                    'year':self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr['+str(i+1)+']/td[6]').text,
                                    'semester':self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr['+str(i+1)+']/td[7]').text,
                                    'total_conducted':self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr['+str(i+1)+']/td[9]').text,
                                    'total_attended':self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr['+str(i+1)+']/td[10]').text,
                                    'total_absent':self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr['+str(i+1)+']/td[11]').text,
                                    'tcbr':self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr['+str(i+1)+']/td[12]').text,
                                    'percentage':self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/div[1]/div[1]/div/table/tbody/tr['+str(i+1)+']/td[13]').text
                                }
                                tempList.append(table_dict)
                        reportName_html=str(row[0])+'.html'
                        outDir ='./report'
                        if not os.path.exists(outDir):
                            os.mkdir(outDir)
                        fullName=os.path.join(outDir,reportName_html)                            
                        reportDf=pd.DataFrame(tempList)                    
                        reportDf.to_html(fullName,justify='center')                    
                        reportName_pdf=os.path.join(outDir,str(row[0])+'.pdf')
                        with open(fullName,'r') as f:
                            content=f.read()
                        content="<h1> ID:" + str(row[0]) +"   Name:"+ str(row[1])+'</h1><br><style> table {text-align: center;} table thead th {text-align: center;}@page {size: letter landscape;margin:  2cm;}</style>' + content                    
                        file=open(reportName_pdf,"w+b")
                        pisa.CreatePDF(content,file)
                        os.remove(fullName)
                        file.close()
                        del(reportDf)
                        df.loc[index,6] = 'success'                                                       
                    except TimeoutException:
                        df.loc[index,6] = 'error'
                        logging.error("Total number of courses not found")       
                    progressPercentage=round((index/df.last_valid_index())*100)
                    self.progress.emit(progressPercentage)                                       
                    self.driver.back()
                    time.sleep(1)                   
            df.to_csv('generationResult.csv')        
    def run(self):
            self.stop=False                                                                                             
            if self.session_id =="none" and self.url=="none":                                
                self.driver=webdriver.Chrome(executable_path='./chromedriver.exe')
            else:
                self.create_driver_session(self.session_id,self.url)
                
                             
            
            self.driver.get("https://newerp.kluniversity.in")
            self.driver.maximize_window()
            self.session_id=self.driver.session_id
            self.url=self.driver.command_executor._url

            assert "KL ERP" in self.driver.title            
            time.sleep(2)
            try:
                self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/nav/div[2]/ul/li[3]/a").click()            
                time.sleep(2)

                #captcha image xpath //*[@id="loginform-captcha-image"]

                element=self.driver.find_element_by_xpath("//*[@id='loginform-captcha-image']")
                location = element.location
                size = element.size
                self.driver.save_screenshot('screenshot.png')

                uname=self.driver.find_element_by_xpath("//*[@id='loginform-username']")
                uname.clear()
                uname.send_keys(Keys.HOME)
                uname.send_keys(self.username)


                pwrd=self.driver.find_element_by_xpath("//*[@id='loginform-password']")
                pwrd.clear()
                pwrd.send_keys(Keys.HOME)
                pwrd.send_keys(self.mypassword)

                captcha=self.driver.find_element_by_xpath('//*[@id="loginform-captcha"]')
                captcha.clear()
                captcha_text=self.get_captcha_text(location,size)
                captcha.send_keys(captcha_text)


                bt_login = self.driver.find_element_by_link_text("Login")
                WebDriverWait(self.driver, timeout=100, poll_frequency=1).until(EC.staleness_of(bt_login))
                logging.info("submitted and logged in")
            except Exception as e:
                logging.info("You are already logged in...")                
            
            try:                                              
                try:
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'sidebar11')))
                    logging.info("Page is ready")
                except TimeoutException:
                    logging.error("Loading error")      
                #Student Information    
                self.driver.get("https://newerp.kluniversity.in/index.php?r=studentattendance%2Fstudentdailyattendance%2Fsearchgetstdinput")
                time.sleep(2)
                
                self.generateReport()
                                              
                self.messagePasser.emit("End of File. Hope everything went well ;) If not, do not give up. Try and try till you succeed")
                logging.info("End of File. Hope everything went well ;) If not, do not give up. Try and try till you succeed")
                # self.driver.close()
                # self.session_id="none"
                # self.url="none"
            except Exception as e:
                self.messagePasser.emit(str(e))
                logging.error(str(e))
                print(str(e))
class reportGenBotUI(QMainWindow, Ui_MainWindow):
    
    def showErrorMessage(self,msgToDisplay):
            msgBox=QMessageBox()
            msgBox.setWindowTitle("Error")
            msgBox.setText(msgToDisplay)
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
            msgBox.setDefaultButton(QMessageBox.StandardButton.Ok)
            msgBox.setEscapeButton(QMessageBox.StandardButton.Ok)                        
            msgBox.exec_()
            msgBox.raise_()
            msgBox.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)

    
    
    def browseForFilePath(self):
            Path=QtWidgets.QFileDialog.getOpenFileName(self,"Select the session plan file","./",filter="CSV (*.csv)")            
            logging.info("SessionPlan filepath:"+ str(Path[0]))            
            self.leFilePath.setText(Path[0])
            self.filePath=Path[0]
            try:
                csv_file=open(self.filePath)
                csv_reader=pd.read_csv(csv_file,delimiter=',')            
                csv_reader.sort_values(csv_reader.columns[0],axis=0,inplace=True)
                id_list=csv_reader['student_uni_id'].tolist()                     
                self.worker.studentDetialsFilePath=Path[0]
                for id in id_list:
                    self.cbStudentID.addItem(str(id))                        
            except Exception as e:
                logging.error(str(e))
                
                
    
    def exitApp(self):
            sys.exit()
        
    def stopExecution(self):
        self.worker.stop=True
    
    def reportProgress(self, n):
        print("in progress with percentage: "+ str(n))        
        self.cbStudentID.setCurrentIndex(self.cbStudentID.currentIndex()+1)
        self.progressBar.setValue(n)

    def sendMessage(self):
        if self.teGreetings.toPlainText() !="" and self.leFilePath.text() !="":
            self.messenger.studentDetialsFilePath=self.leFilePath.text()
            self.messenger.greetings=self.teGreetings.toPlainText()
            self.messenger.currentIndex=self.cbStudentID.currentIndex()            
        else:
            self.showErrorMessage("AAh...!Forgot something? Enter all the details")
            logging.error("AAh...!Forgot something? Enter all the details")
            return
        self.progressBar.setValue(0)
        self.messenger.start()




    def run(self):                                 
        if self.leUserName.text() !="" and self.lePassword !="" and self.leFilePath.text() !="":
                self.worker.username=self.leUserName.text()
                self.worker.mypassword=self.lePassword.text()                              
                self.worker.academicYear=self.cbAcademicYear.currentText()
                self.worker.semester=self.cbSem.currentText()
                self.worker.currentIndex=self.cbStudentID.currentIndex()
        else:
                self.showErrorMessage("AAh...!Forgot something? Enter all the details")
                logging.error("AAh...!Forgot something? Enter all the details")
                return        
                
        self.worker.start()        


    def __init__(self,parent=None):
            super().__init__(parent)
            self.setupUi(self)
            self.pbGen.clicked.connect(self.run)
            self.pbBrowse.clicked.connect(self.browseForFilePath)
            self.pbExit.clicked.connect(self.exitApp)   
            self.pbStop.clicked.connect(self.stopExecution)
            self.pbSend.clicked.connect(self.sendMessage)           
            self.progressBar.setValue(0)            
            self.worker=reportGenBotWorker()
            # self.worker.started.connect(self.worker.run)
            self.worker.finished.connect(self.worker.quit)
            self.worker.finished.connect(self.worker.deleteLater)            
            self.worker.progress.connect(self.reportProgress)
            self.worker.messagePasser.connect(self.showErrorMessage)
            self.messenger=whatsappBot()
            self.messenger.finished.connect(self.messenger.quit)
            self.messenger.finished.connect(self.messenger.deleteLater)
            self.messenger.progress.connect(self.reportProgress)
            self.messenger.messagePasser.connect(self.showErrorMessage)
            logging.basicConfig(filename='attendanceReportGeneratorLog.log', format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s', datefmt='%Y-%m-%d,%H:%M:%S', level=logging.DEBUG , filemode='a') 

def main():
   app = QApplication(sys.argv)
   app.setApplicationName('KLH attendance report generator')   
   ex = reportGenBotUI()
   ex.setWindowIcon(QIcon('logo_48x48.png'))
   ex.setIconSize(QSize(48,48))
   ex.setWindowTitle('KLH attendance report generator')   
   ex.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()