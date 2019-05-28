import datetime
import os
from os import listdir
from os.path import isfile, join
import urllib
import requests
import cv2
from flask import Flask
from flask import Response
from flask import jsonify
from flask import send_file
from gpiozero import MotionSensor, Buzzer, Button
import time
import numpy as np
from Camera import Camera
from threading import Thread

DEVICE = '/dev/video0'
CAPTURES_DIR = os.getcwd() + '/captures/'
SIZE = (640, 480)
app = Flask(__name__)
cam = Camera()
sensor = MotionSensor(24)  # GPIO slot for sensor =1
buzzer = Buzzer(23)
door = Button(18)
#
buzzer.on()
time.sleep(1)
buzzer.off()


@app.route('/api/capture')
def capture():
    FILENAME = CAPTURES_DIR + datetime.datetime.now().isoformat() + ".jpg"
    cv2.imwrite(FILENAME, cam.camera.read()[1])
    return send_file(FILENAME, mimetype='image/jpg')


def capture_nohttp():
    FILENAME = CAPTURES_DIR + datetime.datetime.now().isoformat() + ".jpg"
    cv2.imwrite(FILENAME, cam.camera.read()[1])


@app.route('/api/images')
def images():
    onlyfiles = [{"name": f} for f in listdir(CAPTURES_DIR) if isfile(join(CAPTURES_DIR, f))]
    return jsonify(onlyfiles)

@app.route('/api/alarm')
def get_alarm():
    return jsonify({"alarm": cam.alarm})

@app.route('/api/images/<img>')
def showimage(img):
    FILENAME = CAPTURES_DIR + img
    return send_file(FILENAME, mimetype='image/jpg')


@app.route('/api/live')
def livestream():
    return Response(gen(cam), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/api/toggle')
def toggle_alarm():
    _toggle_alarm(not cam.alarm)
    return ""


def _toggle_alarm(cond):
    cam.alarm = cond
    if cam.alarm:
        for i in range(0, 5):
            buzzer.on()
            time.sleep(0.5)
            buzzer.off()
            time.sleep(0.5)
    else:
        buzzer.off()


def door_unlock():
    print("Door unlocked, starting stream")
    _toggle_alarm(True)
    # gen(cam)


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


@async
def motion_capture():
    with app.app_context():
        capture_nohttp()
        print("motion detected")
        _toggle_alarm(True)
        # buzzer.on()
        # time.sleep(0.5)
        # buzzer.off()


@async
def fsensor():
    with app.app_context():
        sensor.when_motion = motion_capture
        door.when_released = door_unlock


fsensor()

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
