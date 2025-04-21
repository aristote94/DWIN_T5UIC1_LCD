import RPi.GPIO as GPIO
import time

PIN1 = 19
PIN2 = 26

# 🔧 CONFIGURATION STRICTE
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)         # 📌 DÉFINIR LE MODE EN PREMIER
GPIO.cleanup([PIN1, PIN2])     # Nettoyage des pins spécifiques, pas tout le système

# 🔌 SETUP
GPIO.setup(PIN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 📡 CALLBACK
def cb(ch):
    print(f"💡 Changement détecté sur GPIO {ch}")

# ⚙️ ÉVÉNEMENTS
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

