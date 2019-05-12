import socket
import time
import cv2
import sys

def int_to_bytes(x):
    x = x.to_bytes((x.bit_length() + 7) // 8, 'big')
    return b'\x00' * (8 - len(x)) + x

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 8090
s.bind((socket.gethostname(), port))
s.listen(5)

cap = cv2.VideoCapture(0)
while cap.isOpened():
    cs, address = s.accept()
    flags, frame = cap.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('img', frame)
    retval, data = cv2.imencode('.jpg', frame)
    #
    cs.sendall(int_to_bytes(sys.getsizeof(data)) + data.tobytes())
cap.release()
cv2.destroyAllWindows()