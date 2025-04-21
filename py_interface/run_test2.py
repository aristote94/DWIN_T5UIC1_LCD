import time
from dwinlcd import DWIN_LCD

# Port série connecté à l'écran
UART_PORT = "/dev/ttyS0"  # ou /dev/serial0 si alias activé

print("[BOOT] Initialisation de l’écran DWIN...")
DWINLCD = DWIN_LCD(UART_PORT)

print("[RUNNING] Test : fond noir + ligne diagonale + cercle rouge...")
try:
    DWINLCD.lcd.Frame_Clear(DWINLCD.lcd.Color_Bg_Black)
    DWINLCD.lcd.Draw_Line(DWINLCD.lcd.Color_Yellow, 0, 0,241, 50)
    DWINLCD.lcd.Draw_Circle(DWINLCD.lcd.Color_Bg_Red, 136, 240, 50)
    DWINLCD.lcd.UpdateLCD()
    print("[OK] Affichage envoyé.")

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n[EXIT] Ctrl+C détecté. Fin propre.")
