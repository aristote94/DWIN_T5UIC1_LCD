import time
from dwinlcd import DWIN_LCD

UART_PORT = "/dev/ttyS0"  # Vérifie que c'est bien le bon port UART

print("[BOOT] Initialisation de l’écran DWIN...")
DWINLCD = DWIN_LCD(
    USARTx=UART_PORT,
    encoder_pins=(19, 26),       # encore requis par la signature, mais ignoré
    button_pin=21,
    octoPrint_API_Key="TEST"
)

print("[RUNNING] Envoi test écran : fond noir, ligne, cercle...")
try:
    DWINLCD.Frame_Clear(DWINLCD.Color_Bg_Black)
    DWINLCD.Draw_Line(DWINLCD.Color_Yellow, 0, 0, 271, 479)
    DWINLCD.Draw_Circle(DWINLCD.Color_Bg_Red, 136, 240, 50)
    DWINLCD.UpdateLCD()
    print("[OK] Affichage envoyé à l’écran.")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n[EXIT] Interruption clavier. Fin du test.")
