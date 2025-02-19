from gpiozero import LED, Button
import signal
import sys
from time import sleep
from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator
from luma.oled.device import ssd1306
from luma.core.interface.serial import i2c

led = LED(23)
button = Button(24)

def buttonPressHandler():
    print("BUTTON PRESS")

button.when_released =buttonPressHandler 

def keyboardInterruptHandler(sig, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, keyboardInterruptHandler)

serial = i2c(port=1, address=0x3c)
device = ssd1306(serial)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
    with canvas(device, dither=True) as draw:
        #fill, outline = "black", "white"
        textLines = ["Actual Speed(mph): ", "Speed Limit(mph): ", "Target Speed(mph): ", "Input Speed(mph): ", "Authority(ft): ", "Power Out(W): "]
        dataLines = [33, 50, 40, 20, 4000, 4000.12]
        for i in range(len(textLines)):
            draw.text((2,i*10), textLines[i] + str(dataLines[i]))

