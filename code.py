# 
# Wio Terminal HVAC DeltaT Monitor with LoRa
# SPDX-FileCopyrightText: Copyright (c) 2020 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Jeremy Behrle for fun
# SPDX-License-Identifier: MIT

import time
import board
import busio
import displayio
from adafruit_display_shapes.rect import Rect
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
import terminalio  # Ensure this is imported for fallback
import adafruit_sht4x
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20

# ===========================
# Configuration Section
# ===========================
APPKEY = "YOUR_APPKEY_FOR_TTN"  # LoRaWAN Application Key The Things Network
HEADER_TEXT = "YOUR_ROOM_NAME"  # Header text for the display
# ===========================

# Let's get it started
print("")
print("*** Start HVAC DeltaT Monitor ***")

# Setup SleepTimer and timestamp
DisplaySleepTime = 5
SendSleepTime = 30
timestamp = 0
is_join = False

# Room Temp Sensor Setup
sht = adafruit_sht4x.SHT4x(board.I2C())
print("Found SHT4x with serial number", hex(sht.serial_number))
sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
# Can also set the mode to enable heater
# sht.mode = adafruit_sht4x.Mode.LOWHEAT_100MS
print("Current SHT4x mode is: ", adafruit_sht4x.Mode.string[sht.mode])

# Dallas One Wire
# Dallas data wire is plugged into port D1 on the Wio Terminal
# You'll want to mount these sensors in the corret order for the math to work

print("*** Start Dallas One Wire  ***")
ow_bus = OneWireBus(board.D1)

devices = ow_bus.scan()
for device in devices:
    print("ROM = {} \tFamily = 0x{:02x}".format([hex(i) for i in device.rom], device.family_code))

ds18a = DS18X20(ow_bus, ow_bus.scan()[0])
ds18b = DS18X20(ow_bus, ow_bus.scan()[1])

# Set UART Pin BACKWARDS to connect to the LoRa-E5 + GNSS Wio Module
uart = busio.UART(tx=board.RX, rx=board.TX, baudrate=9600)
get_input = True
message_started = False
message_print = []
allstring = ""
printshow = False

def at_send_check_response(p_ack, timeout, p_cmd):
    b = bytes(p_cmd, 'utf-8')
    print(p_ack)
    print(b)
    uart.write(b)
    # delay(200)
    DELAY_DURATION = timeout
    LAST_TIME = 0
    now = time.monotonic()
    condition = True
    allstring = ""
    while condition:
        byte_read = uart.readline()  # read one line
        if byte_read is not None:
            allstring += byte_read.decode()
            printshow = True
        else:
            if printshow == True:
                if allstring != "":
                    print(allstring)
                allstring = ""
                printshow = False
        condition = time.monotonic() - now < timeout
    return 0

print("*** Talking TTN LoRa ***")
at_send_check_response("AT", 2, "AT")
at_send_check_response("AT+ID", 3, "AT+ID")
at_send_check_response("Set AT+MODE=LWOTAA", 2, "AT+MODE=LWOTAA")
# at_send_check_response("Set AT+DR=US915,DR1,SF9,BW125K",2,"AT+DR=US915,DR1,SF9,BW125K") # US915
at_send_check_response("Set AT+DR=US915", 2, "AT+DR=US915")  # US915
at_send_check_response("Set AT+DR=DR1", 2, "AT+DR=DR1")    # Need more than 11 bytes
at_send_check_response("Set AT+CH=NUM,8-15", 2, "Set AT+CH=NUM,8-15")  # FSB2
at_send_check_response("Set AT+APPKEY", 2, f"AT+KEY=APPKEY {APPKEY}")  # Use APPKEY variable
at_send_check_response("Set AT+CLASS=C", 2, "AT+CLASS=C")
at_send_check_response("Set AT+PORT=8", 2, "AT+PORT=8")
at_send_check_response("Set AT+JOIN", 10, "AT+JOIN")
is_join = True
print("*** TTN LoRaWAN Successfully Started ***")

# Starting Wio Terminal Display
splash = displayio.Group()
board.DISPLAY.show(splash)

# Create Four Rectangles
rect = Rect(0, 0, 320, 59, fill=0x00FFFF, outline=0x777777, stroke=2)
rect2 = Rect(0, 60, 320, 59, fill=0x000000, outline=0x777777, stroke=2)
rect3 = Rect(0, 120, 320, 59, fill=0x000000, outline=0x777777, stroke=2)
rect4 = Rect(0, 180, 320, 59, fill=0x000000, outline=0x777777, stroke=2)

# Show Those Four Rectangles
splash.append(rect)
splash.append(rect2)
splash.append(rect3)
splash.append(rect4)

# Create Display Text Objects For the Title / Header
text_area_x = 5
text_area_y = 30
try:
    font = bitmap_font.load_font("/font/Terminus24x24.bdf")  # Load custom font
except OSError:
    print("Error: Font file not found. Using built-in font instead.")
    font = terminalio.FONT  # Fallback to built-in font

Header_text_group = displayio.Group(x=text_area_x, y=text_area_y)
Header_label = label.Label(font, text=HEADER_TEXT, color=0x000000)  # Use HEADER_TEXT variable
Header_text_group.append(Header_label)

# Create Display Text Objects for Temp & RH in Utility Room
Room_text_group = displayio.Group(x=text_area_x, y=text_area_y + 55)
Room_text = "Room: 0°F 0%RH"
Room_label = label.Label(font, text=Room_text, color=0x00FFFF)
Room_text_group.append(Room_label)

# Create Display Text Objects to Show Return & Supply Temps
RtnSup_text_group = displayio.Group(x=text_area_x, y=text_area_y + 115)
RtnSup_text = "Rtn: 0° Sup: 0°"
RtnSup_label = label.Label(font, text=RtnSup_text, color=0x00FFFF)
RtnSup_text_group.append(RtnSup_label)

# Create Display Text Objects to Show DeltaT
DeltaT_Color = 0x00FFFF
DeltaT_text_group = displayio.Group(x=text_area_x + 60, y=text_area_y + 175)
DeltaT_text = "DeltaT: 0 °F"
DeltaT_label = label.Label(font, text=DeltaT_text, color=DeltaT_Color)
DeltaT_text_group.append(DeltaT_label)

# Show All Text Groups
splash.append(Header_text_group)
splash.append(Room_text_group)
splash.append(RtnSup_text_group)
splash.append(DeltaT_text_group)

# Mark the Start of the Program Loop
print("")
print("*** Entering Program Loop ***")

while True:
    if (time.monotonic() - timestamp) >= DisplaySleepTime:
        temperature, relative_humidity = sht.measurements
        tempF = round(temperature * 9 / 5 + 32, 1)
        print("Room: %0.1f°F %0.1f%% RH" % (tempF, relative_humidity))
        Room_label.text = f"Room: {int(tempF)}°F {int(relative_humidity)}%RH"
        
        DallasTempFa = round(ds18a.temperature * 9 / 5 + 32, 1)
        DallasTempFb = round(ds18b.temperature * 9 / 5 + 32, 1)
        TempDeltaF = round(DallasTempFb - DallasTempFa, 1)
        RtnSup_label.text = f"Rtn: {int(DallasTempFa)}° Sup: {int(DallasTempFb)}°"
        print("Rtn: %0.1f°F Sup: %0.1f°F" % (DallasTempFa, DallasTempFb))
        print("DeltaT: %0.1f°F" % (TempDeltaF))
        
        IntTempDeltaF = int(TempDeltaF)
        if -5 < IntTempDeltaF < 5:
            DeltaT_label.text = f"DeltaT: {IntTempDeltaF}°F"
            DeltaT_label.color = 0xFFFF00
            rect.fill = 0xFFFF00
        elif IntTempDeltaF >= 5:
            DeltaT_label.text = f"DeltaT: {IntTempDeltaF}°F"
            DeltaT_label.color = 0xFF0000
            rect.fill = 0xFF0000
        elif IntTempDeltaF <= -5:
            DeltaT_label.text = f"DeltaT: {IntTempDeltaF}°F"
            DeltaT_label.color = 0x0000FF
            rect.fill = 0x0000FF
        
        # Convert values to ints and then to hexadecimal
        tempUtilityRm = int(tempF * 10)
        RhUtilityRm = int(relative_humidity * 10)
        tempSupply = int(DallasTempFb * 10)
        tempReturn = int(DallasTempFa * 10)
        send_string = f"AT+CMSGHEX={tempUtilityRm:04x}{RhUtilityRm:04x}{tempSupply:04x}{tempReturn:04x}"
        at_send_check_response("Sending : ", SendSleepTime, send_string)
        
        timestamp = time.monotonic()
