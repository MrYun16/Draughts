from msilib.schema import Error
from tkinter import *
from time import *
import threading



class Clock:
    def __init__(self, startTime, timeString, win) -> None: # startTime is in demiSeconds
        print("initialised")
        self.__timeString = timeString # timeString in StringVar()
        self.__timeString.set(startTime)
        self.__currentTimeInDemiSec = startTime
        self.__win = win
        self.__notStopped = True

    def start(self):
        self.decrement()


    def decrement(self):
        if self.__currentTimeInDemiSec == 0:
            raise Exception("im bad")
        if self.__notStopped:
            newTime = self.getTimeInString()
            self.__timeString.set(newTime)
            self.__currentTimeInDemiSec -= 1
            self.__win.after(10, self.decrement)

    def stop(self):
        self.__notStopped = False

    

    def getTimeInString(self): #time is in centi seconds
        hrs = str(self.__currentTimeInDemiSec//360000)
        mins = str((self.__currentTimeInDemiSec%360000)//6000)
        sec = str((self.__currentTimeInDemiSec%6000)//100)
        if len(hrs) == 1:
            hrs="0"+hrs
        if len(mins) == 1:
            mins="0"+mins
        if len(sec) == 1:
            sec="0"+sec
        if self.__currentTimeInDemiSec <= 1500:
            centiSec = str(self.__currentTimeInDemiSec%100)
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
