from picamera import PiCamera
import subprocess
from time import sleep

mounted_cameras = {}

try:
    global camera
    camera = PiCamera() # Make sure to close this on program end
except:
    print('no official Raspberry Pi camera connected')

def find_cameras():
    global mounted_cameras 
    mounted_cameras = {}
    for i in range(10):
        num_cameras = get_num_cameras(i)
        if num_cameras > 0:
            mounted_cameras[f'/dev/video{i}'] = num_cameras

    

def get_num_cameras(mount_num: int) -> int:
    """Get the number of cameras associated with the given video device. To 
    find the number of cameras, this function calls fswebcam with the
    --list-inputs flag on the /dev/video{mount_num} device and parses the output
    to find the last input's associated number. For a mount with one camera, the
    parsed output will be '0:Camera 1'. This function interprets the number
    found before the last colon to as the largest camera index. It is assumed
    that there is a valid camera on this mount for every integer value between
    this index and 0, and including 0.

    Args:
        mount_num (int): the postfix to the /dev/video path to check for 
        cameras on

    Returns:
        int: The number of valid cameras connected to the mount 
        /dev/video{mount_num}.
    """

    cmd_output = subprocess.check_output(['script', '-q', '-c', f'(fswebcam --list-inputs -d /dev/video{mount_num})'], text=True)
    error_messages = ['Unable to query input 0.', 'No such file or directory', 'Message from syslogd@raspberrypi']
    if any(message in cmd_output for message in error_messages):
        return 0
    else:
        # TODO delete automatically created typescript file
        start = 'Available inputs:'
        end = 'No input was specified'
        first_run = (cmd_output.split(start)[1]).split(end)[0]
        last_semicolon_index = first_run.rfind(':')
        largest_device_index = int(first_run[last_semicolon_index - 1: last_semicolon_index])
        return largest_device_index + 1

def take_picture(device: str = 'all', output_file_directory: str = "./images/"):
    
    if device == 'picamera':
        global camera
        print('taking picture with PiCamera') 
        camera.capture(output_file_directory + 'image.jpg')
    elif device == 'all':
        find_cameras() # TODO maybe make sure this is only run once
        picture_num = 0 # TODO maybe generate random number if images already exist
        for mount, cameras in mounted_cameras.items():
            for camera_number in range(cameras):
                print(f'Taking picture on mount{mount} with camera{camera_number}')
                subprocess.run(['fswebcam', '-r', '1280x720', '-d', mount, '--no-banner', '-q', output_file_directory + f'image{str(picture_num)}.jpg'])
                picture_num += 1
    elif device.startswith('/dev/video'):
        subprocess.run(['fswebcam', '-r', '1280x720', '-d', device, '--no-banner', '-q', output_file_directory + f'image.jpg'])
    else:
        print(f'device {device} is not supported')


def stop():
    global camera
    if camera is not None:
        camera.close()

if __name__ == '__main__':
    find_cameras()
    print(mounted_cameras)
    stop()