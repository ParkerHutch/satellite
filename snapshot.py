from picamera import PiCamera
from time import sleep

camera = PiCamera()

with PiCamera() as camera:
    camera.capture('./images/image.jpg')
#camera.start_preview()
#sleep(5)

#camera.stop_preview()