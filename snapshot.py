from picamera import PiCamera
import subprocess
from time import sleep

try:
    camera = PiCamera() # Make sure to close this
except:
    print('no official Raspberry Pi camera connected')

def take_picture(device, output_file):
    if device == 'picamera':
        camera.capture(output_file)
    elif device == 'webcam':
        print('inputs found:')
        inputs = subprocess.check_output(['fswebcam', '--list-inputs'])
        print('inputs return: ')
        print(inputs.stdout)
        print('taking picture')
        subprocess.run(['fswebcam', '-r', '1280x720', '--no-banner', '-q', output_file])
    else:
        print(f'device {device} is not supported')


def stop():
    camera.close()

if __name__ == 'main':
    print('Taking a picture')
    camera.capture('image.jpg')
    print('Done')
    stop()