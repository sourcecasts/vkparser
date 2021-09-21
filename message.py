
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject
from time import sleep

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import datetime
import time
import threading 

class Message(QObject):    # Основной класс...
    
    message_length = QtCore.pyqtSignal(str, str, str)
    
    def __init__(self, token, users, message):    # Основной класс...
        super().__init__()

        self.token = token
        self.users = users
        self.message = message

    def running(self): #Метод отправки сообщений...
 
            with  open(self.token, encoding = 'iso-8859-1') as file_token:
                    with  open(self.users, encoding = 'iso-8859-1') as file_users:
                        self.spam = file_token.readlines()

                        for i in self.spam:
                            self.id = file_users.readline()
                            self.vk_session = VkApi(token = i.strip())
                            self.vk = self.vk_session.get_api()

                            if self.vk is not None:
                                call = self.vk.messages.send(user_id = int(self.id), random_id = get_random_id(), message = self.message)
                                self.message_length.emit(str(call), str(self.id), str("Отправлено"))

                                print(call)
                            else:
                                print("Собщение не отправлено")