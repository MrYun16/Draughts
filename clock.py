from msilib.schema import Error
from tkinter import *
from time import *
import threading



class Clock:
    def __init__(self, startTime, clockDisplayString, win) -> None: # startTime is in demiSeconds
        if startTime == -1:
            self.__clockDisplayString = clockDisplayString
            self.__clockDisplayString.set("           ")
            self.__beingUsed = False # user has decided to turn on/off timers in settings
            self.__timeLeft = BooleanVar()
            self.__timeLeft.set(True)
        else:
            self.__currentTimeInDemiSec = startTime
            self.__clockDisplayString = clockDisplayString # clockDisplayString in StringVar()
            self.__clockDisplayString.set(self.__getTimeInString())
            self.__started = False
            self.__win = win
            self.__timeLeft = BooleanVar()
            self.__timeLeft.set(True)
            self.__beingUsed = True

    @property
    def clockDisplayString(self):
        return self.__clockDisplayString

    @property
    def currentTimeInDemiSec(self):
        return self.__currentTimeInDemiSec

    @property
    def started(self):
        return self.__started

    @property
    def timeLeft(self):
        return self.__timeLeft

    def start(self):
        if self.__beingUsed:
            self.__started = True
            self.__decrement()

    def __decrement(self):
        if self.__currentTimeInDemiSec == -1:
            self.__timeLeft.set(False)
            return
        if self.__started:
            newTime = self.__getTimeInString()
            self.__clockDisplayString.set(newTime)
            self.__currentTimeInDemiSec -= 1
            self.__win.after(10, self.__decrement)

    def stop(self):
        if self.__beingUsed:
            self.__started = False

    def __getTimeInString(self): #time is in demi seconds
        hrs = str(self.__currentTimeInDemiSec//216000)
        mins = str((self.__currentTimeInDemiSec%216000)//3600)
        sec = str((self.__currentTimeInDemiSec%3600)//60)
        if len(hrs) == 1:
            hrs="0"+hrs
        if len(mins) == 1:
            mins="0"+mins
        if len(sec) == 1:
            sec="0"+sec
        if self.__currentTimeInDemiSec <= 900:
            centiSec = str(self.__currentTimeInDemiSec%60)
            if len(centiSec) == 1:
                centiSec="0"+centiSec
            return ":".join([hrs, mins, sec, centiSec])
        return ":".join([hrs, mins, sec])

