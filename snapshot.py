from picamera import PiCamera
import subprocess
from time import sleep

camera = PiCamera() # Make sure to close this

def take_picture(device, output_file):
    if device == 'picamera':
        camera.capture(output_file)
    elif device == 'webcam':
        subprocess.run(['fswebcam', '-r', '1280x720', '--no-banner', output_file])


def stop():
    camera.close()

if __name__ == 'main':
    print('Taking a picture')
    camera.capture('image.jpg')
    print('Done')
    stop()