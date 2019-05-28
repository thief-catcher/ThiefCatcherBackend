import time
import threading

import cv2

from CameraEvent import CameraEvent


class Camera():
    alarm = False
    thread = None
    frame = None
    last_access = 0
    event = CameraEvent()
    video_source = 0
    camera = cv2.VideoCapture(0)

    def __init__(self):

        """Start the background camera thread if it isn't running yet."""
        if Camera.thread is None:
            Camera.last_access = time.time()

            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames are available
            while self.get_frame() is None:
                time.sleep(0)

    def _thread(cls):
        """Camera background thread."""
        print('Starting camera thread.')
        frames_iterator = cls.frames()
        for frame in frames_iterator:
            Camera.frame = frame
            Camera.event.set()  # send signal to clients
            time.sleep(0)

            # # if there hasn't been any clients asking for frames in
            # # the last 10 seconds then stop the thread
            # if time.time() - Camera.last_access > 10:
            #     frames_iterator.close()
            #     print('Stopping camera thread due to inactivity.')
            #     break
        Camera.thread = None

    @staticmethod
    def frames():

        if not Camera.camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = Camera.camera.read()

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

    def get_frame(self):
        """Return the current camera frame."""
        Camera.last_access = time.time()

        # wait for a signal from the camera thread
        Camera.event.wait()
        Camera.event.clear()

        return Camera.frame

