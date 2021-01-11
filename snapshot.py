from picamera import PiCamera
import subprocess
from time import sleep

devices = {}
# TODO use -palette option with fswebcam to take jpeg pictures
# TODO experiment with fswebcam flags for better pictures
# TODO separate args into tuning and output arrays that are combined
# whenever a photo is taken (use array unpacking?)
try:
    global camera
    camera = PiCamera() # Make sure to close this on program end
except:
    camera = None
    print('no official Raspberry Pi camera connected')


def find_devices():
    """Create a dictionary of device filepaths as keys and the corresponding 
    number of cameras as values. Only devices that have 1 or more cameras are
    stored. If the PiCamera is connected, it will not be included in this list.
    """

    global devices 
    devices = {}
    for i in range(10):
        num_cameras = get_num_cameras(i)
        if num_cameras > 0:
            devices[f'/dev/video{i}'] = num_cameras

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
        inputs_found = (cmd_output.split(start)[1]).split(end)[0]
        last_colon_index = inputs_found.rfind(':')
        largest_device_index = int(
            inputs_found[last_colon_index - 1: last_colon_index])
        return largest_device_index + 1

def take_picture(device: str = 'all', output_file_directory: str = "./images/"):
    """Take a picture using the given device, or on all connected devices, and
    store the output in the given directory.

    Args:
        device (str, optional): The device to use to take pictures. Defaults to
        'all'.
        output_file_directory (str, optional): The relative filepath to store
        output images in. Defaults to "./images/".
    """
    global camera
    if device == 'picamera':
        camera.capture(output_file_directory + 'image.jpg')
    elif device == 'all':
        picture_num = 0 # TODO maybe generate random number if images already exist
        # Take a picture on the PiCamera
        if camera is not None:
            camera.capture(output_file_directory + f'image{picture_num}.jpg')
            picture_num += 1
        
        # Take a picture on all connected USB cameras
        find_devices() # TODO maybe make sure this is only run once

        # Clear the camera_log.txt file if it exists
        open('./camera_log.txt', 'w').close()

        f = open('./camera_log.txt', 'a')
        for mount, cameras in devices.items(): # TODO rename mount variable
            for _ in range(cameras):
                # TODO route the output from below to a log file, then make sure it's not displayed in console
                f.write(f'Taking picture with device {mount}\n')
                f.flush()
                subprocess.run([
                    'fswebcam', '-r', '1280x720', '-d', mount, '--no-banner', 
                    '-q', '--banner-colour', '#FF0000', '--no-shadow', '--title', 'Title test', 
                    '--subtitle', 'Subtitle test', '--info', 'Info test', 
                    output_file_directory + f'image{str(picture_num)}.jpg'
                ], stdout=f, stderr=f)
                f.write(f'Finished taking picture with device{mount}\n')
                f.flush()
                picture_num += 1
        f.close()
    elif device.startswith('/dev/video'):
        subprocess.run([
            'fswebcam', '-r', '1280x720', '-d', device, '--no-banner', '-q', 
            output_file_directory + f'image.jpg'
        ])
    else:
        print(f'device {device} is not supported')


def stop():
    """Close the PiCamera if it was initialized.
    """
    global camera
    if camera is not None:
        camera.close()

if __name__ == '__main__':
    find_devices()
    print('Devices found:')
    print(devices)
    stop()