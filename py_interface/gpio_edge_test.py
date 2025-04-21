import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()

PIN1 = 19
PIN2 = 26

GPIO.setup(PIN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def cb(ch):
    print(f"💡 Changement détecté sur GPIO {ch}")

try:
    GPIO.add_event_detect(PIN1, GPIO.BOTH, callback=cb)
    GPIO.add_event_detect(PIN2, GPIO.BOTH, callback=cb)
    print("✅ GPIO prêts. Tourne l’encodeur ou fais contact.")
except RuntimeError as e:
    print(f"❌ ERREUR: {e}")
    exit(1)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Nettoyage...")
    GPIO.cleanup()
