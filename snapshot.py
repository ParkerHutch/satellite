from picamera import PiCamera
import subprocess
from time import sleep

try:
    camera = PiCamera() # Make sure to close this
except:
    print('no official Raspberry Pi camera connected')

def get_num_cameras():
    cmd_output = subprocess.check_output(['script', '-c', '(fswebcam --list-inputs)']).decode('utf-8')
    # TODO delete automatically created typescript file
    start = 'Available inputs:'
    end = 'No input was specified'
    first_run = (cmd_output.split(start)[1]).split(end)[0]
    last_semicolon_index = first_run.rfind(':')
    largest_device_index = int(first_run[last_semicolon_index - 1: last_semicolon_index])
    return largest_device_index


def take_picture(device, output_file):
    if device == 'picamera':
        camera.capture(output_file)
    elif device == 'webcam':
        print('inputs found:', get_num_cameras())
        
        #inputs = subprocess.check_output(['fswebcam', '--list-inputs'], stderr=subprocess.STDOUT)
        #print('inputs return: ')
        #print(inputs)
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