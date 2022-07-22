import serial
import time


portVar = "/dev/ttyACM0"
serialInst = serial.Serial()

serialInst.baudrate = 9600
serialInst.port = portVar
serialInst.open()

while True:
    command = input("Choose a direction (w/a/s/d): ")
    serialInst.write(command.encode('utf-8'))
    
    if command == 'exit':
        exit()




