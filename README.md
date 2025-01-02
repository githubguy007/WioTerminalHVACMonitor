# Wio Terminal HVAC DeltaT Monitor with LoRa

## Introduction

Based on Seeed Wio Terminal hardware, the HVAC DeltaT Monitor with LoRa is designed to monitor and display temperature and humidity data from multiple sensors. It leverages LoRaWAN via The Things Network for wireless communication, making it ideal for remote HVAC monitoring in difficult utility rooms. The device displays real-time data on its built-in screen and (eventually) sends sensor readings to Adafruit IO for further and long-term trend analysis. 

<img width="1020" alt="Screenshot 2025-01-01 at 5 13 51 PM" src="https://github.com/user-attachments/assets/febe5290-dda0-4197-bb15-f8c5267723b5" />

## Features

 - Real-Time Monitoring: Displays Utility room temperature & relative humidity, HVAC return and supply temperatures, and HVAC Delta Temperature (ΔT) - the difference between return air temperature and supply air temperature - very common in the HVAC Industry.
 - LoRaWAN Connectivity: Sends sensor data wirelessly over long distances using LoRa technology.
 - Multiple Sensors Support: Integrates SHT4x (temperature and humidity) and DS18X20 (temperature) sensors.

## Hardware Requirements

 - Seeed Wio Terminal ATSAMD51
 - Seed Wio Terminal Chassis - Wio-E5
 - Adafruit SHT4x, or compatible, Sensor
 - DS18B20 Temperature Sensors (2 units)
 - Grove & Grove to STEMMA QT (Qwiic) connector 
 - Wires, Wago connectors, and USB-C Power Supply

## Software Requirements

 - CircuitPython 8.2.10
 - Adafruit Libraries for CircuitPython
   - adafruit_display_shapes
   - adafruit_display_text
   - adafruit_bitmap_font
   - bitmap_font (for custom fonts)
   - terminalio font
   - and, dependencies 
  
## Hardware Assembly

 - SHT4x Sensor, via Wio's left Grove connector 
   - VCC to 3.3V 
   - GND to GND
   - SCL to SCL
   - SDA to SDA
    
 - Two DS18B20 Sensors, via Wio's right Grove connector
   -
   - Data pin to D1
   - VCC to 3.3V
   - GND to GND
   - and a 4.7kΩ resistor between Data and VCC.

 - Connect Wio Terminal Chassis - Wio-E5 "backpack" for LoRa connectivity.

## Network Requirements

  - Connectivity to The Things Network
  - MQTT Feed to Node-RED
  - Node-RED Fuctions to re-write into the format expected by Adafruit IO
  - Webhooks into Adafruit IO (and Adafruit IO subscription)

## Eventually this is what dashboards on Adafruit IO might look like.

<img width="775" alt="Screenshot 2025-01-01 at 5 26 42 PM" src="https://github.com/user-attachments/assets/3d958ba3-b71c-4eda-be81-091110fe4d21" />

## Project Structure 

### CIRCUITPY/
  - code.py  # Main project script
  - lib/     # Required libraries
    - adafruit_display_shapes/
    - adafruit_display_text/
    - adafruit_bitmap_font/
    - bitmap_font/
    - terminalio/
    - ... (other libraries)
  - font/                   # Custom fonts
    - Terminus24x24.bdf   # Terminus font file
      
 ### TTN/ # Contains Decoder for The Things Network

## License

This project is licensed under the MIT License. See the LICENSE file for details.

