import RPi.GPIO as GPIO
import time

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

        print(f"[INIT] Encoder pins: left={self.leftPin}, right={self.rightPin}")
        GPIO.cleanup()  # nettoyage complet avant config

        GPIO.setup(self.leftPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.rightPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        try:
            GPIO.remove_event_detect(self.leftPin)
            GPIO.remove_event_detect(self.rightPin)
        except RuntimeError:
            pass  # ok si rien n’était défini avant

        try:
            GPIO.add_event_detect(self.leftPin, GPIO.BOTH, callback=self.transitionOccurred)
            GPIO.add_event_detect(self.rightPin, GPIO.BOTH, callback=self.transitionOccurred)
            print("[OK] Interruption ajoutée avec succès sur les deux pins")
        except RuntimeError as e:
            print(f"[ERREUR] Impossible d’ajouter les événements sur GPIO {self.leftPin}/{self.rightPin} : {e}")
            print("👉 Vérifie que rien d'autre n'utilise ces pins ou que le script n’est pas déjà en cours")
            raise

    def transitionOccurred(self, channel):
        p1 = GPIO.input(self.leftPin)
        p2 = GPIO.input(self.rightPin)
        newState = f"{p1}{p2}"
        print(f"[ÉVÉNEMENT] GPIO {channel} — État : {self.state} → {newState}")

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
