from picamera import PiCamera
from time import sleep

with PiCamera() as camera:
    camera.capture('./images/image.jpg')