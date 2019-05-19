import datetime
import os
from os import listdir
from os.path import isfile, join

import cv2
from flask import Flask
from flask import jsonify
from flask import send_file
from gpiozero import MotionSensor, Buzzer

DEVICE = '/dev/video0'
CAPTURES_DIR = os.getcwd() + '/captures/'
SIZE = (640, 480)
app = Flask(__name__)
camera = cv2.VideoCapture(0)
sensor = MotionSensor(1) #GPIO slot for sensor =1
buzzer = Buzzer(2)

@app.route('/api/capture')
def capture():
    FILENAME = CAPTURES_DIR + datetime.datetime.now().isoformat() + ".jpg"
    cv2.imwrite(FILENAME, camera.read()[1])
    return send_file(FILENAME, mimetype='image/jpg')

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

def motion_capture():
    capture()
    buzzer.on()


sensor.when_motion = motion_capture
