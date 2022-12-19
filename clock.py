from msilib.schema import Error
from tkinter import *
from time import *
import threading



class Clock:
    def __init__(self, startTime, timeString, timeStillLeft, win) -> None: # startTime is in demiSeconds
        self.__currentTimeInDemiSec = startTime
        self.__timeString = timeString # timeString in StringVar()
        self.__timeString.set(self.__getTimeInString())
        self.__started = False
        self.__win = win
        self.__timeStillLeft = timeStillLeft

    def start(self):
        self.__started = True
        self.__decrement()

    def __decrement(self):
        if self.__currentTimeInDemiSec == -1:
            self.__timeStillLeft.set(False)
        if self.__timeStillLeft.get() and self.__started:
            newTime = self.__getTimeInString()
            self.__timeString.set(newTime)
            self.__currentTimeInDemiSec -= 1
            self.__win.after(10, self.__decrement)

    def stop(self):
        self.__started = False

    def __getTimeInString(self): #time is in demi seconds
        hrs = str(self.__currentTimeInDemiSec//36000)
        mins = str((self.__currentTimeInDemiSec%36000)//600)
        sec = str((self.__currentTimeInDemiSec%600)//60)
        if len(hrs) == 1:
            hrs="0"+hrs
        if len(mins) == 1:
            mins="0"+mins
        if len(sec) == 1:
            sec="0"+sec
        if self.__currentTimeInDemiSec <= 1500:
            centiSec = str(self.__currentTimeInDemiSec%60)
            if len(centiSec) == 1:
                centiSec="0"+centiSec
            return ":".join([hrs, mins, sec, centiSec])
        return ":".join([hrs, mins, sec])

"""
    def getTimeInDemiSec(timeString):
        t = timeString.get().split(":")
        hrs, mins, sec = int(t[0]), int(t[1]), int(t[2])
        if len(t) == 4:
            centiSec = int(t[3])
            return hrs*360000+mins*6000+sec*100+centiSec
        return hrs*360000+mins*6000+sec*100
"""
