from picamera import PiCamera
import subprocess
from time import sleep

try:
    camera = PiCamera() # Make sure to close this on program end
except:
    print('no official Raspberry Pi camera connected')

mounted_cameras = {}

def find_cameras():
    global mounted_cameras 
    mounted_cameras = {}
    for i in range(10):
        num_cameras = get_num_cameras(i)
        if num_cameras > 0:
            mounted_cameras[f'/dev/video{i}'] = num_cameras
    

# get the number of cameras installed for the given /dev/video mount.
def get_num_cameras(mount_num):
    cmd_output = subprocess.check_output(['script', '-q', '-c', f'(fswebcam --list-inputs -d /dev/video{mount_num})']).decode('utf-8')
    error_messages = ['Unable to query input 0.', 'No such file or directory']
    if any(message in cmd_output for message in error_messages):
        print(f'Error for {mount_num}')
        return 0
    else:
        # TODO delete automatically created typescript file
        start = 'Available inputs:'
        end = 'No input was specified'
        first_run = (cmd_output.split(start)[1]).split(end)[0]
        last_semicolon_index = first_run.rfind(':')
        largest_device_index = int(first_run[last_semicolon_index - 1: last_semicolon_index])
        return largest_device_index + 1


def take_picture(device, output_file):
    find_cameras() # TODO maybe make sure this is only run once
    if device == 'picamera':
        camera.capture(output_file)
    elif device == 'webcam':
        #print('inputs found:', get_num_cameras())

        print('taking pictures')

        for mount, cameras in mounted_cameras:
            for camera in range(cameras):
                print(f'Taking picture on mount{mount} with camera{camera}')
                subprocess.run(['fswebcam', '-r', '-d', mount, '1280x720', '--no-banner', '-q', output_file+camera])

        #subprocess.run(['fswebcam', '-r', '1280x720', '--no-banner', '-q', output_file])
    else:
        print(f'device {device} is not supported')


def stop():
    camera.close()

if __name__ == '__main__':
    print('finding cameras')
    find_cameras()
    print(mounted_cameras)
    stop()