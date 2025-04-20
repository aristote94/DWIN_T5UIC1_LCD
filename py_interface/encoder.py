import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class Encoder:

    def __init__(self, leftPin, rightPin, callback=None):
        self.leftPin = leftPin
        self.rightPin = rightPin
        self.value = 0
        self.state = '00'
        self.direction = None
        self.callback = callback

        GPIO.cleanup([self.leftPin, self.rightPin])  # nettoyage ciblé
        GPIO.setup(self.leftPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.rightPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.leftPin, GPIO.BOTH, callback=self.transitionOccurred)
        GPIO.add_event_detect(self.rightPin, GPIO.BOTH, callback=self.transitionOccurred)

    def transitionOccurred(self, channel):
        p1 = GPIO.input(self.leftPin)
        p2 = GPIO.input(self.rightPin)
        newState = f"{p1}{p2}"

        if self.state == "00":
            if newState == "01":
                self.direction = "R"
            elif newState == "10":
                self.direction = "L"
        elif self.state == "01":
            if newState == "11":
                self.direction = "R"
            elif newState == "00" and self.direction == "L":
                self.value -= 1
                if self.callback:
                    self.callback(self.value)
        elif self.state == "10":
            if newState == "11":
                self.direction = "L"
            elif newState == "00" and self.direction == "R":
                self.value += 1
                if self.callback:
                    self.callback(self.value)
        elif self.state == "11":
            if newState == "01":
                self.direction = "L"
            elif newState == "10":
                self.direction = "R"
            elif newState == "00":
                if self.direction == "L":
                    self.value -= 1
                    if self.callback:
                        self.callback(self.value)
                elif self.direction == "R":
                    self.value += 1
                    if self.callback:
                        self.callback(self.value)

        self.state = newState

    def getValue(self):
        return self.value
