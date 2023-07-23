import serial 
import time


ser = serial.Serial('/dev/ttyACM0',115200, timeout=1.0)
"""def SerialArduino():
    try :
        while True:
            if (ser.in_waiting>0):
                data = ser.readline()
                data = data.decode()
                data1 = data.rstrip()
                print(data)
                sleep(1)
    except KeyboardInterrupt:
        ser.close()"""          
time.sleep(3)
ser.reset_input_buffer()
print("Serial OK") 
try:
        while True:
                #time.sleep(0.01)
                if (ser.in_waiting>0):
                        line = int(ser.readline().decode())
                        if(line==0):
                                print("toc do duoi 10km/h")
                        else:
                                print("toc do lon")
except KeyboardInterrupt:
        print("end com") 
        ser.close() 
        
