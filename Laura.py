##############################################################################################################
########################################### CarBar automation ################################################

##This is the script that automates CarBar and allows for its movement, facial recognition, and coming soon,
##facial recognition. This is still a WIP at this stage. 

##############################################################################################################


import RPi.GPIO as gpio
import time
import cv2
import pygame

def init() :  #Python function that initializes the GPIO board
    gpio.setmode(gpio.BOARD)
    gpio.setup(7, gpio.OUT)
    gpio.setup(11, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    gpio.setup(15, gpio.OUT)

def forward(timeframe) :   ##Defines forward movement for the car. Takes timeframe as input. 
    init()
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, True)
    gpio.output(15, False)
    time.sleep(timeframe)
    gpio.cleanup()

def reverse(timeframe):  ##Defines reverse movement for the car. Takes timeframe as input
    init()
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(timeframe)
    gpio.cleanup()

def turn_right(timeframe):  ## Defines the right turn for the car. Takes timeframe as input
    init()   
    gpio.output(7,  True)
    gpio.output(11, True)
    gpio.output(13, False)
    gpio.output(15, False)
    time.sleep(timeframe)
    gpio.cleanup()


def turn_left(timeframe):  ## Defines the left turn for the car. Takes timeframe as input 
    init()
    gpio.output(7,  False)
    gpio.output(11, False)
    gpio.output(13, True)
    gpio.output(15, True)
    time.sleep(timeframe)
    gpio.cleanup()

def sound_player(sound):  ##This function plays the sound and takes the sound path as input
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()

## Define actions that make the robot more life-like, aka singing, saying random things, 
## asking for something...etc.

sounds = ["./AudioFiles/Hello_Plural.wav","./AudioFiles/hello_singular.wav",
          "./AudioFiles/nice_to_see_you_plural.wav","./AudioFiles/nice_to_see_you_singular.wav",
	  "./AudioFiles/scientist_ahmad_chaiban.wav","./AudioFiles/you_are_not_my_master_singular.wav",
      "./AudioFiles/you_mean_yes.wav"]   ## Array of sounds here

video = cv2.VideoCapture(0)  ## This captures the video feed from the camera constantly

a = 1  ## variable to keep track of the number of iterations
face_cascade = cv2.CascadeClassifier("./openCV Model/haarcascade_frontalface_default.xml")  ## Reads the CV model
while_breaker = 0  ## This is for breaking the while loop

## Begin Main Loop
while True:    ## infinite while loop being performed here
    a = a+1
    check,frame = video.read()  ## Reads a single frame from the video feed
    camera_face = face_cascade.detectMultiScale(frame,scaleFactor=1.05,minNeighbors=5) ## attempts to detect a face in the frame
    if len(camera_face) > 0:  ## Checks if a face was indeed found in the camera
        if len(camera_face)>1:  ## Checks if more than one face was found
	        sound_player(sounds[0])  ## Says hello to more than one human found
    	else:                        ## checks if only one face was found
            sound_player(sounds[1])  ## Says hello to one human found
        face_not_in_middle = True    ## Assumes that the human face is not in the middle
        while face_not_in_middle == True:  ## Looop on the condition that the human face is not in the middle
            if while_breaker >3:   ##If a face was not detected 3 times, break the loop 
                while_breaker = 0   ##This resets the face count
                break               ##This break is done so that Laura can say hi to the human again
            check,frame = video.read()  ##reads another frame from the video feed
            face_position = face_cascade.detectMultiScale(frame,scaleFactor=1.05,minNeighbors=5)  ##Attempts to detect the face
            if len(face_position) > 0:   ## if a face was indeed detected
		        print("seen")          ## print "seen"
                face_position_real = face_position[0][0]  ##Find the x-coordinate of the face
                w = face_position[0][2]                  ##find the z-coordinate of the face
                if 160<= face_position_real <= 320 and 150<=w<=190:   ##These ranges are considered to be the safe zone of the face
                    face_not_in_middle = False  ## Specifies that the face is indeed in the midle
                elif w<150:        ##condition for being too far from the human
                    forward(0.3)
                elif w>190:        ##condition for being too close to the human
                    reverse(0.3)
                if face_position_real <160:  ##condition for turning too far right from the human
                    turn_left(0.3)
                elif face_position_real >320:  ##condition for turning too far left from the human
                    turn_right(0.3)
    else:
	    while_breaker +=1  ## If no face was detected, iterate +1 to the inner while loop breaker
	
    key = cv2.waitKey(1)  ##Allows for input from keyboard to CV

    if key == ord('q'):
        break      ## Break the original while loop if "q" is pressed 
video.release()  ## Release the video caputre
cv2.destroyAllWindows ## Destroy all windows
