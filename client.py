import socket
import cv2
import numpy as np
from PIL import Image
import sys
# Create a var for storing an IP address:
ip = "192.168.1.10"



# Create some more var's:
timer = 0
previousImage = ""
image = ""

# Main program loop:
while 1:

    # We use a timer to limit how many images we request from the server each second:
    if timer < 1:

        # Create a socket connection for connecting to the server:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((str(ip), 8090))

        # Recieve data from the server:
        size = client_socket.recv(8)
        size = int.from_bytes(size, 'big')
        data = client_socket.recv(size)
        # Set the timer back to 30:
        timer = 30

    else:

        # Count down the timer:
        timer -= 1

    # We store the previous recieved image incase the client fails to recive all of the data for the new image:
    previousImage = image

    # We use a try clause to the program will not abort if there is an error:
  #  try:

        # We turn the data we revieved into a 120x90 PIL image:
        #image = Image.fromstring("RGB", (640, 480), data)

        # We resize the image to 640x480:
        #image = image.resize((640, 480))

        # We turn the PIL image into a surface that PyGame can display:

    image = cv2.imdecode(np.frombuffer(data, dtype='uint8'), cv2.IMREAD_COLOR)
    cv2.imshow("chuj", image)
    key = cv2.waitKey(1) & 0xFF

   # except:

        # If we failed to recieve a new image we display the last image we revieved:
      #  image = previousImage

    # Set the var output to our image:
    output = image
