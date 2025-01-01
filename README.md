# Wio Terminal HVAC DeltaT Monitor with LoRa

Introduction

Bassed on the Seeed Wio Terminal, the HVAC DeltaT Monitor with LoRa is designed to monitor and display temperature and humidity data from multiple sensors. It leverages LoRaWAN via The Things Network for wireless communication, making it ideal for remote HVAC monitoring in difficult ultility rooms. The device displays real-time data on its built-in screen and (eventually) sends sensor readings to Adafruit IO for further analysis and long term trend analsis. 

Introduction

Based on Seeed Wio Terminal hardware, the HVAC DeltaT Monitor with LoRa is designed to monitor and display temperature and humidity data from multiple sensors. It leverages LoRaWAN via The Things Network for wireless communication, making it ideal for remote HVAC monitoring in difficult utility rooms. The device displays real-time data on its built-in screen and (eventually) sends sensor readings to Adafruit IO for further and long-term trend analysis. 

Features
Real-Time Monitoring: Displays room temperature, relative humidity, return and supply temperatures, and Delta Temperature (ΔT).
LoRaWAN Connectivity: Sends sensor data wirelessly over long distances using LoRa technology.
Multiple Sensors Support: Integrates SHT4x (temperature and humidity) and DS18X20 (temperature) sensors.

Hardware Requirements

  Seeed Wio Terminal ATSAMD51
  Seed Wio Terminal Chassis - Wio-E5
  Adafruit SHT4x, or compatible, Sensor
  DS18B20 Temperature Sensors (2 units)
  Grove & Grove to STEMMA QT (Qwiic) connector 
  Wires, Wago connectors, and USB-C Power Supply

Software Requirements

  CircuitPython 8.2.10
  Adafruit Libraries for CircuitPython
  adafruit_display_shapes
  adafruit_display_text
  adafruit_bitmap_font
  bitmap_font (for custom fonts)
  terminalio font
  and, dependencies 
  
Hardware Assembly

  SHT4x Sensor, via Wio's left Grove connector 
    VCC to 3.3V
    GND to GND
    SCL to SCL
    SDA to SDA
    
Two DS18B20 Sensors, via Wio's right Grove connector 
    Data pin to D1
    VCC to 3.3V
    GND to GND
    and a 4.7kΩ resistor between Data and VCC.

Connect Wio Terminal Chassis - Wio-E5 "backpack" for LoRa connectivity.

Project Structure 

CIRCUITPY/
│
├── code.py                 # Main project script
├── lib/                    # Required libraries
│   ├── adafruit_display_shapes/
│   ├── adafruit_display_text/
│   ├── adafruit_bitmap_font/
│   ├── bitmap_font/
│   ├── terminalio/
│   └── ... (other libraries)
└── font/                   # Custom fonts
    └── Terminus24x24.bdf   # Terminus font file

License
This project is licensed under the MIT License. See the LICENSE file for details.
