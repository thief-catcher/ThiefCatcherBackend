import datetime
import os
from os import listdir
from os.path import isfile, join

import cv2
from flask import Flask
from flask import Response
from flask import jsonify
from flask import send_file

from Camera import Camera

DEVICE = '/dev/video0'
CAPTURES_DIR = os.getcwd() + '/captures/'
SIZE = (640, 480)
app = Flask(__name__)
cam = Camera()
#
#
@app.route('/api/capture')
def capture():
    FILENAME = CAPTURES_DIR + datetime.datetime.now().isoformat() + ".jpg"
    cv2.imwrite(FILENAME, cam.camera.read()[1])
    return send_file(FILENAME, mimetype='image/jpg')
#

@app.route('/api/images')
def images():
    onlyfiles = [{"name": f} for f in listdir(CAPTURES_DIR) if isfile(join(CAPTURES_DIR, f))]
    return jsonify(onlyfiles)


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
