import time
import os
from os import listdir
from os.path import isfile, join

import pygame
import pygame.camera
from flask import Flask
from flask import jsonify
from flask import send_file

DEVICE = '/dev/video0'
CAPTURES_DIR = os.getcwd() + '/captures/'
SIZE = (640, 480)
app = Flask(__name__)
pygame.init()
pygame.camera.init()
display = pygame.display.set_mode(SIZE, 0)
camera = pygame.camera.Camera(DEVICE, SIZE)
camera.start()

@app.route('/api/capture')
def capture():
    FILENAME = CAPTURES_DIR + time.strftime("%x,%X").replace("/",".") + ".png"
    pygame.display.flip()
    screen = pygame.surface.Surface(SIZE, 0, display)
    screen = camera.get_image(screen)
    pygame.image.save(screen, FILENAME)
    return send_file(FILENAME, mimetype='image/png')

@app.route('/api/images')
def images():
    onlyfiles = [f for f in listdir(CAPTURES_DIR) if isfile(join(CAPTURES_DIR, f))]
    return jsonify(onlyfiles)

@app.route('/api/images/<img>')
def showimage(img):
    FILENAME = CAPTURES_DIR + img
    return send_file(FILENAME, mimetype='image/png')

@app.route('/quit')
def quit():
    camera.stop()
    pygame.quit()
