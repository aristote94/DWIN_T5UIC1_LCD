import time
import multitimer
import atexit

from RPi import GPIO
from DWIN_Screen import T5UIC1_LCD


def current_milli_time():
    return round(time.time() * 1000)


class DWIN_LCD:
    # Constants and variables
    TROWS = 6
    MROWS = TROWS - 1
    TITLE_HEIGHT = 30
    MLINE = 53
    LBLX = 60
    MENU_CHR_W = 8
    STAT_CHR_W = 10

    dwin_abort_flag = False

    MSG_STOP_PRINT = "Stop Print"
    MSG_PAUSE_PRINT = "Pausing..."

    DWIN_SCROLL_UP = 2
    DWIN_SCROLL_DOWN = 3

    select_page = 0

    ENCODER_DIFF_NO = 0
    ENCODER_DIFF_CW = 1
    ENCODER_DIFF_CCW = 2
    ENCODER_DIFF_ENTER = 3
    ENCODER_WAIT = 80
    ENCODER_WAIT_ENTER = 300
    EncoderRateLimit = True

    ICON = 0x09
    ICON_LOGO = 0
    ICON_Print_0 = 1
    ICON_Print_1 = 2
    ICON_Prepare_0 = 3
    ICON_Prepare_1 = 4
    ICON_Control_0 = 5
    ICON_Control_1 = 6
    ICON_Info_0 = 90
    ICON_Info_1 = 91

    def __init__(self, USARTx):
        GPIO.setmode(GPIO.BCM)
        self.EncodeLast = 0
        self.EncodeMS = current_milli_time() + self.ENCODER_WAIT
        self.EncodeEnter = current_milli_time() + self.ENCODER_WAIT_ENTER
        self.next_rts_update_ms = 0
        self.last_cardpercentValue = 101
        self.lcd = T5UIC1_LCD(USARTx)
#        self.checkkey = self.MainMenu
        self.timer = multitimer.MultiTimer(interval=2, function=self.EachMomentUpdate)
#        self.HMI_ShowBoot()
        print("Boot looks good")
#       self.HMI_Init()
#       self.HMI_StartFrame(False)

    def EachMomentUpdate(self):
        update = False
        if update:
            self.Draw_Status_Area(update)
        self.lcd.UpdateLCD()

    def HMI_StartFrame(self, with_update):
        self.last_status = "standby"
        self.Goto_MainMenu()
        self.Draw_Status_Area(with_update)

    def Goto_MainMenu(self):
        self.checkkey = self.MainMenu
        self.Clear_Main_Window()
        self.lcd.Frame_AreaCopy(1, 0, 2, 39, 12, 14, 9)
        self.lcd.ICON_Show(self.ICON, self.ICON_LOGO, 71, 52)
        self.ICON_Print()
        self.ICON_Prepare()
        self.ICON_Control()
        self.ICON_StartInfo(self.select_page == 3)

    def Clear_Main_Window(self):
        self.lcd.Draw_Rectangle(1, self.lcd.Color_Bg_Blue, 0, 0, self.lcd.DWIN_WIDTH, 30)
        self.lcd.Draw_Rectangle(1, self.lcd.Color_Bg_Black, 0, 31, self.lcd.DWIN_WIDTH, self.STATUS_Y)

    def ICON_Print(self):
        if self.select_page == 0:
            self.lcd.ICON_Show(self.ICON, self.ICON_Print_1, 17, 130)
            self.lcd.Draw_Rectangle(0, self.lcd.Color_White, 17, 130, 126, 229)
            self.lcd.Frame_AreaCopy(1, 1, 451, 31, 463, 57, 201)
        else:
            self.lcd.ICON_Show(self.ICON, self.ICON_Print_0, 17, 130)
            self.lcd.Frame_AreaCopy(1, 1, 423, 31, 435, 57, 201)

    def ICON_Prepare(self):
        if self.select_page == 1:
            self.lcd.ICON_Show(self.ICON, self.ICON_Prepare_1, 145, 130)
            self.lcd.Draw_Rectangle(0, self.lcd.Color_White, 145, 130, 254, 229)
            self.lcd.Frame_AreaCopy(1, 33, 451, 82, 466, 175, 201)
        else:
            self.lcd.ICON_Show(self.ICON, self.ICON_Prepare_0, 145, 130)
            self.lcd.Frame_AreaCopy(1, 33, 423, 82, 438, 175, 201)

    def ICON_Control(self):
        if self.select_page == 2:
            self.lcd.ICON_Show(self.ICON, self.ICON_Control_1, 17, 246)
            self.lcd.Draw_Rectangle(0, self.lcd.Color_White, 17, 246, 126, 345)
            self.lcd.Frame_AreaCopy(1, 85, 451, 132, 463, 48, 318)
        else:
            self.lcd.ICON_Show(self.ICON, self.ICON_Control_0, 17, 246)
            self.lcd.Frame_AreaCopy(1, 85, 423, 132, 434, 48, 318)

    def ICON_StartInfo(self, show):
        if show:
            self.lcd.ICON_Show(self.ICON, self.ICON_Info_1, 145, 246)
            self.lcd.Draw_Rectangle(0, self.lcd.Color_White, 145, 246, 254, 345)
            self.lcd.Frame_AreaCopy(1, 132, 451, 159, 466, 186, 318)
        else:
            self.lcd.ICON_Show(self.ICON, self.ICON_Info_0, 145, 246)
            self.lcd.Frame_AreaCopy(1, 132, 423, 159, 435, 186, 318)
