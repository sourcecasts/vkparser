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

class Group(QObject):    # Main class...
    
    group_length = QtCore.pyqtSignal(str, str, str, str)
    
    def __init__(self, token, q):    #  Main class...
        super().__init__()

        self.token = token
        self.q = q

        self.vk_session = VkApi(token = self.token)
        self.vk = self.vk_session.get_api()
    
    def running(self): # Search process...
    
        resp = self.vk.groups.search(q = self.q, count = 100)        
        #print(resp)
        for lists in resp["items"]:
            print(lists["id"])
            self.group_length.emit(str(lists["id"]), str(lists["name"]), str(lists["type"]), str(lists["is_closed"]))

    
    