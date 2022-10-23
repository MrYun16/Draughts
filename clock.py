from msilib.schema import Error
from tkinter import *
from time import *
import threading
class TimeError(Exception):
    pass

class Timer(threading.Thread):
    def __init__(self, initialTimeInSec, timeString) -> None:
        threading.Thread.__init__(self)
        self.timeString = timeString
        self.currentTime = initialTimeInSec
        newHr, newMins, newSec = self.getHrMinSec(self.currentTime)
        self.updateVariables(newHr, newMins, newSec)
    def run(self):
       
        while self.currentTime > 0:
            #print(self.currentTime)
            sleep(1)
            newHr, newMins, newSec = self.getHrMinSec(self.currentTime)
            self.updateVariables(newHr, newMins, newSec)
            self.currentTime -= 1
        
    def updateTimeVar(self, newHr, newMins, newSec):
        time = [newHr, newMins, newSec]
        for i, unit in enumerate(time):
            if unit <= 9:
                time[i] = "0"+str(unit)
            else:
                time[i] = str(time[i])
        self.timeString.set(":".join(time))

    def getHrMinSec(self, time):
        hr, mins, sec = time//3600, (time%3600)//60, (time%3600)%60
        return hr, mins, sec 

    def join(self):
        threading.Thread.join(self)
        raise TimeError("Ran out of time")

timer = Timer(1)
timer.start()
try:
    timer.join()
except TimeError as e:
    print(e)

