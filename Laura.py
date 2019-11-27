#################################################################################################################
########################################### CarBar automation ###################################################

##This is the script that automates CarBar and allows for its movement, facial recognition, and coming soon,
##facial recognition. This is still a WIP at this stage. 


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

def forward(timeframe) :   ##Defines 
    init()
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, True)
    gpio.output(15, False)
    time.sleep(timeframe)
    gpio.cleanup()

def reverse(timeframe):
    init()
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(timeframe)
    gpio.cleanup()

def turn_right(timeframe): 
    init()   
    gpio.output(7,  True)
    gpio.output(11, True)
    gpio.output(13, False)
    gpio.output(15, False)
    time.sleep(timeframe)
    gpio.cleanup()


def turn_left(timeframe):
    init()
    gpio.output(7,  False)
    gpio.output(11, False)
    gpio.output(13, True)
    gpio.output(15, True)
    time.sleep(timeframe)
    gpio.cleanup()

def sound_player(sound):
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()

## Define actions that make the robot more life-like, aka singing, saying random things, asking for something...etc.

sounds = ["Hello_Plural.wav","hello_singular.wav","nice_to_see_you_plural.wav","nice_to_see_you_singular.wav",
	  "scientist_ahmad_chaiban.wav","you_are_not_my_master_singular.wav","you_mean_yes.wav"]

video = cv2.VideoCapture(0)

a = 1
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
while_breaker = 0
while True:
    turn_left(1)
    a = a+1
    check,frame = video.read()
    camera_face = face_cascade.detectMultiScale(frame,scaleFactor=1.05,minNeighbors=5)
    if len(camera_face) > 0:
        if len(camera_face)>1:
	    sound_player(sounds[0])
    	else:
	    sound_player(sounds[1])
        face_not_in_middle = True
        while face_not_in_middle == True:
	    if while_breaker >3:
		while_breaker = 0
                break
            check,frame = video.read()
            face_position = face_cascade.detectMultiScale(frame,scaleFactor=1.05,minNeighbors=5)
            if len(face_position)>0:
		print("seen")
                face_position_real = face_position[0][0]
                w = face_position[0][2]
                if 160<= face_position_real <= 320 and 150<=w<=190:
                    face_not_in_middle = False
                elif w<150:
                    forward(0.3)
                elif w>190:
                    reverse(0.3)
                if face_position_real <160:
                    turn_left(0.3)
                elif face_position_real >320:
                    turn_right(0.3)
    else:
	while_breaker +=1
	
    key = cv2.waitKey(1)

    if key == ord('q'):
        break
video.release()
cv2.destroyAllWindows
