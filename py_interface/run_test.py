import time
from RPi import GPIO

from dwinlcd import DWIN_LCD
from printerInterface import PrinterData
from encoder import Encoder

# === CONFIGURATION GPIO ===
ENCODER_PINS = (19, 26)       # GPIO BCM, 19 = PIN 35 / 26 = PIN 37
BUTTON_PIN = 21               # À adapter selon ton câblage
UART_PORT = "/dev/ttyS0"      # Port série pour l'écran DWIN (à adapter si besoin)
OCTOPRINT_API_KEY = "your_api_key_here"  # Remplace par ta clé API

# === INITIALISATION GPIO GLOBALE ===
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup([*ENCODER_PINS, BUTTON_PIN])

# === CALLBACK EXEMPLE POUR L’ENCODEUR ===
def on_encoder_change(value):
    print(f"[ENCODEUR] Nouvelle valeur : {value}")
    # Ici, tu pourrais appeler une fonction d'interface pour mettre à jour l'écran par exemple

# === LANCEMENT DES OBJETS PRINCIPAUX ===
print("[BOOT] Initialisation des objets...")
#printer_data = PrinterData(API_Key=OCTOPRINT_API_KEY)

DWINLCD = DWIN_LCD(
    USARTx=UART_PORT,
#    encoder_pins=ENCODER_PINS,
#    button_pin=BUTTON_PIN,
 #   octoPrint_API_Key=OCTOPRINT_API_KEY
)

# L’encodeur est initialisé ici séparément si tu veux faire des tests indépendants
encoder = Encoder(ENCODER_PINS[0], ENCODER_PINS[1], callback=on_encoder_change)

# === BOUCLE PRINCIPALE ===
print("[RUNNING] Interface lancée. Appuie sur Ctrl+C pour quitter.")
try:
    while True:
        # Tu peux lire des données de l’écran, de l’imprimante, mettre à jour l’affichage, etc.
        time.sleep(0.1)  # Simulation de boucle de polling/affichage

except KeyboardInterrupt:
    print("\n[EXIT] Interruption clavier. Nettoyage...")
finally:
    GPIO.cleanup()
    print("[EXIT] GPIO nettoyés. Fermeture propre.")
