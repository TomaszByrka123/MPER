#!/venv/bin/python
#OBSŁUGA KOMUNIKACJI Z ARDUINO PRZEZ UART

import serial
import threading
import time

class Arduino:
    def __init__(self, serial_port):
        self.serial_port = serial_port
        self.arduino = serial.Serial(self.serial_port, 9600, timeout=1)
        self.arduino.reset_input_buffer()
        self.is_running = False
        self.thread = None
        self.received_data = None 


    def get_data(self):
        while self.is_running:
            if self.arduino.in_waiting > 0:
                line = self.arduino.readline().decode().rstrip()
                self.received_data = line


    def start_get_data(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self.get_data)
            self.thread.start()


    def stop_get_data(self):
        if self.is_running:
            self.is_running = False
            self.thread.join()


    def send_data(self, data):
        try:
            self.data_str = ','.join(map(str, data)) + '\n'
            self.arduino.write(self.data_str.encode())
            time.sleep(0.1)
        except Exception as e:
            print(f"Błąd wysyłania danych: {str(e)}")


    def __del__(self):
        if 'arduino' in locals() and self.arduino.is_open:
            self.arduino.close()

