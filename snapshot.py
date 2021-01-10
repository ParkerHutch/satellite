from picamera import PiCamera
from time import sleep

camera = PiCamera() # Make sure to close this

def take_picture(output_file):
    camera.capture(output_file)

def stop():
    camera.close()

if __name__ == 'main':
    print('Taking a picture')
    camera.capture('image.jpg')
    print('Done')
    stop()