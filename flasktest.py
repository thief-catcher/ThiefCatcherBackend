from os import listdir
from os.path import isfile, join
import pygame
import pygame.camera
from pygame.locals import *
from flask import Flask
from flask import send_file
from flask import jsonify
import time
DEVICE = '/dev/video0'
SIZE = (640, 480)
app = Flask(__name__)
pygame.init()
pygame.camera.init()
display = pygame.display.set_mode(SIZE, 0)
camera = pygame.camera.Camera(DEVICE, SIZE)
camera.start()

@app.route('/api/capture')
def capture():
    FILENAME = '/home/pi/captures/' + time.strftime("%x,%X").replace("/",".") + ".png"
    pygame.display.flip()
    screen = pygame.surface.Surface(SIZE, 0, display)
    screen = camera.get_image(screen)
    pygame.image.save(screen, FILENAME)
    return send_file(FILENAME, mimetype='image/png')

@app.route('/api/images')
def images():
    onlyfiles = [f for f in listdir('/home/pi/captures/') if isfile(join('/home/pi/captures/', f))]
    return jsonify(onlyfiles)

@app.route('/api/images/<img>')
def showimage(img):
    FILENAME = '/home/pi/captures/' + img
    return send_file(FILENAME, mimetype='image/png')

@app.route('/quit')
def quit():
    camera.stop()
    pygame.quit()
