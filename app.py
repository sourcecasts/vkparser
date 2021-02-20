# -*- coding: utf-8 -*-

# Copyright 2021 Roman Adodin <scriptgr@gmail.com>  
# https://www.youtube.com/channel/UCRv9n8HDvM8lq0Y9JCsB6Lg
# https://scriptgu.ru/
# https://vk.com/roman.adodin
# -----------------------------------------------------------------------------

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QAction, qApp, QMenu, QApplication, QDialog, QSystemTrayIcon, QStyle

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject
import threading 
from processor import Processor
import threading
import init
import sys  
import os
import untitled


class ExampleApp(QtWidgets.QMainWindow, untitled.Ui_MainWindow):
   
    def __init__(self):    # Main Processor ui class...
        super().__init__()
        
        self.setupUi(self)
        self.index = 0 
        self.sex = 0    
        self.number = self.spin_number_01.value() 
        header = self.tableWidget.horizontalHeader()    
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.setRowCount(self.number)

        self.btn_send.clicked.connect(self.hunter)
        self.btn_sear.clicked.connect(self.start)
        
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


    def hunter(self):
        is_token = self.lineEdit_1.text() 
        is_users = self.lineEdit_2.text() 
        is_messa = self.txtMessage.toPlainText()

        vk_session = VkApi(token = is_token)
        vk = vk_session.get_api()
        
    
        if vk is not None:
            vk.messages.send(user_id = int(is_users), random_id = get_random_id(), message = is_messa)
        else:
           print("Собщение не отправлено")


    def start(self):    # Start stream metod...
        
        self.index = 0 
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(self.number)
        
        token = self.lineEdit_1.text() 
        group = self.lineEdit_3.text()
        stolder = self.spin_number_02.value()
        edolder = self.spin_number_03.value()
 


        self.th = Processor(token, group, self.number, stolder, edolder, self.sex, self.check_01(), self.check_02(), self.check_03())
        self.th.length.connect(self.append)
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
            item_ative.setForeground(QtGui.QColor(126, 224, 120))

        self.statusBar.showMessage("Retrive user id " + add_id)
        self.tableWidget.repaint()
        self.tableWidget.scrollToItem(item)        

     

      
def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # Запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
