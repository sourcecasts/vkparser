# -*- coding: utf-8 -*-

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

class Repost(QObject):    # Основной класс...
    
    repost_length = QtCore.pyqtSignal(str, str, str, str)
    
    def __init__(self, token, wall):    # Основной класс...
        super().__init__()

        self.token = token
        self.wall = wall


    def running(self): #Метод отправки сообщений...
 
            with  open(self.token, encoding = 'iso-8859-1') as file_token:
                    self.spam = file_token.readlines()

                    for i in self.spam:
                        self.vk_session = VkApi(token = i.strip())
                        self.vk = self.vk_session.get_api()

                        if self.vk is not None:
                            call = self.vk.wall.repost(object = self.wall)
                            self.repost_length.emit(str(call["post_id"]), str(call["reposts_count"]), str(call["likes_count"]), str("Готово"))

                            print(call)
                        else:
                            print("Репост не выполнен")