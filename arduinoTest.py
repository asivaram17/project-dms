import pyfirmata
 2 import time
 3 
 4 board = pyfirmata.Arduino('/dev/ttyACM0')
 5 
 6 while True:
 7     board.digital[13].write(1)
 8     time.sleep(1)
 9     board.digital[13].write(0)
10     time.sleep(1)