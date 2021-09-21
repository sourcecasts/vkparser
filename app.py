# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QAction, QMenu, QApplication, QDialog, QSystemTrayIcon, QStyle
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from processor import Processor
from group import Group
from repost import Repost
from message import Message

import init
import sys  
import untitled
import os
import threading 


class ExampleApp(QtWidgets.QMainWindow, untitled.Ui_MainWindow):
   
    def __init__(self):    # Main Processor ui class...
        super().__init__()
        
        self.setupUi(self)
        self.index = 0 
        self.sex = 0    
        self.number = self.spin_number_01.value() 

        self.lineEdit_3.setCursorPosition(1)
        header = self.tableWidget.horizontalHeader()    
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        
        header_2 = self.tableWidget_2.horizontalHeader()    
        header_2.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        header_5 = self.tableWidget_5.horizontalHeader()    
        header_5.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.tableWidget.setRowCount(self.number)

   
      
        self.btn_send.clicked.connect(self.send_msg)
        self.btn_sear.clicked.connect(self.start)
        self.btn_ava.clicked.connect(self.avatars)
        self.btn_repost.clicked.connect(self.get_repost)
        self.btn_base.clicked.connect(self.get_base)
        self.btn_token.clicked.connect(self.get_token)
        self.btn_sear_3.clicked.connect(self.gr_search)


        self.check_box_01.clicked.connect(self.check_01)
        self.check_box_02.clicked.connect(self.check_02)
        
        self.radio_01.toggled.connect(self.radio_clicked)
        self.radio_02.toggled.connect(self.radio_clicked)
        self.radio_03.toggled.connect(self.radio_clicked)
        
        self.spin_number_01.lineEdit().setReadOnly(True)
        self.spin_number_01.valueChanged.connect(self.update_number)
        
    def update_number(self):
        self.number = self.spin_number_01.value() 



    def radio_clicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.sex = radioButton.text()

    def check_01(self): 
        if self.check_box_01.isChecked():
            return True
        return False
 
    def check_02(self): 
        if self.check_box_02.isChecked():
            return True
        return False
    
    def check_03(self): 
        if self.check_box_03.isChecked():
            return True
        return False


    def send_msg(self):
        self.index = 0 
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setRowCount(1000)

        token = self.lineEdit_5.text() 
        users = self.lineEdit_4.text() 
        message = self.txtMessage.toPlainText()

        self.th = Message(token, users, message)
        self.th.message_length.connect(self.message_append)
        threading.Thread(target = self.th.running).start()

        self.statusBar.showMessage("Start processor...")
        
    
    def get_base(self):    # Select list metod...
    
        self.file = QtWidgets.QFileDialog.getOpenFileName(self, "Select file", "C:",  "(*.txt)")[0]
        if self.file != "":
            self.lineEdit_4.setText(self.file)
            self.statusBar.showMessage("List add...")
        else:
            pass

    def get_token(self):    # Select list metod...
    
        self.file = QtWidgets.QFileDialog.getOpenFileName(self, "Select file", "C:",  "(*.txt)")[0]
        if self.file != "":
            self.lineEdit_5.setText(self.file)
            self.statusBar.showMessage("Accsess token add...")
        else:
            pass       
   
    def avatars(self):
        is_token = self.lineEdit_1.text() 
        is_photo = 'eyJvaWQiOjYzNjAyMTE1NSwicGhvdG8iOnsibWFya2Vyc19yZXN0YXJ0ZWQiOnRydWUsInBob3RvIjoiMWRmNDc0NTA4MDp6Iiwic2l6ZXMiOltdLCJsYXRpdHVkZSI6MCwibG9uZ2l0dWRlIjowLCJraWQiOiJhMDQzZmViZjBkYzQxNjU1OGQ1YTliODYxYmFhNGE1OCIsInNpemVzMiI6W1sicyIsImRkZDc4NzZiYjBlYjE3OTFiZmJmOTBlNTQyNTFiNmI5NjE2OTc2MmQyZjUyNGFjNWJhZmIzMDcwIiwiODA4MDIxODg1MjkyNDczNzQwMCIsNTIsNzVdLFsibSIsIjBlNTRhNjU2YmJjODc3Mzg0NjA0MTgyMjVjZGU3OWFjZTZjYjUxZmQxMjg1MzQ3MDc5NzMxZjYzIiwiMjY5MTMxNzkzNzA4NTQ4ODU1MiIsOTEsMTMwXSxbIngiLCI5NTlmYTIzNzRiMGMyNWQzNGFiNmNjOGRjN2RhMjM2MTk3NzkyNDE4MWM5MWViNmViYWY0ZTJiNSIsIi04ODEwMDM3MzkwMzI3OTgzODk0Iiw0MjEsNjA0XSxbInkiLCJjMjE0M2FmMjU4ZWNjOTZlZGJmOTY5M2EyNzZkMmY3ZDQyZWQzOTNiZmI2NDI0NDNjYzk2MTZkMSIsIi0zNzEzNjU3NzQyODI5ODQ0ODE4Iiw1NjMsODA3XSxbInoiLCJjYmRmN2ZiYWYxZDM5NjMzOTVkZmY5YjQzMzk0NmNkY2ZjYzE0NDUyNGYzZjM3ZWFiMTRhODg5ZCIsIjI0OTg0OTA5NTI3Njc3OTAwMzIiLDc1NCwxMDgwXSxbIm8iLCIzZjU1NmRkOWU1ZjVjNjRiMTc1NjQ4YTM5MGRjM2I5MmNlYThiNmVjMjJjMWY1ZTlkYzdkYjdiOSIsIjI3NjUwMDg2NzA1ODEyOTA1NzMiLDEzMCwxODddLFsicCIsImU2YmRhYjZlYmFhMjdiYzYxZGY2ODkwYTZkNTdmOTRhN2Q4ZjY2MjllMDFlZGE2N2RiZjc1MWVmIiwiLTY1ODYyMzk1MzUyOTg4MjA3NzYiLDIwMCwyODddLFsicSIsImMwMTA2OWM3MWU2ZWU2OTQ1MGE3N2YwMTk3YjgzNDYyMjc2YTIwMzM1NTQyYjQ3ODc5NTQ1OTQyIiwiLTIyMjQxMDc2NjY4NDg5NjI3NzkiLDMyMCw0NThdLFsiciIsImFmYTNjYTRlYmYyNThjODFhOTA2NTAzY2ZkNzk5ODZkZjI3MDJkOTgwZmM5YTk0N2ZhMjk2ZjMwIiwiNjEyMDYzNDMxMjUwMTQ4NzU2NyIsNTEwLDczMV1dLCJ1cmxzIjpbXSwidXJsczIiOlsiM2RlSGE3RHJGNUdfdjVEbFFsRzJ1V0ZwZGkwdlVrckZ1dnN3Y0FcL2VFZi1ZenkwSW5BLmpwZyIsIkRsU21WcnZJZHpoR0JCZ2lYTjU1ck9iTFVmMFNoVFJ3ZVhNZll3XC9xQjJla1dkN1dTVS5qcGciLCJsWi1pTjBzTUpkTkt0c3lOeDlvallaZDVKQmdja2V0dXV2VGl0UVwvNmxDWHk2dDF2SVUuanBnIiwid2hRNjhsanN5VzdiLVdrNkoyMHZmVUx0T1R2N1pDUkR6SllXMFFcL3JvWV9iZlZ2ZHN3LmpwZyIsInk5OV91dkhUbGpPVjNfbTBNNVJzM1B6QlJGSlBQemZxc1VxSW5RXC8wRnRBc2toc3JDSS5qcGciLCJQMVZ0MmVYMXhrc1hWa2lqa053N2tzNm90dXdpd2ZYcDNIMjN1UVwvVFhiZmVyeElYeVkuanBnIiwiNXIycmJycWllOFlkOW9rS2JWZjVTbjJQWmluZ0h0cG4yX2RSN3dcL1dFWGh2QW42bUtRLmpwZyIsIndCQnB4eDV1NXBSUXAzOEJsN2cwWWlkcUlETlZRclI0ZVZSWlFnXC9KYWMtWDl4aEl1RS5qcGciLCJyNlBLVHI4bGpJR3BCbEE4X1htWWJmSndMWmdQeWFsSC1pbHZNQVwvei1lM2pIcmM4RlEuanBnIl19LCJzcXVhcmUiOiIiLCJkYXRhIjpbIntcInBob3RvXCI6XCI4ODk2MTEzN2RkeFwiLFwic2l6ZXNcIjpbXSxcInNpemVzMlwiOltbXCJtYXhcIixcImNiZGY3ZmJhZjFkMzk2MzM5NWRmZjliNDMzOTQ2Y2RjZmNjMTQ0NTI0ZjNmMzdlYWIxNGE4ODlkXCIsXCIyNDk4NDkwOTUyNzY3NzkwMDMyXCIsNzU0LDEwODBdLFtcIm9cIixcIjRmNzQzOGZmOTIxM2M2ZTcyNmMyMDBkMTk0MTY5ZDc1YzEzZDI0N2QxNzQzYjAxNzI0ZGQyNGM2XCIsXCItMTUzNDI3NjAwOTgyODY0NjYzNlwiLDc1NCwxMDgwXSxbXCJiXCIsXCIwNWIxODk0NjkxYjc0ZWMwOGRiY2E3OGJjOTVlMTk3OTI3MGY3MTI0YzdmMTgzOGJhZDQ4Mzk2NVwiLFwiLTE0NzE0MTA4OTU0NDMwMzY3NjRcIiw0MDAsNTczXSxbXCJhXCIsXCI1YTlmNDRjN2M0Y2Y5YTU2ZThmM2EzN2M0NDgyZTkzYTE3YzQyOGJmYzNkODVlYWExNTQ1NjM1OVwiLFwiLTU0ODA5NzI2Nzk1MDQwMzI1OTdcIiwyMDAsMjg2XSxbXCJjXCIsXCI5YTJkZjM5MDI1OGRiMjY4NTYwZThkN2Q5NGU3ZTc4MThmNGJmMTM3NTE5MWI3MmFmYjQzNWUxOFwiLFwiMzU3NTEyMzExMDY1MTk1OTE3XCIsMjAwLDIwMF0sW1wiZFwiLFwiNmQzOTA5ODM1MTcxZTZiMjRhN2IyYzM5ZDhhZjdjMmZkOWJmZjg3N2Q2ODdjZWYyYTAxZmI5MmNcIixcIjg2NDkwODU4NzE5NjU5MjQwNDRcIiwxMDAsMTAwXSxbXCJlXCIsXCJkODNlMWU3YWM5ZDYwZmYyNGRkYjYxNDk0NDU1ODQ0MTUwNmM5OTU2YjI0OWJjNDcwM2ZhMTg1ZFwiLFwiNjMwOTcwMTI0ODAzMjg0NzExXCIsNTAsNTBdXSxcInVybHNcIjpbXSxcInVybHMyXCI6W1wieTk5X3V2SFRsak9WM19tME01UnMzUHpCUkZKUFB6ZnFzVXFJblFcLzBGdEFza2hzckNJLmpwZ1wiLFwiVDNRNF81SVR4dWNtd2dEUmxCYWRkY0U5SkgwWFE3QVhKTjBreGdcL0ZJSENGaGtvdGVvLmpwZ1wiLFwiQmJHSlJwRzNUc0NOdktlTHlWNFplU2NQY1NUSDhZT0xyVWc1WlFcL3BIVjZJcFpfbE9zLmpwZ1wiLFwiV3A5RXg4VFBtbGJvODZOOFJJTHBPaGZFS0xfRDJGNnFGVVZqV1FcL3E0eUtMbU9zNzdNLmpwZ1wiLFwibWkzemtDV05zbWhXRG8xOWxPZm5nWTlMOFRkUmtiY3EtME5lR0FcL2piWGVmNDBqOWdRLmpwZ1wiLFwiYlRrSmcxRng1ckpLZXl3NTJLOThMOW1fLUhmV2g4N3lvQi01TEFcL3pPcGdsc2E1QjNnLmpwZ1wiLFwiMkQ0ZWVzbldEX0pOMjJGSlJGV0VRVkJzbVZheVNieEhBX29ZWFFcLzU1N0lTUHlud1FnLmpwZ1wiXSxcIm1hcmtlcnNfcmVzdGFydGVkXCI6dHJ1ZX0iLCIwLDAsNzU0LDEwODAsNzUsNzUsNjAzIl0sImJ3YWN0Ijoib3duZXJfcGhvdG8iLCJzZXJ2ZXIiOjg1NjAxMiwibWlkIjo2MzYwMjExNTUsIl9zaWciOiJhMDdmOWViMGRiNGUxOTZkODBiNmU3YWZmM2Y4MmE2ZSJ9' 
        is_hash = '7448f93f405dfd5c444f5d4aabb84942'

        vk_session = VkApi(token = is_token)
        vk = vk_session.get_api()
        
    
        if vk is not None:
            vk.photos.saveOwnerPhoto(server = 999, photo = is_photo, hash = is_hash)
            print("Аватар изменен")

        else:
           print("Не удалось изменить аватар")

    def start(self):    # Start stream metod...
        
        self.index = 0 
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(self.number)
        
        self.token = self.lineEdit_5.text() 
        with  open(self.token, encoding = 'iso-8859-1') as file_token:
            self.tk = file_token.readline()
            group = self.lineEdit_3.text()
            stolder = self.spin_number_02.value()
            edolder = self.spin_number_03.value()
 


            self.th = Processor(self.tk.strip(), group, self.number, stolder, edolder, self.sex, self.check_01(), self.check_02(), self.check_03())
            self.th.length.connect(self.append)
            threading.Thread(target = self.th.running).start()

            self.statusBar.showMessage("Start processor...")
        
    def gr_search(self):    # Start stream metod...

        self.index = 0 
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.setRowCount(self.number)
        
        self.token = self.lineEdit_5.text() 
        with  open(self.token, encoding = 'iso-8859-1') as file_token:
            self.tk = file_token.readline() 
            self.q = self.lineEdit_7.text()
        
            self.th = Group(self.tk.strip(), self.q)
            self.th.group_length.connect(self.group_append)
            threading.Thread(target = self.th.running).start()

            self.statusBar.showMessage("Start processor...")


    def get_repost(self):    # Start stream metod...
        self.index = 0 

        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.setRowCount(self.number)
        self.token = self.lineEdit_5.text() 
        self.wall = self.lineEdit_9.text()
        
        self.th = Repost(self.token, self.wall)
        self.th.repost_length.connect(self.repost_append)

        threading.Thread(target = self.th.running).start()
        self.statusBar.showMessage("Start processor...")

    def append(self, add_id, add_first, add_last, add_date, add_online, add_dialog):    # Append stream metod...
        
        index = 0
        self.index = self.index + 1
        index = self.index - 1
        
        add_online = int(add_online)
        if add_online == 0:
            
            add_active = "Офлайн"
        else:
            add_active = "Онлайн"
        
        add_dialog = int(add_dialog)
        if add_dialog == 0:
            
            add_sender = "Закрыты"
        else:
            add_sender = "Открыты" 

        
        item = QtWidgets.QTableWidgetItem(add_id)
        self.tableWidget.setItem(index, 0, item) 
        
        item = QtWidgets.QTableWidgetItem(add_first)
        self.tableWidget.setItem(index, 1, item)               

        item = QtWidgets.QTableWidgetItem(add_last)
        self.tableWidget.setItem(index, 2, item)               

        item_ative = QtWidgets.QTableWidgetItem(add_active)
        self.tableWidget.setItem(index, 3, item_ative)               

        item = QtWidgets.QTableWidgetItem(add_sender)
        self.tableWidget.setItem(index, 4, item)   
        
        if add_online != 0:
            item_ative.setForeground(QtGui.QColor(82, 129, 184))

        self.statusBar.showMessage("Retrive user id " + add_id)
        self.tableWidget.repaint()
        self.tableWidget.scrollToItem(item) 

        self.writer(add_id)
    

    def writer(self, id):    # Write data file metod...
    
        with open("C:/Users/Root/Desktop/Vkparser/result/output.txt", "a") as files:
            files.write(id + "\n")    
             
    def group_append(self, add_id, add_first, add_last):    # Append stream metod...
        
        index = 0
        self.index = self.index + 1
        index = self.index - 1
        

        
        item = QtWidgets.QTableWidgetItem(add_id)
        self.tableWidget_3.setItem(index, 0, item) 
        
        item = QtWidgets.QTableWidgetItem(add_first)
        self.tableWidget_3.setItem(index, 1, item)               

        item = QtWidgets.QTableWidgetItem(add_last)
        self.tableWidget_3.setItem(index, 2, item)               

 

        self.statusBar.showMessage("Retrive group id " + add_id)
        self.tableWidget_3.repaint()
        self.tableWidget_3.scrollToItem(item)        

    def repost_append(self, add_post, add_repost, add_likes, add_success):    # Append stream metod...
        
        index = 0
        self.index = self.index + 1
        index = self.index - 1
        

        
        item = QtWidgets.QTableWidgetItem(add_post)
        self.tableWidget_5.setItem(index, 0, item) 
        
        item = QtWidgets.QTableWidgetItem(add_repost)
        self.tableWidget_5.setItem(index, 1, item)               

        item = QtWidgets.QTableWidgetItem(add_likes)
        self.tableWidget_5.setItem(index, 2, item)               

        item = QtWidgets.QTableWidgetItem(add_success)
        self.tableWidget_5.setItem(index, 3, item) 

        self.statusBar.showMessage("Retrive group id " + add_success)
        self.tableWidget_5.repaint()
        self.tableWidget_5.scrollToItem(item)  



    def message_append(self, add_id, add_user, add_status):    # Append stream metod...
        
        index = 0
        self.index = self.index + 1
        index = self.index - 1
        

        
        item = QtWidgets.QTableWidgetItem(add_id)
        self.tableWidget_2.setItem(index, 0, item) 
        
        item = QtWidgets.QTableWidgetItem(add_user)
        self.tableWidget_2.setItem(index, 1, item)               

        item = QtWidgets.QTableWidgetItem(add_status)
        self.tableWidget_2.setItem(index, 2, item)               

 
        self.statusBar.showMessage("Retrive group id " + add_status)
        self.tableWidget_2.repaint()
        self.tableWidget_2.scrollToItem(item)  

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # Запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
