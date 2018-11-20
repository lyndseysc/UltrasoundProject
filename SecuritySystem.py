#importing all of the necessary packages
import time
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import os


#define functions needed for main fn 
def LED(distance): #LED function is working in place of a camera to check the code/distance measurement is correct while the camera is disabled
    LED0 = 24 #the GPIO on the Pi used
    parameter = 10.0 #parameter is the distance overwhich we do not want the LED to turn on
    if distance <= parameter:
        GPIO.setup(LED0, GPIO.OUT) # Set Pin as output
        GPIO.output(LED0, GPIO.HIGH)# Turn on the LED
        sleep(2) #pauses so we can see the LED 'blink'
        GPIO.output(LED0, GPIO.LOW) #Turn LED off
    sleep(5) #stops the code from constantly outputting, waits 5 seconds before outputting distance again

def record(distance, camera):
    parameter = 50.0  #when the 'suspect' approaches (comes within 0.5m), the camera will record a 5 second video 
    if distance <= parameter:
       camera.start_preview() #preview shows it on the screen while recording
       camera.start_recording('/home/student10/Desktop/videosuspect.h264') #video is saved to desktop
       sleep(5) #defining the length of video
       camera.stop_recording()
       camera.stop_preview()
       
    sleep(5)


def reading():
  
# GPIO output = the pin that's connected to "Trig" on the sensor
# GPIO input = the pin that's connected to "Echo" on the sensor

    TRIG = 11 
    ECHO = 12

    # Disable any warning message such as GPIO pins in use and set up the numbering system
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    camera = PiCamera()
    #create a while loop so the code runs forever 
    while True:
 
        # Setup the GPIO pins for TRIG and ECHO
         
        GPIO.setup(ECHO, GPIO.IN)
        GPIO.setup(TRIG, GPIO.OUT)
         
        time.sleep(0.3)
         
        
        # to get a pulse length of 10Us we need to start the pulse, then
        # wait for 10 microseconds, then stop the pulse. This will 
        # result in the pulse length being 10Us.
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
  
        # listen to the input pin. 0 means nothing is happening. Once a
        # signal is received the value will be 1 so the while loop
        # stops and has the last recorded time the signal was 0
        while GPIO.input(ECHO) == 0:
          signaloff = time.time()
          
        # listen to the input pin. Once a signal is received, record the
        # time the signal came through
        while GPIO.input(ECHO) == 1:
          signalon = time.time()
         
        # work out the difference in the two recorded times above to 
        # calculate the distance of an object in front of the sensor
        timepassed = signalon - signaloff
        print(timepassed) 
        # we now have our distance but it's not in a useful unit of
        # measurement. So now we convert this distance into centimetres
        # Define relation between "distance" and "timepassed"
         
        distance = (34300.0 * timepassed) * 0.5
        print(distance)
        #distance at which the LED turns on/camera starts recording
        #LED(distance) #LED function is commented out once confirmed the camera is working    
        record(distance, camera)

        
def main(): #runs main 
    distance = reading()
main()

