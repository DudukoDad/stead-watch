import serial
import time
import requests
import datetime
import sys
# Configure the serial port
# For Windows: Use 'COM3', 'COM4', etc.
# For Mac/Linux: Use '/dev/ttyACM0' or '/dev/ttyUSB0'
SERIAL_PORT = 'COM3' 
BAUD_RATE = 9600

try:
    # Open the serial connection
    arduino = serial.Serial(port=SERIAL_PORT, baudrate=BAUD_RATE, timeout=0.1)
    
    # Crucial step: Allow the Arduino time to reset after opening the connection
    time.sleep(2) 
    print(f"Connected to Arduino on {SERIAL_PORT}")

    while True:
        # Check if data is available in the buffer
        if arduino.in_waiting > 0:
            # Read a line of data, decode from bytes to string, and remove whitespace
            raw_data = arduino.readline()
            print(raw_data)
            decoded_data = raw_data.decode('utf-8').strip()
            data = {
                    "measurement": "homestead",
                    "location": "Chicke Coop",
                    "device_id": "1",
                    "sensor_data": decoded_data,
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                    }
            print(data)
            resp = requests.post("http://127.0.0.1:8000/api/v1/sensors/sensor-data/", json=data)
            resp.raise_for_status()  # Raise an error if the request was unsuccessful
            print(resp.status_code, resp.text)
            time.sleep(2) # Adjust the sleep time as needed to control the data sending frequency
            # Print the result
            print(f"Received: {decoded_data}")
            
except serial.SerialException as e:
    print(f"Error connecting to serial port: {e}")
except KeyboardInterrupt:
    print("\nProgram stopped by user.")
finally:
    # Ensure the port closes properly upon exit
    if 'arduino' in locals() and arduino.is_open:
        arduino.close()
        print("Serial port closed.")