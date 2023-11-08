import time
import board
import serial
import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
import subprocess
import os

#change ttyusb1 to whatever scriptusb says
#run ./scriptusb.sh

#run ./scripusb.sh and capture the output
result = subprocess.run(['./scriptusb.sh'], stdout=subprocess.PIPE)
output = result.stdout.decode('utf-8')
output = output.split('\n')
output = [x for x in output if x != '']
port = ""
for device in output:
    device = device.split(' ')
    if device[1] == "Prolific_Technology_Inc._USB-Serial_Controller":
        port = device[0]

# if port == "":
#     # raise Exception("Fingerprint Reader not found")
#     return
print("fingerprint reader on port: ", port)
if port:
    uart = serial.Serial(port, baudrate=57600, timeout=1)
    finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
# uart = serial.Serial("/dev/ttyUSB1", baudrate=57600, timeout=1)
# finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def clear_sensor():
    for i in finger.templates:
        if finger.delete_model(i) == adafruit_fingerprint.OK:
            print("Deleted model", i)
        else:
            print("Failed to delete model", i)

def enroll_finger(idx,finger_label):
    
    for fingerimage in range(1,4):
        if fingerimage == 1:
            finger_label.configure(text="Place your finger on the sensor")
        else:
            finger_label.configure(text="Place your finger again")
            
        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                break
        
        print("Templating...")
        if finger.image_2_tz(fingerimage) != adafruit_fingerprint.OK:
            print("Failed to template")
            return False
        
        finger_label.configure(text="Remove your finger")
        while finger.get_image() != adafruit_fingerprint.NOFINGER:
            pass
        
        time.sleep(1)
        
    print("Creating model...")
    if finger.create_model() != adafruit_fingerprint.OK:
        print("Failed to create model")
        return False
    
    print("Storing model")
    if finger.store_model(idx) != adafruit_fingerprint.OK:
        print("Failed to store model")
        return False
    
    print("Stored")
    return True
        
        
        
        
            
def fingerprint_register(user, finger_label):
    
    finger.read_templates()
    if len(finger.templates) == 0:
        idx = 1
    else:
        idx = max(finger.templates) + 1
    
    #go to /db/user and create fingerid.txt
    #fingerid.txt will contain the fingerprint id
    #fingerprint id will be used to search for the fingerprint template
    
    #if user exists and fingerid.txt exists
    if os.path.exists("./db/"+user+"/fingerid.txt"):
        #read fingerid.txt
        with open("./db/"+user+"/fingerid.txt", "r") as f:
            idx = int(f.read())
            print("idx: ", idx)
            #if idx is in templates
            if idx in finger.templates:
                #delete the template
                if finger.delete_model(idx) == adafruit_fingerprint.OK:
                    print("Deleted model", idx)
                else:
                    print("Failed to delete model", idx)
    
    #if user exists and fingerid.txt does not exist
    else:
        #create fingerid.txt
        with open("./db/"+user+"/fingerid.txt", "w") as f:
            f.write(str(idx))
    
    #enroll fingerprint
    enroll_finger(idx, finger_label)
    


if __name__ == "__main__":
    finger.read_templates()
    print(finger.templates)
    clear_sensor()