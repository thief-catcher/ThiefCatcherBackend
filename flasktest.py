import datetime
import os
from os import listdir
from os.path import isfile, join
import urllib
import requests
import cv2
from flask import Flask
from flask import jsonify
from flask import send_file
from gpiozero import MotionSensor, Buzzer, InputDevice
import time
import numpy as np

CAPTURES_DIR = os.getcwd() + '/captures/'
SIZE = (640, 480)
app = Flask(__name__)
sensor = MotionSensor(24) #GPIO slot for sensor =1
buzzer = Buzzer(23)
door = InputDevice(18)

buzzer.on()
time.sleep(1)
buzzer.off()





@app.route('/api/images/capture')
def takePhoto():
    req = urllib.request.urlopen('http://localhost:8080/?action=snapshot')
    arr = np.asarray(bytearray(req.read()), dtype='uint8')
    img = cv2.imdecode(arr, -1)
    cv2.imwrite(CAPTURES_DIR + datetime.datetime.now().isoformat() + ".jpg", img)
    return """"""


@app.route('/api/images')
def images():
    onlyfiles = [{"name": f} for f in listdir(CAPTURES_DIR) if isfile(join(CAPTURES_DIR, f))]
    return jsonify(onlyfiles)


@app.route('/api/images/<img>')
def showimage(img):
    FILENAME = CAPTURES_DIR + img
    return send_file(FILENAME, mimetype='image/jpg')

@app.route('/api/mute')
def mute_buzzer():
    buzzer.off()
    print(door.value)

def motion_capture():
    takePhoto()
    print("motion detected")
    buzzer.on()

def test():
    print("dziala")

sensor.when_motion = motion_capture
sensor.when_no_motion = mute_buzzer
