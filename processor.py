# -*- coding: utf-8 -*-

# Copyright 2021 Roman Adodin <scriptgr@gmail.com>  
# https://www.youtube.com/channel/UCRv9n8HDvM8lq0Y9JCsB6Lg
# https://scriptgu.ru/
# https://vk.com/roman.adodin
# -----------------------------------------------------------------------------

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject
import datetime

import time

import threading 
from time import sleep

class Processor(QObject):    # Основной класс...
    
    length = QtCore.pyqtSignal(str, str, str, str, str, str)
    
    def __init__(self, token, group, number, stolder, edolder, sex, dialgs, online, old):    # Основной класс...
        super().__init__()

        self.now = datetime.datetime.now()
        self.offset = 0
        self.array = []

        self.token = token
        self.group = group
        self.number = number
        self.stolder = stolder
        self.edolder = edolder
        self.sex = sex
        self.dialgs = dialgs
        self.online = online
        self.old = old

        self.vk_session = VkApi(token = self.token)
        self.vk = self.vk_session.get_api()
    
    #---------------------------------------------------------------------------------------------
    def running(self): #Метод запуска основного процесса поиска...
    
        while True: 
            resp = self.vk.groups.getMembers(group_id = self.group, offset = self.offset, sort = "id_desc", fields = "bdate, sex, online, can_write_private_message")        
            self.array += resp["items"]
            self.offset += 1000
            if self.offset > resp["count"]:
                break
            elif len(self.array) == self.number:
                break
    
    
        for lists in self.array:
            self.sleep()
            if self.dialgs == True and self.online == True and self.old == True:
                self.on_old_open_dial(lists)
                
            elif self.dialgs == True and self.online == True:
                self.on_open_dial(lists)
           
            elif self.dialgs == True and self.old == True:
                self.old_dial(lists)

            elif self.online == True and self.old == True:
                self.on_old(lists)

            elif self.old == True:
                self.older(lists)
            
            elif self.dialgs == True:
                self.open_dial(lists)
                
            elif self.online == True:
                self.on(lists)
                   
            else:   
                self.off(lists)
                
                
    #---------------------------------------------------------------------------------------------
    def sleep(self):    # Метод устанавливает задержку в мс...
    
        sleep = time.sleep(0.001)
        return sleep



    #---------------------------------------------------------------------------------------------
    def older(self, lists):    # Метод поиска пользователей сообщества по возрасту
        try: 
            add_date = str(lists["bdate"])

            if len(add_date) >= 4 and add_date[-4:].isdigit():
                rez = add_date[-4:]
                
                if self.sex == "Женский":
                    gender = lists["sex"]
                    if gender == 1 and int(self.now.year - int(rez)) == self.stolder:
                        self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
            
                elif self.sex == "Мужской":
                    gender = lists["sex"]
                    if gender == 2 and int(self.now.year - int(rez)) == self.stolder:
                        self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
            
                elif int(self.now.year - int(rez)) == self.stolder:
                    self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
   
        except Exception as error:
            print(error)

      
    #---------------------------------------------------------------------------------------------
    def off(self, lists):    # Метод поиска всех пользователей сообщества
        try:
            if self.sex == "Женский":
                gender = lists["sex"]
                if gender == 1:
                    self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
            
            elif self.sex == "Мужской":
                gender = lists["sex"]
                if gender == 2:
                    self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
            
            else:
                self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
        
        except Exception as error:
            print(error)


    #---------------------------------------------------------------------------------------------
    def on(self, lists):     # Метод поиска пользователей сообщества онлайн
        try: 
            if self.sex == "Женский":
                gender = lists["sex"]
                if gender == 1 and lists["online"] == 1:
                    self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
            
            elif self.sex == "Мужской":
                gender = lists["sex"]
                if gender == 2 and lists["online"] == 1:
                    self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
            
            elif lists["online"] == 1:
                self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
       
        except Exception as error:
            print(error)
            
    
    #---------------------------------------------------------------------------------------------
    def open_dial(self, lists):    # Метод поиска пользователей с открытыми сообщениями
        try: 
            if self.sex == "Женский":
                gender = lists["sex"]
                if gender == 1 and lists["can_write_private_message"] == 1:
                    self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
            
            elif self.sex == "Мужской":
                gender = lists["sex"]
                if gender == 2 and lists["can_write_private_message"] == 1:
                    self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
            
            elif lists["can_write_private_message"] == 1:
                self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
       
        except Exception as error:
            print(error)
 
 
    #---------------------------------------------------------------------------------------------
    def on_open_dial(self, lists):    # Метод поиска пользователей сообщества онлайн с открытыми сообщениями
        try: 
            if self.sex == "Женский":
                gender = lists["sex"]
                if gender == 1 and lists["can_write_private_message"] == 1 and lists["online"] == 1:
                    self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
            
            elif self.sex == "Мужской":
                gender = lists["sex"]
                if gender == 2 and lists["can_write_private_message"] == 1 and lists["online"] == 1:
                    self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
            
            elif lists["can_write_private_message"] == 1 and lists["online"] == 1:
                self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
       
        except Exception as error:
            print(error)
 

    #---------------------------------------------------------------------------------------------
    def on_old(self, lists):    # Метод поиска пользователей сообщества  по возрасту и онлайн
        try: 
            add_date = str(lists["bdate"])

            if len(add_date) >= 4 and add_date[-4:].isdigit():
                rez = add_date[-4:]
                
                if self.sex == "Женский":
                    gender = lists["sex"]
                    if gender == 1 and int(self.now.year - int(rez)) == self.stolder and lists["online"] == 1:
                        self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
            
                elif self.sex == "Мужской":
                    gender = lists["sex"]
                    if gender == 2 and int(self.now.year - int(rez)) == self.stolder and lists["online"] == 1:
                        self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
            
                elif int(self.now.year - int(rez)) == self.stolder and lists["online"] == 1:
                    self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
   
        except Exception as error:
            print(error)


    #---------------------------------------------------------------------------------------------
    def old_dial(self, lists):    # Метод поиска пользователей сообщества  по возрасту и открытым диалогам
        try: 
            add_date = str(lists["bdate"])

            if len(add_date) >= 4 and add_date[-4:].isdigit():
                rez = add_date[-4:]
                
                if self.sex == "Женский":
                    gender = lists["sex"]
                    if gender == 1 and int(self.now.year - int(rez)) == self.stolder and lists["can_write_private_message"] == 1:
                        self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
            
                elif self.sex == "Мужской":
                    gender = lists["sex"]
                    if gender == 2 and int(self.now.year - int(rez)) == self.stolder and lists["can_write_private_message"] == 1:
                        self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
            
                elif int(self.now.year - int(rez)) == self.stolder and lists["can_write_private_message"] == 1:
                    self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
   
        except Exception as error:
            print(error)


    #---------------------------------------------------------------------------------------------
    def on_old_open_dial(self, lists):    # Метод поиска пользователей сообщества  по всем  параметрам
        try: 
            add_date = str(lists["bdate"])

            if len(add_date) >= 4 and add_date[-4:].isdigit():
                rez = add_date[-4:]
                
                if self.sex == "Женский":
                    gender = lists["sex"]
                    if gender == 1 and int(self.now.year - int(rez)) == self.stolder and lists["can_write_private_message"] == 1 and lists["online"] == 1:
                        self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
            
                elif self.sex == "Мужской":
                    gender = lists["sex"]
                    if gender == 2 and int(self.now.year - int(rez)) == self.stolder and lists["can_write_private_message"] == 1 and lists["online"] == 1:
                        self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
            
                elif int(self.now.year - int(rez)) == self.stolder and lists["can_write_private_message"] == 1 and lists["online"] == 1:
                    self.length.emit(str(lists["id"]), str(lists["first_name"]), str(lists["last_name"]), str(lists["bdate"]), str(lists["online"]), str(lists["can_write_private_message"]))
   
        except Exception as error:
            print(error)

 
