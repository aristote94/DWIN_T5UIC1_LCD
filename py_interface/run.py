import time
from RPi import GPIO
from dwinlcd import DWIN_LCD

GPIO.cleanup()
# === CONFIG UART ===
UART_PORT = "/dev/ttyS0"  # À adapter si besoin

# === CONFIG FACTICE POUR TEST LOCAL ===
ENCODER_PINS = (19, 26)     # Pins utilisés mais pas utilisés activement ici
BUTTON_PIN = 21             # À adapter si connecté, sinon fictif
FAKE_API_KEY = "test"

# === INIT GPIO ===
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup([*ENCODER_PINS, BUTTON_PIN])

# === INIT ÉCRAN DWIN ===
print("[BOOT] Initialisation de l’écran DWIN...")
DWINLCD = DWIN_LCD(
    USARTx=UART_PORT,
    encoder_pins=ENCODER_PINS,
    button_pin=BUTTON_PIN,
    octoPrint_API_Key=FAKE_API_KEY
)

# === TEST AFFICHAGE ===
print("[RUNNING] Test d’affichage : fond noir, ligne et cercle...")
try:
    DWINLCD.Frame_Clear(DWINLCD.Color_Bg_Black)
    DWINLCD.Draw_Line(DWINLCD.Color_Yellow, 0, 0, 271, 479)
    DWINLCD.Draw_Circle(DWINLCD.Color_Bg_Red, 136, 240, 50)
    DWINLCD.UpdateLCD()
    print("[OK] Affichage envoyé à l’écran.")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n[EXIT] Ctrl+C détecté. Fermeture propre.")
finally:
    GPIO.cleanup()
    print("[EXIT] GPIO libérés.")

