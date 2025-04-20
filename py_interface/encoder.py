# encoder.py — version robuste

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Encoder:
    def __init__(self, leftPin, rightPin, callback=None):
        self.leftPin = leftPin
        self.rightPin = rightPin
        self.value = 0
        self.state = '00'
        self.direction = None
        self.callback = callback

        GPIO.setup(self.leftPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.rightPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        try:
            GPIO.remove_event_detect(self.leftPin)
            GPIO.remove_event_detect(self.rightPin)
        except RuntimeError:
            pass  # Aucun événement précédent, c’est normal au premier lancement

        try:
            GPIO.add_event_detect(self.leftPin, GPIO.BOTH, callback=self.transitionOccurred)
            GPIO.add_event_detect(self.rightPin, GPIO.BOTH, callback=self.transitionOccurred)
        except RuntimeError as e:
            print(f"[ERROR] Impossible d'ajouter une détection sur les pins GPIO {self.leftPin}/{self.rightPin} : {e}")
            print("🔧 Vérifie que ces broches ne sont pas déjà utilisées ou que ton script ne tourne pas déjà ailleurs.")
            raise

    def transitionOccurred(self, channel):
        p1 = GPIO.input(self.leftPin)
        p2 = GPIO.input(self.rightPin)
        newState = "{}{}".format(p1, p2)

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
