import Modules
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

class Box:
    def __init__(self, bx, debounceTime):
        self.bx = bx-1
        self.debounceTime = debounceTime
        GPIO.setup(Modules.Box[self.bx, 3], GPIO.OUT)
        GPIO.setup(Modules.Box[self.bx, 4], GPIO.OUT)
        GPIO.setup(Modules.Box[self.bx, 5], GPIO.OUT)
        GPIO.setup(Modules.Box[self.bx, 6], GPIO.OUT)
        GPIO.setup(Modules.Box[self.bx, 7], GPIO.OUT)
        GPIO.setup(Modules.Box[self.bx, 8], GPIO.OUT)

        GPIO.output(Modules.Box[self.bx, 3], 0)
        GPIO.output(Modules.Box[self.bx, 4], 0)
        GPIO.output(Modules.Box[self.bx, 5], 0)
        GPIO.output(Modules.Box[self.bx, 6], 0)
        GPIO.output(Modules.Box[self.bx, 7], 0)
        GPIO.output(Modules.Box[self.bx, 8], 0)

        GPIO.setup(Modules.Box[self.bx, 0], GPIO.IN)
        GPIO.setup(Modules.Box[self.bx, 1], GPIO.IN)
        GPIO.setup(Modules.Box[self.bx, 2], GPIO.IN)

        self.rightDebounce = self.currentTimeMs()
        self.leftDebounce = self.currentTimeMs()
        self.noseDebounce = self.currentTimeMs()

        self.rightPalet = 0
        self.leftPalet = 0

    def startSession(self):
        GPIO.output(Modules.Box[self.bx, 3], 1)
        GPIO.output(Modules.Box[self.bx, 4], 1)
        GPIO.output(Modules.Box[self.bx, 7], 1)

    def stopSession(self):
        GPIO.output(Modules.Box[self.bx, 3], 0)
        GPIO.output(Modules.Box[self.bx, 4], 0)
        GPIO.output(Modules.Box[self.bx, 7], 0)

    def setRightLeverResponse(self):
        if((int(self.currentTimeMs()) - int(self.rightDebounce)) > int(self.debounceTime)):
            self.rightDebounce = self.currentTimeMs()
            self.rightPalet += 1

    def setLeftLeverResponse(self):
        if((int(self.currentTimeMs()) - int(self.leftDebounce)) > int(self.debounceTime)):
            self.leftDebounce = self.currentTimeMs()
            self.leftPalet += 1

    def getRightLeverResponse(self):
        return self.rightPalet

    def getLeftLeverResponse(self):
        return self.leftPalet

    def getNosePoke(self):
        if((int(self.currentTimeMs()) - int(self.noseDebounce)) > int(self.debounceTime)):
            if (GPIO.input(Modules.Box[self.bx, 2]) == 0):
                return 1
                self.noseDebounce = self.currentTimeMs()
            else: return 0
        else: return 0

    def rightStimulusLightOn(self):
        GPIO.output(Modules.Box[self.bx, 5], 1)

    def rightStimulusLightOff(self):
        GPIO.output(Modules.Box[self.bx, 5], 0)

    def leftStimulusLightOn(self):
        GPIO.output(Modules.Box[self.bx, 6], 1)

    def leftStimulusLightOff(self):
        GPIO.output(Modules.Box[self.bx, 6], 0)

    def sendReward(self):
        GPIO.output(Modules.Box[0, 8], 0)
        GPIO.output(Modules.Box[0, 8], 1)
        time.sleep(1)
        GPIO.output(Modules.Box[0, 8], 0)

    def currentTimeMs(self):
        return int(round(time.time() * 1000))